import csv
import os
import time
from datetime import datetime

import pandas as pd

from config import *
from instruments import InstrumentManager
from report import generate_statistics


os.makedirs("results/csv", exist_ok=True)
os.makedirs("results/waveforms", exist_ok=True)
os.makedirs("results/reports", exist_ok=True)

manager = InstrumentManager()
manager.initialize()

psu = manager.psu
load = manager.load
scope = manager.scope
dmm = manager.dmm


def analyze_waveform(times, volts, vnom):
    """Return v_min, v_max, peak deviation %, settling time (s or None)."""
    v_min = min(volts)
    v_max = max(volts)
    dev_pct = max(abs(vnom - v_min), abs(v_max - vnom)) / vnom * 100

    band = vnom * SETTLE_BAND_PCT / 100
    step_idx = None
    for i, v in enumerate(volts):
        if abs(v - vnom) > band:
            step_idx = i
            break

    settle_s = None
    if step_idx is not None:
        for i in range(step_idx, len(volts)):
            if abs(volts[i] - vnom) <= band and all(
                abs(v - vnom) <= band for v in volts[i:i + 20]
            ):
                settle_s = times[i] - times[step_idx]
                break

    return v_min, v_max, dev_pct, settle_s


csv_file = "results/csv/TestResults.csv"

header = [
    "Timestamp",
    "Rail",
    "Capture",
    "V_min",
    "V_max",
    "Deviation_pct",
    "SettlingTime_us",
    "Status"
]

try:
    print("Power Supply Configuration")

    psu.write("VOLT 5")
    psu.write("CURR 3")
    psu.write("OUTP ON")
    time.sleep(1)  # let the PGOOD daisy chain fully sequence up

    with open(csv_file, "w", newline="") as file:

        writer = csv.writer(file)
        writer.writerow(header)

        for rail, data in RAILS.items():

            print(f"Testing {rail}")

            vnom = data["voltage"]
            max_current = data["current"]
            channel = data["channel"]

            low_load = 0.1 * max_current
            high_load = 0.9 * max_current

            # arm the scope on this rail's channel
            scope.write(f":CHANnel{channel}:DISPlay ON")
            scope.write(f":CHANnel{channel}:COUPling AC")
            scope.write(f":CHANnel{channel}:BWLimit ON")
            scope.write(f":TRIGger:EDGE:SOURce CHANnel{channel}")
            scope.write(":TRIGger:SWEep NORMal")

            load.write("MODE CC")
            load.write(f"CURR {low_load}")
            time.sleep(0.3)

            for cap in range(1, CAPTURES_PER_RAIL + 1):

                scope.write(":DIGitize")           # arm single acquisition
                load.write(f"CURR {high_load}")     # trigger the transient step
                time.sleep(0.05)                     # allow the capture to complete

                scope.write(f":WAVeform:SOURce CHANnel{channel}")
                scope.write(":WAVeform:FORMat ASCII")
                raw = scope.query(":WAVeform:DATA?")
                volts = [float(v) for v in raw.strip().split(",") if v]
                xinc = float(scope.query(":WAVeform:XINCrement?"))
                times = [i * xinc for i in range(len(volts))]

                v_min, v_max, dev_pct, settle_s = analyze_waveform(times, volts, vnom)

                status = "PASS"
                if dev_pct > MAX_DEVIATION_PCT:
                    status = "FAIL"
                if settle_s is None or settle_s > MAX_SETTLE_TIME_S:
                    status = "FAIL"

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                settle_us = "N/A" if settle_s is None else f"{settle_s * 1e6:.1f}"

                # raw waveform per capture -- needed to recompute deviation /
                # settling time later; a screenshot alone isn't analyzable
                wf_name = f"results/waveforms/{rail}_cap{cap:02d}_{datetime.now().strftime('%H%M%S')}.csv"
                with open(wf_name, "w", newline="") as wf:
                    wf_writer = csv.writer(wf)
                    wf_writer.writerow(["time_s", "voltage_v"])
                    wf_writer.writerows(zip(times, volts))

                writer.writerow([
                    timestamp,
                    rail,
                    cap,
                    f"{v_min:.4f}",
                    f"{v_max:.4f}",
                    f"{dev_pct:.2f}",
                    settle_us,
                    status
                ])

                print(f"  capture {cap:02d}/{CAPTURES_PER_RAIL}: "
                      f"dev={dev_pct:.2f}% settle={settle_us}us -> {status}")

                load.write(f"CURR {low_load}")  # return to low before next capture
                time.sleep(0.3)

            load.write("INPUT OFF")

    generate_statistics(csv_file)

finally:
    psu.write("OUTP OFF")
    load.write("INPUT OFF")
    manager.close()
    print("Testing Completed")
