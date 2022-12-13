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