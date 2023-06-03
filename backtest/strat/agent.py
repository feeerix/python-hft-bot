# IMPORTS
import pandas as pd

# LOCAL IMPORTS
from settings.settings import settings

# ---------------------------------------------------------------
"""
CREATING A STATE MACHINE TO MODEL THE MARKET


"""
# ---------------------------------------------------------------

class Position:
    def __init__(self, _settings:settings, verbose:bool = False) -> None:
        pass

    def change_size(self, time:int, increase:bool, size:int, entry:int) -> None:
        pass

    def close(self, time:int) -> None:
        pass

class Condition:
    def __init__(self, _settings:settings, verbose:bool = False):
        self.condition_func = _settings

class State:
    def __init__(self, name:str, description:str, _statechanges:list, _settings:settings, current:bool = False, verbose:bool = False) -> None:
        self.settings = _settings
        self.verbose=verbose
        self.description = description
        self.statechanges = _statechanges
        self.current = current
        self.name = name
        self.count = 0

    def __str__(self):
        return f"STATE: {self.settings['name']}"
    
    def check_state(self, time:int, verbose:bool=False) -> bool:
        for state in self.statechanges:
            state.check_change()

class Statechange:
    def __init__(self, name:str, description:str, from_state:State, to_state:State, condition_settings:settings, verbose:bool = True) -> None:
        self.from_state = from_state
        self.to_state = to_state
        self.settings = condition_settings
        self.verbose = verbose
        self.description = description
        self.name = name
        self.count = 0
        

    def __str__(self):
        return f"TRANSITION FROM: {self.from_state} -> TO: {self.to_state} - NAME: {self.settings['name']}"

    def check_change(self, df:pd.DataFrame) -> bool:
        
        
        return self.settings['func_name'](**self.settings['arguments'])

class Agent:
    def __init__(self, _settings:settings, verbose:bool = True) -> None:
        self.states = {}
        self.settings = _settings
        self.attention = None
        self.verbose = verbose
        self.current_state = None
    
    def add_state(self, _state:State):
        self.states[_state.settings['name']] = _state

    def setState(self):
        pass
    
    def monitor(self):
        pass


