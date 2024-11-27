from enum import Enum

class MAP_STATES(Enum):
    UNFERTILE_DIRT = { 
            "value" : 0, 
            "color" : (115, 82, 64)
        }
    ROCK = { 
            "value" : 1, 
            "color" : (105, 105, 105)
        }
    WIND_TURBINE = { 
            "value" : 2, 
            "color" : (255, 255, 255)
        }
    PURIFIER = { 
            "value" : 3, 
            "color" : (181, 0, 0)
        }
    FERTILE_DIRT = { 
            "value" : 4, 
            "color" : (133, 51, 8)
        }
    IRRIGATOR = { 
            "value" : 5, 
            "color" : (0, 181, 115)
        }
    GRASS = { 
            "value" : 6, 
            "color" : (0, 235, 12)
        }



class MACHINE_TYPE(Enum):
    WIND_TURBINE = "WIND_TURBINE"
    PURIFIER = "PURIFIER"
    IRRIGATOR = "IRRIGATOR"
