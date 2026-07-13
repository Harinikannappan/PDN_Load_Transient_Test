import pyvisa
from config import PSU, LOAD, SCOPE, DMM

class InstrumentManager:

    def __init__(self):

        rm = pyvisa.ResourceManager()

        self.psu = rm.open_resource(PSU)
        self.load = rm.open_resource(LOAD)
        self.scope = rm.open_resource(SCOPE)
        self.dmm = rm.open_resource(DMM)

        for inst in [self.psu, self.load, self.scope, self.dmm]:
            inst.timeout = 10000  # ms -- waveform transfers can be slow

    def initialize(self):

        for inst in [self.psu,self.load,self.scope,self.dmm]:
            inst.write("*RST")
            inst.write("*CLS")

    def close(self):

        for inst in [self.psu, self.load, self.scope, self.dmm]:
            try:
                inst.close()
            except Exception as e:
                print(f"Warning: failed to close instrument: {e}")
