#!/usr/bin/env python3
import subprocess
subprocess.run(["python3", "dash/app.py"])  # doesn't capture output
subprocess.run(["python3", "mqtt/mqttinfoscraper.py"])  # doesn't capture output
subprocess.run(["python3", "mqtt/mqttdatatoinfluxdb.py"])  # doesn't capture output
