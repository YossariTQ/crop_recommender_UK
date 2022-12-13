"""
IMPORTS including to ignore harmless warnings.

"""
# program modules
import mongo_connection
import dialogue

import pandas as pd
import numpy as np
import pymongo as pm
import geopy.distance
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')


"""
CLASSES

"""

class Latitude():

    def __init__(self):
        self.user_latitude = self.latitudeChecker()
    
    def latitudeChecker(self):       
        while True:
            try:
                self.user_latitude = float(input('\nEnter a UK latitude, that\'s probably between -5 and 2... \n\n'))
            except ValueError:
                print('\nThe provided value is not a number.\n')
                continue
            else:
                print(f'\nYour latitude is: {self.user_latitude}')
                break
        return self.user_latitude


class Longitude():
    
    def __init__(self):
        self.user_longitude = self.longitudeChecker()
    
    def longitudeChecker(self):
        while True:
            try:
                self.user_longitude = float(input('\nEnter a UK longitude, that\'s probably between 49 and 60... \n\n'))
            except ValueError:
                print('\nThe provided value is not a number.\n')
                continue
            else:
                print(f'\nYour latitude is: {self.user_longitude}')
                break
        return self.user_longitude



class UserHistoricData:
    
    ENV_SOIL_DF = pd.read_csv('/Users/jamiemorris/projects/pkbcrs/environmental_soil_final.csv', index_col=[0])
        
    def __init__(self):
        self.input_coords = (Latitude().user_latitude, Longitude().user_longitude)
        self.user_latlong_index = self.calculate_user_latlong_index()
        self.user_historic_df = self.calculate_user_historic_df()
        self.user_historic_latlong = self.calculate_user_historic_latlong()
        print("User Longitude and Latitude: ", self.calculate_user_historic_latlong())
        
    def calculate_user_latlong_index(self):
        dialogue.Dialogue.explain_getting_user_latlong()
        self.user_latlong_index = UserHistoricData.ENV_SOIL_DF.loc[:, 'latlong'].apply(lambda x: geopy.distance.geodesic(self.input_coords, eval(x)).km).argmin()
        return self.user_latlong_index
    
    def calculate_user_historic_df(self):
        self.user_historic_df = UserHistoricData.ENV_SOIL_DF.loc[UserHistoricData.ENV_SOIL_DF['latlong'] == UserHistoricData.ENV_SOIL_DF.loc[self.user_latlong_index]['latlong']]
        return self.user_historic_df
        
    def calculate_user_historic_latlong(self):
        self.user_historic_latlong = self.user_historic_df['latlong'].iloc[0]
        return self.user_historic_latlong


class PredictedUserProfile:
    
    ENV_SOIL_DF = pd.read_csv('/Users/jamiemorris/projects/pkbcrs/environmental_soil_final.csv', index_col=[0])
    
    def __init__(self, user_historic_df):
        dialogue.Dialogue.explain_arima()
        self.user_historic_df = user_historic_df
        self.env_forecasted_dfs, self.environmental_dfs = self.apply_arima()
        
        self.soil_ph = self.get_soil_ph()
        self.soil_group = self.get_soil_group()
        self.tasmax = self.get_tasmax()
        self.tasmin = self.get_tasmin()
        self.sun_hours = self.get_sun_hours()
        self.rainfall = self.get_rainfall()
        
        self.output_user_profile()
        
    def apply_arima(self):
        
        self.environmental_dfs = []
        environmental_features = ['tasmax (c)', 'tasmin (c)', 'sun hours', 'rainfall_m']
        
        for feature in environmental_features: 
            self.environmental_dfs.append(ARIMA(self.user_historic_df[feature], 
                                           order=(1,0,0)).fit().predict(start=len(self.user_historic_df),
                                                                        end=len(self.user_historic_df)+2, 
                                                                        type='levels').to_frame())
        self.env_forecasted_dfs = self.environmental_dfs
        return self.env_forecasted_dfs, self.environmental_dfs
    
    def get_soil_ph(self):
        self.soil_ph = list(PredictedUserProfile.ENV_SOIL_DF['PH_07'])[0]
        return self.soil_ph
    
    def get_soil_group(self):
        self.soil_group = list(PredictedUserProfile.ENV_SOIL_DF['SOIL_GROUP'])[0]
        return self.soil_group
    
    def get_tasmax(self):
        self.tasmax = self.environmental_dfs[0].loc[12][0]
        return self.tasmax
    
    def get_tasmin(self):
        self.tasmin = self.environmental_dfs[1].loc[12][0]
        return self.tasmin
    
    def get_sun_hours(self):
        self.sun_hours = self.environmental_dfs[2].loc[12][0]/274
        return self.sun_hours
    
    def get_rainfall(self):
        self.rainfall = self.environmental_dfs[3].loc[12][0]
        return self.rainfall
    
    def output_user_profile(self):
    
        self.user_profile_2023 = f"""        
    - Average Minimum Air temperature: {self.tasmin}\u00B0C 
    - Average Maximum Air temperature: {self.tasmax}\u00B0C
    - Rainfall: {self.rainfall}mm
    - Average sun hours per day: {self.sun_hours} hours
    - Soil pH: {self.soil_ph}
    - Soil Type: {self.soil_group}

"""
        print(self.user_profile_2023)    


class KnowledgeDatabaseQuery:
    
    def __init__(self, mongo_database, mongo_collection, tasmin, tasmax, rainfall, sun_hours, soil_ph, soil_group):
        
        self.tasmin = tasmin
        self.tasmax = tasmax
        self.rainfall = rainfall
        self.sun_hours = sun_hours
        self.soil_ph = soil_ph
        self.soil_group = soil_group
        
        self.mong_uri = 'mongodb://kbcrs:yorkirp@ac-xib4iiz-shard-00-00.u4ryiau.mongodb.net:27017,ac-xib4iiz-shard-00-01.u4ryiau.mongodb.net:27017,ac-xib4iiz-shard-00-02.u4ryiau.mongodb.net:27017/?ssl=true&replicaSet=atlas-fy2az9-shard-0&authSource=admin&retryWrites=true&w=majority'
        
        self.pkbcrs_connection = mongo_connection.MongoConnection(self.mong_uri, mongo_database, mongo_collection)
        self.crop_recommendations_list = self.KB_query()
        self.output_crop_recommendations()
         
    def KB_query(self):
        
        self.crop_recommendations_list = []
                
        for crop in self.pkbcrs_connection.cropsCollection.find({"Viable_Air_Temp_Min": {"$lte": self.tasmin}, 
                                "Viable_Air_Temp_Max":{"$gte": self.tasmax},
                                "Viable_Rain_Min":{"$lte": self.rainfall},
                                "Viable_Rain_Max":{"$gte": self.rainfall},
                                "Viable_Sun_Min":{"$lte": self.sun_hours},
                                "Viable_Sun_Max":{"$gte": self.sun_hours},
                                "Viable_PH_Min":{"$lte": self.soil_ph},
                                "Viable_PH_Max":{"$gte": self.soil_ph},
                                "Viable_Soil_Type":{"$regex": ".*" + self.soil_group + ".*"}
                              }):
        

            viable_crop_recommendation_text = f"""{crop["Crop"]} ({crop["Latin_Name"]}) can be grown in your location. 
        
    - Have a viable air temperature range of {crop["Viable_Air_Temp_Min"]}\u00B0C to {crop["Viable_Air_Temp_Max"]}\u00B0C. 
    - Have a viable soil pH range is {crop["Viable_PH_Min"]}pH to {crop["Viable_PH_Max"]}pH.
    - Require at least {crop["Viable_Rain_Min"]}mm rainfall per year, with a maximum tolerance of {crop["Viable_Rain_Max"]}mm.
    - Require between {crop["Viable_Sun_Min"]} and {crop["Viable_Sun_Max"]} sun hours per day.    
    
    """
         
            self.crop_recommendations_list.append(viable_crop_recommendation_text)
        
        return self.crop_recommendations_list
    
    def output_crop_recommendations(self):
        
        for recommended_crop in self.crop_recommendations_list: print(recommended_crop)


class PKBCRS:
    
    def __init__(self):
        
        dialogue.Dialogue.introduction()
        self.program_controller() 

    def program_controller(self):
        
        ans = True
        while ans:            
            ans=input("\n\nUse Crop Recommendation System (y) / Quit (q)\n\n")
            if ans=="y":
                user_profile = PredictedUserProfile(UserHistoricData().user_historic_df)
                KnowledgeDatabaseQuery('crop_properties', 'cropsCollection', user_profile.tasmin, user_profile.tasmax,
                          user_profile.rainfall, user_profile.sun_hours, user_profile.soil_ph, user_profile.soil_group)
                dialogue.Dialogue.outro()
            elif ans=="q":
                dialogue.Dialogue.goodbye()
                break
            else:
                print("\n Not Valid Choice Try again") 


PKBCRS()