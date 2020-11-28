# -*- coding: utf-8 -*-
""" UHD TX example for arbitrary ASCII text
"""

__author__ = "Igor Kim"
__credits__ = ["Igor Kim"]
__maintainer__ = "Igor Kim"
__email__ = "igor.skh@gmail.com"
__status__ = "Development"
__date__ = "11/2020"
__license__ = ""

import random
import uhd
import time
import numpy as np
import pyfiglet

from commpy.sequences import zcsequence


def figlet_to_array(in_str):
    result = pyfiglet.figlet_format(in_str, font="banner")
    result_str = str(result).split("\n")
    res = []
    for s in result_str:
        line = [c != " " for c in s]
        res.append(line)
    res.reverse()
    return res


def mod_am(t, freq, amp=.05):
    return amp*np.exp(2j*np.pi*freq*t)


def rand_am(t, bw, n=2, amp=.05):
    res = 0
    for i in range(n):
        freq = np.random.randint(0, bw)
        res += .05*np.exp(2j*np.pi*freq*t)
    return res


def ascii_to_freq(text, n_samples, freq_list, t, amp=.05):
    s_print = figlet_to_array(text)
    samples_buffer = np.zeros((len(s_print), n_samples), dtype=np.complex64)
    for i, line in enumerate(s_print):
        amp = .04
        for j, char in enumerate(line):
            # if j % 5 == 0:
            #     amp += .02
            if char and j < len(freq_list):
                samples_buffer[i] += mod_am(t, freq_list[j], amp)
        samples_buffer[i] *= np.hamming(n_samples)

    return samples_buffer


def ascii_text(text, n_samples, freq_list, t):
    samples_buffer = None
    text = text.split("\n")
    text.reverse()
    for s in text:
        res = ascii_to_freq(s, n_samples, freq_list, t)
        if samples_buffer is None:
            samples_buffer = res
        else:
            samples_buffer = np.concatenate((samples_buffer, res), axis=0)
    return samples_buffer


addr = "192.168.11.2"
rate = 5e6
wave_freq = 500e3
gain = 0
channels = [0]
freq = 900e6
period = .05
modulation_index = 1
freq_spacing = 20e3
bw = 250e3

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
n_cols = int(bw*2 / freq_spacing)
freq_list = np.arange(int(-bw), int(bw), int(freq_spacing))

t = np.linspace(0, duration, n_samples, dtype=np.complex64)

buffer_term = mod_am(t, -620e3)
buffer0 = np.zeros(n_samples)

screens = []
# for i in range(11):
#     screens.append((ascii_text(
#         str(10-i)+"\n"*12, n_samples, freq_list, t), 1.))
screens.append((ascii_text(
    "PSS\n\nPSS\n\nPSS\n\nPSS", n_samples, freq_list, t), 1.))
# screens.append((ascii_text(
#     "Hello\nHTWK\nI am\nASCII", n_samples, freq_list, t), 2.))
# screens.append((ascii_text(
#     "Agile\nRadio\nLab\n" + "\n"*7, n_samples, freq_list, t), 2.))

metadata = uhd.types.TXMetadata()
metadata.start_of_burst = False
metadata.end_of_burst = False
metadata.has_time_spec = False

running = True
smps = 0

block_size_ms = (max_num_samples / rate) * 1e3
screen_size_ms = 40
n_screen = int(screen_size_ms/block_size_ms)
min_detect = int(np.ceil(1 / block_size_ms))

step = 0
screen_id = 0

samples_buffer = screens[screen_id][0]
while running:
    try:
        for i in range(int(n_screen)):
            if i % min_detect == 0:
                if step < len(samples_buffer):
                    streamer.send(samples_buffer[step], metadata)
                else:
                    streamer.send(buffer0, metadata)
                step += 1
            else:
                streamer.send(buffer0, metadata)
        for i in range(int(n_screen/4)):
            streamer.send(buffer_term, metadata)
        start_time = time.time()
        while time.time() - start_time < screens[screen_id][1]:
            streamer.send(buffer0, metadata)

        screen_id += 1
        if screen_id == len(screens):
            screen_id = 0
        samples_buffer = screens[screen_id][0]
        step = 0
    except KeyboardInterrupt:
        running = False
        print("Exiting...")
