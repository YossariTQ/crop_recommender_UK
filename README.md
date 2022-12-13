# Predictive Knowledge-based Crop Recommendation System (PKBCRS)

-------------------------
CONTENTS OF THIS FILE
-------------------------

* 1. Introduction

* 2. Requirements

* 3. Running the program


-------------------------
1. INTRODUCTION
-------------------------

The PKBCRS provides location-based predictive crop recommendations for small-scale UK farmers.


Alongside this README, in the repository you will find...


	a) Files to run the PKBCRS:

	- main.py 
  - longitude.py
  - latitude.py
  - dialogue.py
  - mongo_connection.py

	- environmental_soil_final.csv (The locational environmental and soil dataset used to extract the features upon which ARIMA was applied to create the 2023 User Profile).

	
-------------------------
2. REQUIREMENTS
-------------------------

To run the KBCRS you will need to download the following:

	- pandas: https://pypi.org/project/pandas/
	
	- numpy: https://numpy.org/install/

	- pymongo: https://pypi.org/project/pymongo/

	- geopy: https://pypi.org/project/pymongo/

	- statsmodels: https://www.statsmodels.org/stable/install.html

	- warnings: https://pypi.org/project/pytest-warnings/


To run the data preparation ipynb files you will also need to download the following (Excluding ones above):

	- xarray: https://pypi.org/project/xarray/
	
	- netCDF4: https://pypi.org/project/netCDF4/

	- geopandas: https://geopandas.org/en/stable/getting_started/install.html


All of which can be installed using Python's de facto package management system: 

	- pip: https://pypi.org/project/pip/


-------------------------
3. RUNNING THE PROGRAM
-------------------------

To run the PKBCRS follow these steps:

	1. Open a terminal window

	2. In the terminal, navigate to the location of the unzipped artefact folder

	3. When in this folder run the program with the commands:
		
		python ./main.py

	4. Follow the menu to run the PKBCRS. Hit y to continue and q to quit.


NOTE: If you experience connection issues with the MongoDB Atlas, this may be because of your VPN settings - this has been noted as an issue on Eduroam Wifi. 

Please use a different wifi or hotspot if you experience this. 



We hope you enjoy the PKBCRS and plant some crops of your own!



