class Dialogue:
    
    def __init__(self):
        pass  
    

    @staticmethod
    def introduction():
        
        print('\n------------------------------------------------\n')

        opening_spiel = (f"""Welcome to the Knowledge Based Crop Recommendation System!

We use location based timeseries forecasting to recommend viable crops for the 2023 growing season.

You will be asked to enter your longitude and latitude as your location.

------------------------------------------------
""")
        print(opening_spiel)

    @staticmethod
    def explain_getting_user_latlong():
        
        print('\n------------------------------------------------\n')

        
        get_user_latlong_spiel = """We now need to locate the nearest 1km squared within our locational database.

Each location has 10 years of air temperature, rainfall and sunlight hours data, which is combined with 2007 soil pH and soil type data.

Individual datasets are available from the MetOffice and UKCEH. Please see the documentation for more detail.

This shouldn't take long...

------------------------------------------------

    """
        print(get_user_latlong_spiel)
        
        
    @staticmethod
    def explain_user_latlong_retrieved():
        
        print('\n------------------------------------------------\n')

        
        retrieved_user_latlong_spiel = """We have retrieved your nearest location within the Environmental & Soil Dataset. 

10 years of data from this location is used to predict the growing conditions for the 2023 growing season. 
    """
        print(retrieved_user_latlong_spiel)
        
    
    @staticmethod
    def explain_arima():
        
        print('\n------------------------------------------------\n')
        
        retrieved_user_latlong_spiel = """The ARIMA function predicts the following 2023 User Profile for your location.
    """
        print(retrieved_user_latlong_spiel)
        
    
    @staticmethod
    def outro():
        
        print('\n------------------------------------------------\n')
        
        retrieved_user_latlong_spiel = """^^^^^ Scroll up to see your recommendations ^^^^^

............................................................................
............................................................................
    """
        print(retrieved_user_latlong_spiel)
    
    @staticmethod
    def goodbye():
        
        print('\n------------------------------------------------\n')
        
        retrieved_user_latlong_spiel = """
Thanks for using the Knowledge-based Crop Recommendation System, version 2.0 .\n    

"""
        print(retrieved_user_latlong_spiel)

