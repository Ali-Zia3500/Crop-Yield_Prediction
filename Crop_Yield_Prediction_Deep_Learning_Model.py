# -*- coding: utf-8 -*-
"""Deep_Learn_Model_Yield_Prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oIT9uQxY2upxRsp7lNehqPsmGgFUixtd
"""

# Commented out IPython magic to ensure Python compatibility.
from ast import increment_lineno
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,LSTM,Dropout
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
# %matplotlib inline

df_yield = pd.read_csv("/content/yield.csv")
df_yield.shape

df_yield.head()

df_yield.tail()

df_yield = df_yield.rename(index=str,columns = {"Value" : "hg/ha_yield"})
df_yield.head()

print(df_yield.columns)

df_yield = df_yield.drop(["Year Code","Element Code", "Element", "Year Code", "Area Code", "Domain Code", "Domain", "Unit", "Item Code"],axis=1)
df_yield.head()

df_yield.tail(10)

df_yield.describe()

df_yield.info()

df_rain = pd.read_csv("/content/rainfall.csv")
df_rain.head()

df_rain.shape
df_rain.tail()

df_rain.info()

df_rain["average_rain_fall_mm_per_year"] = pd.to_numeric(df_rain["average_rain_fall_mm_per_year"],errors="coerce")
df_rain.info()

df_rain= df_rain.dropna()

df_rain.describe()

df_yield.columns = df_yield.columns.str.strip()
df_rain.columns = df_rain.columns.str.strip()

print("Columns in df_yield:", df_yield.columns.tolist())
print("Columns in df_rain:", df_rain.columns.tolist())

yield_df = pd.merge(df_yield, df_rain, on=['Area', 'Year'])

yield_df.head()

yield_df.describe()

yield_df.shape

df_pes = pd.read_csv("/content/pesticides.csv")
df_pes.head()

df_pes = df_pes.rename(index=str,columns = {"Value":"pesticides_value"})
df_pes = df_pes.drop(["Element","Domain","Unit","Item"],axis=1)
df_pes.head()

df_pes.describe()

df_pes.info()

yield_df = pd.merge(yield_df , df_pes, on=["Year","Area"])
yield_df.shape

yield_df.head()

avg_temp = pd.read_csv("/content/temp.csv")
avg_temp.head()

avg_temp.describe()

avg_temp = avg_temp.rename(index=str,columns = {"year":"Year","country":"Area"})
avg_temp.head()

yield_df = pd.merge(yield_df,avg_temp, on=["Area","Year"])
yield_df.head()

yield_df.shape

yield_df.describe()

yield_df.isnull().sum()

yield_df.groupby("Item").count()

yield_df.describe()

yield_df["Area"].nunique()

yield_df.groupby(["Area"],sort=True)["hg/ha_yield"].sum().nlargest(10)

yield_df.groupby(["Item","Area"],sort=True)["hg/ha_yield"].sum().nlargest(10)

yield_df.head()

from sklearn.preprocessing import OneHotEncoder
yield_df_onehot = pd.get_dummies(yield_df,columns=["Area","Item"],prefix = ["Country","Item"])
features = yield_df_onehot.drop(columns=["hg/ha_yield"])
target = yield_df_onehot["hg/ha_yield"]

X = features
y = target

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train ,X_test,y_train,y_test = train_test_split(X_scaled,target,test_size=0.2,random_state=42)

reg_model = Sequential([
    Dense(64,activation="relu",input_shape=(X_train.shape[1],)),
    Dense(32,activation="relu"),
    Dense(1)
])

from tensorflow.keras.optimizers import Adam
reg_model.compile(optimizer=Adam(learning_rate=0.01),loss="mean_squared_error")

h_reg = reg_model.fit(X_train,y_train,epochs=50,validation_split=0.2,batch_size=32)

loss_reg = reg_model.evaluate(X_test,y_test)
print("Regression Test Loss",loss_reg)

pred_reg = reg_model.predict(X_test)
print("Regression Predictions",pred_reg[:5])

from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score

mae = mean_absolute_error(y_test,pred_reg)
mse = mean_squared_error(y_test,pred_reg)
rmse = np.sqrt(mse)
r2 = r2_score(y_test,pred_reg)


print("Mean Absoluate Error : ",mae)
print("Mean Squared Error : ",mse)
print("Root Mean Squared Error : ",rmse)
print("R2 Score : ",r2)

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import seaborn as sns

def convert_to_categories(values,bins,labels):
  binned_indices = np.digitize(values,bins,right=True)
  return np.array([labels[ i - 1 ] for i in binned_indices])

predictions_regression = reg_model.predict(X_test).flatten()  # Flatten in case predictions are 2D


bins = [0, 20000, 50000, 100000, 200000]
labels = ['Very Low', 'Low', 'Medium', 'High','Very High']


y_pred_categories = convert_to_categories(predictions_regression, bins, labels)
y_true_categories = convert_to_categories(y_test, bins, labels)

accuracy = accuracy_score(y_true_categories,y_pred_categories)
print("Accuracy OF Regression : ",accuracy)

precision = precision_score(y_true_categories,y_pred_categories,average="weighted")
print("Precision of Regression : ",precision)


recall = recall_score(y_true_categories,y_pred_categories,average="weighted")
print("Recall of Regression : ",recall)

f1 = f1_score(y_true_categories,y_pred_categories,average="weighted")
print("F1 Score of Regression",f1)

cm = confusion_matrix(y_true_categories,y_pred_categories)
print("Confusion Matrix :\n",cm)

plt.figure(figsize=(10,7))
sns.heatmap(cm,annot=True,fmt="d",xticklabels=labels,yticklabels=labels,cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matix For Regression Model")
plt.show()

plt.figure(figsize=(10, 5))
plt.hist(pred_reg, bins=50, alpha=0.75)
plt.title('Histogram of Regression Predictions')
plt.xlabel('Predicted Value')
plt.ylabel('Frequency')
plt.show()

def create_sequences(X,y,sequence_lenght):
  X_seq , y_seq = [],[]
  for i in range(len(X) - sequence_lenght):
    X_seq.append(X[i:i + sequence_lenght])
    y_seq.append(y[i + sequence_lenght])
  return np.array(X_seq),np.array(y_seq)


sequence_lenght = 3
X_seq,y_seq = create_sequences(X_scaled,y.values,sequence_lenght)

X_train_seq,X_test_seq,y_train_seq,y_test_seq = train_test_split(X_seq,y_seq,test_size=0.2,random_state=42)

# Print shapes of training and test sets
print(f'Shape of X_train_seq: {X_train_seq.shape}')
print(f'Shape of X_test_seq: {X_test_seq.shape}')
print(f'Shape of y_train_seq: {y_train_seq.shape}')
print(f'Shape of y_test_seq: {y_test_seq.shape}')

from tensorflow.keras.regularizers import l2
input_shape = (sequence_lenght, 68)
lstm_model = Sequential([
    LSTM(64,activation="relu",input_shape=input_shape,return_sequences=True,kernel_regularizer=l2(0.01)),
    Dropout(0.3),
    LSTM(32,activation="relu",kernel_regularizer=l2(0.01)),
    Dropout(0.3),
    Dense(1)
])

lstm_model.compile(optimizer=Adam(learning_rate=0.001),loss="mean_squared_error")

h_lstm = lstm_model.fit(X_train_seq,y_train_seq,epochs=60,validation_split=0.2,batch_size=64)

loss_lstm = lstm_model.evaluate(X_test_seq,y_test_seq)
print("LSTM Model loss",loss_lstm)

pred_lstm = lstm_model.predict(X_test_seq)
print("LSTM Prediction ",pred_lstm[:5])

mae = mean_absolute_error(y_test_seq,pred_lstm)
print("Mean Absolute Error",mae)

mse = mean_squared_error(y_test_seq,pred_lstm)
print("Mean Squared Error",mse)

rmse_ltsm = np.sqrt(mse)
print("Root Mean Squared Error ",rmse_ltsm)

r2 = r2_score(y_test_seq,pred_lstm)
print("R2 Square ",r2)

def convert_to_categories(values,bins,labels):
  binned_indices = np.digitize(values,bins,right=True)
  return np.array([labels[ i - 1 ] for i in binned_indices])


bins = [0, 20000, 50000, 100000, 200000]
labels = ['Very Low', 'Low', 'Medium', 'High','Very High']

pred_lstm = pred_lstm.flatten()

y_pred_categories = convert_to_categories(pred_lstm,bins,labels)
y_true_categories = convert_to_categories(y_test_seq, bins , labels)


accuracy = accuracy_score(y_true_categories,y_pred_categories)
print("Accuracy OF LSTM : ",accuracy)

precision = precision_score(y_true_categories,y_pred_categories,average="weighted")
print("Precision of LSTM : ",precision)


recall = recall_score(y_true_categories,y_pred_categories,average="weighted")
print("Recall of LSTM : ",recall)

f1 = f1_score(y_true_categories,y_pred_categories,average="weighted")
print("F1 Score of LSTM",f1)

cm_lstm = confusion_matrix(y_true_categories,y_pred_categories)
print("Confusion Matrix for LSTM Model : \n",cm_lstm)

plt.figure(figsize=(10,7))
sns.heatmap(cm_lstm,annot=True,fmt="d",xticklabels=labels,yticklabels=labels,cmap="Reds")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix for LSTM Model ")
plt.show()

plt.figure(figsize=(10, 5))
plt.hist(pred_lstm, bins=50, alpha=0.75)
plt.title('Histogram of LSTM Predictions')
plt.xlabel('Predicted Value')
plt.ylabel('Frequency')
plt.show()

print(f'Shape of pred_reg: {pred_reg.shape}')
print(f'Shape of pred_lstm: {pred_lstm.shape}')
print(f'Shape of y_test: {y_test.shape}')

from sklearn.linear_model import LinearRegression


# Ensure predictions and true values have the same length
min_length = min(len(pred_reg), len(pred_lstm), len(y_test))
pred_reg = pred_reg[:min_length].reshape(-1,1)
pred_lstm = pred_lstm[:min_length].reshape(-1,1)
y_test = y_test[:min_length]

meta_features = np.hstack((pred_reg, pred_lstm))

meta_model = LinearRegression()
meta_model.fit(meta_features, y_test)


Crop_predictions = meta_model.predict(meta_features)

# Convert continuous values into categorical bins
def convert_to_categories(values, bins, labels):
    indices = np.digitize(values, bins=bins, right=True)
    indices = np.clip(indices, 1, len(labels)) - 1  # Clip indices to be within valid range
    return np.array([labels[i] for i in indices])


bins = [0, 20000, 50000, 100000, 200000]
labels = ['Very Low', 'Low', 'Medium', 'High']




y_pred_categories_voting = convert_to_categories(Crop_predictions, bins, labels)
y_true_categories = convert_to_categories(y_test, bins, labels)

Crop_accuracy = accuracy_score(y_true_categories, y_pred_categories_voting)
print("Accuracy of Crop_Yield Model: ",Crop_accuracy)

Crop_precision = precision_score(y_true_categories, y_pred_categories_voting, average='weighted')
print("Precision of Crop_Yield Model: ",Crop_precision)


Crop_recall = recall_score(y_true_categories, y_pred_categories_voting, average='weighted')
print("Recall of Crop_Yield Model: ",Crop_recall)


Crop_f1 = f1_score(y_true_categories, y_pred_categories_voting, average='weighted')
print("F1 Score of Crop_Yield Model: ",Crop_f1)


# Confusion Matrix
Crop_cm = confusion_matrix(y_true_categories, y_pred_categories_voting, labels=labels)
print("Confusion Matrix for Crop_Yield Model:\n", Crop_cm)

plt.figure(figsize=(10, 7))
sns.heatmap(Crop_cm, annot=True, fmt='d', xticklabels=labels, yticklabels=labels, cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix for Crop_Yield Model')
plt.show()

# Plot scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(y_test, Crop_predictions, alpha=0.5, color='b')
plt.xlabel('True Values')
plt.ylabel('Predictions')
plt.title('Scatter Plot of True Values vs. Predictions (Crop_Yield Model)')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='r', linewidth=2)
plt.grid(True)
plt.show()