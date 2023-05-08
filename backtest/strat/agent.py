# LOCAL IMPORTS
from settings.settings import settings

# ---------------------------------------------------------------
"""
CREATING A STATE MACHINE TO MODEL THE MARKET


"""
# ---------------------------------------------------------------

class State:
    def __init__(self, _settings:settings) -> None:
        self.settings = _settings
        self.change_conditions = []

    def __str__(self):
        return self.settings['name']

class Statechange:
    def __init__(self, from_state:State, to_state:State, condition_settings:settings, verbose:bool = True) -> None:
        self.from_state = from_state
        self.to_state = to_state
        self.settings = condition_settings
        self.verbose = verbose

    def __str__(self):
        return f"STATECHANGE FROM: {self.from_state} -> TO: {self.to_state} - NAME: {self.settings['name']}"


    def check_change(self) -> bool:
        ret_data = self.settings['func_name']

class Agent:
    def __init__(self, _settings:settings, verbose:bool = True) -> None:
        self.states = {}
        self.settings = _settings
        self.attention = None
        self.verbose = verbose
    
    def add_state(self, _state:State):
        self.states[_state.settings['name']] = _state
