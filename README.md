# Wind Power Prediction


This project uses publicly available weather and wind farm data to make a forecast model for wind power prediction. The weather data is provided by Dark Sky, and the power data is from the Australian Renewable Energy Mapping Infrastructure Project (AREMI).

This work is primarily done on Google Cloud Platform on a N1 virtual machine with 4 vCPUs, 15 GB RAM, and a NVIDIA Tesla K80 GPU. However, most moderately-speced personal computers should be able to run the models.

You can view a live web app that uses the XGBoost models to make hourly power forecast with real-time weather data for all major wind farms in South Australia [here](https://wpp-hw.herokuapp.com/).
