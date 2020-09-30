class Worm:
    def __init__(self, id, coordinates, luciferin, adaptation, coveredSet, intradistance):
        self.id = id
        self.coordinates = coordinates
        self.luciferin = luciferin
        self.adaptation = adaptation
        self.coveredSet = None
        self.intradistance = intradistance
        
    def __str__(self):
        return (f"Worm:"
            f"Coordinates: {self.coordinates}"
            f"Luciferin: {self.luciferin}"
            f"Adaptation (F): {self.adaptation}"
            f"Covered data set: {self.coveredSet}"
            f"Intradistance: {self.intradistance}")
