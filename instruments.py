import pyvisa

class InstrumentManager:

    def __init__(self):

        rm = pyvisa.ResourceManager()

        self.psu = rm.open_resource("USB0::0x05E6::0x2230::1234567::INSTR")
        self.load = rm.open_resource("USB0::0x05E6::0x2380::7654321::INSTR")
        self.scope = rm.open_resource("USB0::0x2A8D::0x1766::MY12345678::INSTR")
        self.dmm = rm.open_resource("USB0::0x05E6::0x6500::9876543::INSTR")

    def initialize(self):

        for inst in [self.psu,self.load,self.scope,self.dmm]:
            inst.write("*RST")
            inst.write("*CLS")

    def close(self):

        self.psu.close()
        self.load.close()
        self.scope.close()
        self.dmm.close()