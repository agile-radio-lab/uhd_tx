import json
import numpy as np

IP_ADDRESS = "192.168.11.4"
RATE = 500e3
SOURCE_FREQUENCY = 15e3
GAIN = 0
CHANNELS = [0]
CARRIER_FREQUENCY = 901e6
N_SAMPLES = 200
DURATION = N_SAMPLES / RATE
T = np.linspace(0, DURATION, N_SAMPLES, dtype=np.complex64)


def ones_sequence(n_samples=N_SAMPLES):
    return np.ones(n_samples, dtype=np.complex64)

def zeros_sequence(n_samples=N_SAMPLES):
    return np.zeros(n_samples, dtype=np.complex64)

def rectangular(n_samples=N_SAMPLES,period=1e3,puls_width=500):
    rect = np.arange(n_samples) % period < puls_width
    return [float(sample) for sample in rect]

def mod_exp(t=T, freq=SOURCE_FREQUENCY, amp=.05):
    return amp*np.exp(2j*np.pi*freq*t)

def mod_neg_exp(t=T, freq=SOURCE_FREQUENCY, amp=.05):
    return amp*np.exp(-2j*np.pi*freq*t)


def mod_am(t=T, freq=SOURCE_FREQUENCY, amp=.05):
    return amp*np.cos(2*np.pi*freq*t)

def get_sequence_from_json(filename="data.json"):
    with open(filename) as f:
        data = json.load(f)
        iq_sequence =[]
        for i_q in data["iq_samples"]:
            iq_sequence.append(np.complex64(complex(i_q)))
        return iq_sequence


type_of_sequence = {"ones":ones_sequence,"zeros":zeros_sequence,"square":rectangular,"exp":mod_exp,"neg_exp":mod_neg_exp,"cos":mod_am,"manual":get_sequence_from_json}


def write_data_to_dict(rate,source_frequency,gain,channels,carrier_frequency,iq_samples):

    data = {"sample_rate": rate,
            "source_frequency":source_frequency,
            "tx_gain":gain,
            "carrier_frequency":carrier_frequency,
            "iq_samples":iq_samples}
    return data
    
def write_data_to_json(data):
    with open('data.json', 'w') as fp:
        json.dump(data, fp)