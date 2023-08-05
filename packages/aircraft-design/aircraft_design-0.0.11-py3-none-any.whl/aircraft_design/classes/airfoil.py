import pickle
from pathlib import Path
from numpy import loadtxt

"""
WIP - TUDO AINDA
"""
class Airfoil:
    def __init__(self, name:str, airfoil_path:Path, Re:tuple = (400e3, 1_000e3), resolution: int=10):
        
        self.__airfoil = loadtxt(airfoil_path)
        self.__Re = Re
        self.__resol = resolution

        ...
    
    
