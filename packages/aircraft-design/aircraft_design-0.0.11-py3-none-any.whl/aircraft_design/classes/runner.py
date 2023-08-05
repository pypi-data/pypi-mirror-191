#!/usr/bin/env python3
import avlwrapper as avl
from configparser import ConfigParser
from aircraft_design.classes.errors import AircraftDesignError
from pathlib import Path
# from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor, as_completed

__config_path__ = Path(__file__).parent.parent.absolute() / 'bin'

__list_bin_path__ = [file for file in __config_path__.iterdir()]

__config_file__ = ConfigParser()

__config_file__['environment'] = {
    'Executable': __config_path__ / 'avl',
    'PrintOutput': 'no',
    'GhostscriptExecutable': 'gs',
    'LogLevel': 'WARNING',
}

__config_file__['output'] = {
    'Totals': 'yes',
    'SurfaceForces': 'yes',
    'BodyForces': 'yes',
    'StripForces': 'yes',
    'ElementForces': 'yes',
    'BodyAxisDerivatives': 'yes',
    'StabilityDerivatives': 'yes',
    'HingeMoments': 'yes',
    'StripShearMoments': 'yes',
}

with open(__config_path__ / 'config.cfg', 'w') as config_file:
    __config_file__.write(config_file)

__cfg_path__ = __config_path__ / 'config.cfg'


class Session(avl.Session):
    def __init__(self, geometry, cases=None, name=None):
        self.config = __cfg_path__
        configuration = avl.Configuration(str(self.config))
        super().__init__(geometry, cases, name, config=configuration)

"""
WIP - Closure para execução de código paralelo
"""
def __closure__(function:callable, *args):
    def inner():
        result = function(*args)
        return result
    return inner

class FunctionRunner:
    def __init__(self, function:callable, args_list:list) -> None:
        self.function = function
        self.args_list = args_list

    def run_all_cases(self, max_workers:int|None=None):
        func_list = []

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            result_list = []
            future_list = []

            for session in self.args_list:
                worker = executor.submit(__Session_Run__, session)
                future_list.append(worker)
            
            for worker in as_completed(future_list):
                result_list.append(worker.result())

"""
WIP - Multiprocessamento de aeronaves
"""
def __Session_Run__(session:Session)->tuple:
    return session.run_all_cases()

class MultiSession:
    def __init__(self, session_array: list[Session]) -> None:
        self.session_array = session_array

    def run_all_cases(self, max_workers:int|None=None):

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            result_list = []
            future_list = []

            for session in self.session_array:
                worker = executor.submit(__Session_Run__, session)
                future_list.append(worker)
            
            for worker in as_completed(future_list):
                result_list.append(worker.result())

        return result_list
