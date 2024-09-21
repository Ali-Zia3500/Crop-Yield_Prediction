# Crop-Yield_Prediction
This project focuses on predicting crop yield using machine learning models, specifically a Regression Model, an LSTM Model, and a Voting Model that combines the two. The models are trained and evaluated using datasets containing features like Area, Item, Year, Yield, and various environmental factors.

Features
Area: The region where the crop is cultivated (e.g., India, Pakistan, etc.).
Item: The type of crop.
Year: The year of cultivation.
hg/ha_yield: Yield per hectare.
average_rain_fall_mm_per_year: Annual rainfall.
pesticides_value: Value of pesticides used.
avg_temp: Average temperature.

Models Used

Regression Model: Predicts yield using regression techniques.

LSTM Model: A sequential model used for time series prediction.

Voting Model: Combines the predictions from both regression and LSTM models for improved accuracy.

Results:

Accuracy OF Regression :  0.9022956326987682

Precision of Regression :  0.903207406976877

Recall of Regression :  0.9022956326987682

F1 Score of Regression 0.9022862193473783

LONG SHORT-TERM MEMORY(LSTM):

Accuracy OF LSTM :  0.704284514141697

Precision of LSTM :  0.7268358979983076

Recall of LSTM :  0.704284514141697

F1 Score of LSTM 0.7065498949645639

Accuracy of Crop_Yield Model:  0.9120694483338001

Precision of Crop_Yield Model:  0.911996995039719

Recall of Crop_Yield Model:  0.9120694483338001

F1 Score of Crop_Yield Model:  0.9117896803860732


Project Structure
Crop_Yield_Prediction.ipynb: The main notebook where the models are implemented and trained.
datasets/: Contains the following datasets:

pesticides.csv

rainfall.csv

temp.csv

yield.csv


Instructions for Running the Project

Open the notebook in Google Colab or locally.

Ensure the datasets are in the correct directory.

Run each cell in the notebook to see the model training, evaluation, and results.
