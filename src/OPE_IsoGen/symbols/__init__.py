from .builtin.dummy_symbol import DummySymbol  # existing
from .builtin.straight_pipe import StraightPipeSymbol, StraightPipeParams

# Simple in-memory registry; keys are case-insensitive here
_SYMBOLS = {
    "dummy": DummySymbol,
    "straightpipe": StraightPipeSymbol,
}

def get_symbol_class(name: str):
    if not name:
        return None
    return _SYMBOLS.get(name.lower())