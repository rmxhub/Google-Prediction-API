# PredictAPI
This project is prepared by Rongmin Xia .

There ares three files: readme.md, googlepredapil.py, and resultanalysis.pdf

This dataset has five columns, “Temp3pm,Cloud3pm,WindSpeed3pm,Pressure3pm,Date”. First column is the temperature which will be used as prediction term. 

Since the temperature at 3 PM of certain day is affected by weather, cloud, atm pressure, and date, it can predicted within certain range based on 

necessary information.

Research step:

1.	Split data to training and test dataset. Currently, only 20 data are in the test dataset, because it is a demo.

2.	Upload the training dataset to google cloud storage

3.	Training the data using the google prediction tool

4.	In local computer, we write a python code to send the test data to google and obtain the predict value.

5.	Comparing the actual temperature and predicted temperature, and make a conclusion 
    for result obtained from Google prediction API.
