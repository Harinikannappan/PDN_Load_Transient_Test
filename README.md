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
- Load Transient Testing
- Voltage Measurement
- Ripple Measurement
- Oscilloscope Screenshot Capture
- CSV Logging
- Pass / Fail Evaluation
- Statistics Generation

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
