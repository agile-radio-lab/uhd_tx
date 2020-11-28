# -*- coding: utf-8 -*-
""" UHD TX example for amplitude modulation
"""

__author__ = "Igor Kim"
__credits__ = ["Igor Kim"]
__maintainer__ = "Igor Kim"
__email__ = "igor.skh@gmail.com"
__status__ = "Development"
__date__ = "101/2020"
__license__ = ""


import random
import uhd
import time
import numpy as np


def mod_am(t, freq, amp=.05):
    return amp*np.exp(2j*np.pi*freq*t)


addr = "192.168.11.2"
rate = 5e6
wave_freq = 500e3
gain = 0
channels = [0]
freq = 900e6
modulation_index = 1

st_args = uhd.usrp.StreamArgs("fc32", "sc16")

usrp = uhd.usrp.MultiUSRP("addr=%s" % addr)
usrp.set_tx_rate(rate, 0)
usrp.set_tx_freq(uhd.types.TuneRequest(freq), 0)
usrp.set_tx_gain(gain, 0)

streamer = usrp.get_tx_stream(st_args)
max_num_samples = streamer.get_max_num_samps()
print("Max samples: %d" % max_num_samples)
n_samples = max_num_samples
duration = n_samples / rate

t = np.linspace(0, duration, n_samples, dtype=np.complex64)

metadata = uhd.types.TXMetadata()
metadata.start_of_burst = False
metadata.end_of_burst = False
metadata.has_time_spec = False

running = True
smps = 0


step = 0
screen_id = 0

samples_buffer = mod_am(t, 100e3) + mod_am(t, -50e3)
while running:
    try:
        streamer.send(samples_buffer, metadata)
    except KeyboardInterrupt:
        running = False
        print("Exiting...")
