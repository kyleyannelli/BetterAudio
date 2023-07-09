from pedalboard import Pedalboard, Compressor, Gain, NoiseGate
from pedalboard.io import AudioStream
import signal
import sys
import time

# Create a variable to store if we're currently running or not
running = True

def stop_running(signal, frame):
  """Stop the program when a SIGINT signal is received"""
  global running
  running = False
  print("Received signal to stop running")

# Register the stop_running function to be called on SIGINT
signal.signal(signal.SIGINT, stop_running)

def start_stream():
  # Open up an audio stream:
  with AudioStream(
      input_device_name="Scarlett Solo USB", # Use SM57 via Scarlett 
      output_device_name="BlackHole 2ch" # Output to BlackHole so it can be used on things like OBS & Discord
    ) as stream:
      stream.plugins = Pedalboard([
        NoiseGate(threshold_db=-45, ratio=4, attack_ms=1.0, release_ms=100.0),
        Compressor(threshold_db=-20, ratio=4, attack_ms=10, release_ms=200),
        Gain(gain_db=20),
        Compressor(threshold_db=-10, ratio=4, attack_ms=10, release_ms=200),
      ])

      print("Starting loop")  # Debug print

      while running:
        # Just sleep for a bit to prevent this loop from using too much CPU
        time.sleep(1)


def start_stream_exceptionally():
  try:
    start_stream()
  except:
    print("Couldn't find the devices, retrying in 5 seconds")
    time.sleep(5)
    start_stream_exceptionally()

start_stream_exceptionally()

