

class Graphinfo:

    def __init__(self, measurement, where_time_range=None):

        self.measurement = measurement
        self.where_time_range = where_time_range

    def setmeasurement(self,measurement):
        self.measurement = measurement
        
    def getmeasurement(self):
        return self.measurement