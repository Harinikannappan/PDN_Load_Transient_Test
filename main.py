import csv
import os
import time
from datetime import datetime

import pandas as pd

from config import *
from instruments import InstrumentManager
from report import generate_statistics


os.makedirs("results/csv",exist_ok=True)
os.makedirs("results/waveforms",exist_ok=True)

manager = InstrumentManager()
manager.initialize()

psu = manager.psu
load = manager.load
scope = manager.scope
dmm = manager.dmm

print("Power Supply Configuration")

psu.write("VOLT 5")
psu.write("CURR 3")
psu.write("OUTP ON")

scope.write(":AUToscale")

csv_file = "results/csv/TestResults.csv"

header = [
    "Timestamp",
    "Rail",
    "Voltage",
    "Ripple",
    "Status"
]

with open(csv_file,"w",newline="") as file:

    writer = csv.writer(file)
    writer.writerow(header)

    for rail,data in RAILS.items():

        print(f"Testing {rail}")

        max_current = data["current"]

        low_load = 0.1 * max_current
        high_load = 0.9 * max_current

        load.write("MODE CC")

        load.write(f"CURR {low_load}")

        time.sleep(1)

        load.write(f"CURR {high_load}")

        time.sleep(1)

        voltage = float(dmm.query("MEAS:VOLT?"))

        ripple = float(scope.query(":MEASure:VRMS?"))

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        voltage_limit_low = data["voltage"]*(1-VOLTAGE_TOLERANCE)
        voltage_limit_high = data["voltage"]*(1+VOLTAGE_TOLERANCE)

        status = "PASS"

        if voltage < voltage_limit_low:
            status="FAIL"

        if voltage > voltage_limit_high:
            status="FAIL"

        if ripple > MAX_RIPPLE:
            status="FAIL"

        image_name = f"results/waveforms/{rail}_{datetime.now().strftime('%H%M%S')}.png"

        scope.write(":DISPLAY:DATA? PNG")

        with open(image_name,"wb") as image:
            image.write(scope.read_raw())

        writer.writerow([
            timestamp,
            rail,
            voltage,
            ripple,
            status
        ])

        print(status)

psu.write("OUTP OFF")
load.write("INPUT OFF")

generate_statistics(csv_file)

manager.close()

print("Testing Completed")