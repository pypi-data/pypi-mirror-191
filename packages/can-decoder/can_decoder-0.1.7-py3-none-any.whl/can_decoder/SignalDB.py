from enum import IntFlag
from typing import Optional, List, Callable

from can_decoder.Frame import Frame
from can_decoder.Signal import Signal


class SignalDBFilterStates(IntFlag):
    KeepSignal = 0x01
    Recurse = 0x02
    

class SignalDB(object):
    def __init__(self, protocol: Optional[str] = None):
        """Create a new signal database, with a pre-defined protocol.
        
        :param protocol: Protocol to associate with the database.
        """
        self._protocol = protocol
        self.frames = {}
        pass
    
    @property
    def protocol(self) -> Optional[str]:
        """Returns the protocol string of the signal database.
        
        :return: The current protocol string of the database.
        """
        return self._protocol
    
    def add_frame(self, frame: Frame) -> bool:
        """Add a CAN frame to the signal database.
        
        :return: True for frame successfully added, False otherwise.
        """
        if frame.id not in self.frames.keys():
            self.frames[frame.id] = frame
            return True
        
        return False
    
    def signals(self, filter_func: Optional[Callable[[Frame,Signal],int]] = None) -> List[str]:
        """Get a list of all signals in the database.
        The list can be filtered with the filter_func argument, where the passed-in function is called for
        each signal with the frame and signal as arguments. Depending on the returned value, based on the flags in
        SignalDBFilterStates, the signal is kept/discarded and further recursion is enabled/disabled.
        
        :filter_func: Optional filter function, which will be called for each Signal.
        :return: List of all signals as strings.
        """
        result = []
        
        if filter_func is None:
            filter_func = self._default_filter_func
        
        def yield_signals(result_list: List[str], frame: Frame, signal: Signal):
            # Test the signal against the filter.
            state = filter_func(frame, signal)
            
            if (state & SignalDBFilterStates.KeepSignal) == SignalDBFilterStates.KeepSignal:
                result_list.append(signal.name)

            if (state & SignalDBFilterStates.Recurse) == SignalDBFilterStates.Recurse:
                if signal.is_multiplexer:
                    for multiplex in signal.signals.values():
                        for sub_signal in multiplex:
                            yield_signals(result_list=result_list, frame=frame, signal=sub_signal)
            return

        for frame in self.frames.values():
            for signal in frame.signals:
                yield_signals(result_list=result, frame=frame, signal=signal)
            
        return result
    
    @staticmethod
    def _default_filter_func(frame: Frame, signal: Signal) -> int:
        return SignalDBFilterStates.KeepSignal | SignalDBFilterStates.Recurse
    
    def __str__(self):
        # Generate a pretty nested tree.
        result = f"SignalDB with {len(self.frames)} frames"

        for frame in self.frames.values():
            frame_str = str(frame)
            
            for line in frame_str.splitlines():
                result += f"\n\t{line}"

        return result
    
    pass
