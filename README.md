# PDN Automated Load Transient Test

## Hardware

- Keithley 2230 PSU
- Keithley 2380 Electronic Load
- Keysight DSOX6004A
- Keithley DMM6500

## Software

Python 3.11

PyVISA

## Features

- Automatic Instrument Initialization
- Load Transient Testing (repeated captures per rail, configurable in config.py)
- Raw Waveform Capture (per capture, saved as CSV for later analysis)
- Peak Deviation & Settling Time Calculation
- CSV Logging
- Pass / Fail Evaluation
- Per-Rail Statistics & Report Generation

## Assumptions

Load transient test parameters are not specified in the source Annexure and are
assumed in `config.py`:
- Load step 10% -> 90% of each rail's rated max current
- 10 captures per rail
- Pass criteria: peak deviation <=5% of nominal, settling time <=500us
  (to within +/-1% of nominal)

These should be replaced with the actual program specification before use on
real hardware.

## Folder Structure

results/

- csv/
- waveforms/
- reports/

## Run

```bash
pip install -r requirements.txt
python main.py
```
