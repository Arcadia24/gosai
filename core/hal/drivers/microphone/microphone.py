import json
import math
from core.hal.drivers.driver import BaseDriver
import sounddevice as sd
import queue
import numpy as np
from os import path


import sounddevice as sd
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

class Driver(BaseDriver):
    def __init__(self, name: str, parent):
        super().__init__(name, parent)
        
        # create driver event
        self.create_event("audio_stream")


    def pre_run(self):
        # runs to do at the start of the driver
        BLOCKSIZE = 1024  # TODO:read these parameters from config.json
        SAMPLERATE = 48000

        if path.exists("home/config.json"):
            with open("home/config.json", "r") as f:
                config = json.load(f)
                if ("channels_nb" in config["microphone"]):
                    CHANNELS = config["microphone"]["channels_nb"]
        
                if ("number" in config["microphone"]):
                    DEVICE = config["microphone"]["number"]
        
        else: 
            CHANNELS = 1
            DEVICE = 6

        if path.exists("home/config.json"):
            with open("home/config.json", "r") as f:
                config = json.load(f)
                CHANNELS = config["microphone"]["channels_nb"] if ("channels_nb" in config["microphone"]) else 1

                if ("number" in config["microphone"]):
                    DEVICE = config["microphone"]["number"]
        
        else: 
            CHANNELS = 1
            DEVICE = 6

        def callback(indata, frames, time, status):
            self.set_event_data(
                "audio_stream",
                {
                    "block": indata,
                    "samplerate": SAMPLERATE,
                },
            )
        stream = sd.InputStream(
            samplerate=SAMPLERATE,
            blocksize=BLOCKSIZE,
            callback=callback,
            channels=CHANNELS,
            device=DEVICE,
        )

        stream.start()
