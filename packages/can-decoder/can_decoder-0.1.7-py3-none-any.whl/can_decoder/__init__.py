from can_decoder.exceptions import *
from can_decoder.iterator import IteratorDecoder, DecodedSignal
from can_decoder.warnings import *

from can_decoder.Frame import Frame
from can_decoder.Signal import Signal
from can_decoder.SignalDB import SignalDB

try:
    from can_decoder.dataframe import DataFrameDecoder
except ModuleNotFoundError:
    pass


import logging


# Disable warnings in logs temporarily for canmatrix
canmatrix_logger = logging.getLogger("canmatrix")
previous_level = canmatrix_logger.getEffectiveLevel()
canmatrix_logger.setLevel(logging.ERROR)

try:
    from can_decoder.DBCLoader import load_dbc
except ModuleNotFoundError:
    pass
finally:
    canmatrix_logger.setLevel(previous_level)
    canmatrix_logger = None
    previous_level = None
