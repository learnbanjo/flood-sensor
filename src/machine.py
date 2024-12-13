# this is a mock of the machine module for micropython
class ADC:
    def __init__(self, pin):
        self.pin = pin
        print(f"ADC({pin})")
    
    def read(self):
        return self.pin

class Pin:
    IN = 0
    PULL_UP = 1

    def __init__(self, pin, mode, pull):
        self.pin = pin
        self.mode = mode
        self.pull = pull
        print(f"Pin({pin}, {mode}, {pull})")
    
    def value(self):
        return self.pin
        
def reset():
    print("Resetting the device")
    pass