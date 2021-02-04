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


import uhd
from helper import *

st_args = uhd.usrp.StreamArgs("fc32", "sc16")
usrp = uhd.usrp.MultiUSRP("IP_ADDRESS=%s" % IP_ADDRESS)
usrp.set_tx_rate(RATE, 0)
usrp.set_tx_freq(uhd.types.TuneRequest(CARRIER_FREQUENCY), 0)
usrp.set_tx_gain(GAIN, 0)

streamer = usrp.get_tx_stream(st_args)
max_num_samples = streamer.get_max_num_samps()

metadata = uhd.types.TXMetadata()
metadata.start_of_burst = False
metadata.end_of_burst = False
metadata.has_time_spec = False

##### LOOP For Genetating a OFDM-Like Signal 

#amp= 0.05
#for i in range(2):
#    samples_buffer_1 = type_of_sequence["exp"](t, SOURCE_FREQUENCY,amp) 
#    samples_buffer_2 = type_of_sequence["exp-"](t, SOURCE_FREQUENCY,amp) 
#    samples_buffer +=    samples_buffer_1+samples_buffer_2
#    SOURCE_FREQUENCY*=2
#    amp*=2
#######

#####  Generate the IQ samples (Choose one sequence: ones, zeros, cos, exp, neg_exp, square, manual ), 
# Note: Manual is read from the json file data.json

samples_buffer = type_of_sequence["exp"]() 
#######

#####  Write the Tx signal info into a json file
iq_samples_as_str = [str(iq_sample) for iq_sample in samples_buffer]
data = write_data_to_dict(RATE,SOURCE_FREQUENCY,GAIN,CHANNELS,CARRIER_FREQUENCY,iq_samples_as_str)
write_data_to_json(data)
#######

running = True
#####  Main Tx Loop
while running:
    try:
        streamer.send(samples_buffer, metadata)
    except KeyboardInterrupt:
        running = False
        print("Exiting...")
#######