# VISA Addresses

PSU = "USB0::0x05E6::0x2230::1234567::INSTR"
LOAD = "USB0::0x05E6::0x2380::7654321::INSTR"
SCOPE = "USB0::0x2A8D::0x1766::MY12345678::INSTR"
DMM = "USB0::0x05E6::0x6500::9876543::INSTR"

INPUT_VOLTAGE = 5.0

RAILS = {
    "3V6": {"voltage":3.6,"current":2.5},
    "3V3": {"voltage":3.3,"current":3.0},
    "2V5": {"voltage":2.5,"current":1.5},
    "1V8": {"voltage":1.8,"current":3.0}
}

VOLTAGE_TOLERANCE = 0.05
MAX_RIPPLE = 0.05