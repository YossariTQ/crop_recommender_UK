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
