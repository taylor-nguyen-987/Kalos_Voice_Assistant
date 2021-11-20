from pyaudio import PyAudio, paInt16
from deepspeech import Model
import numpy as np
import pages

CHUNK = 2048  # Number of frames in a buffer
FORMAT = paInt16  # Sample Size
RATE_PROCESS = 16000  # Sampling rate AKA the number of frames per second
CHANNELS = 1 #Each frame as 1 sample

class Audio:
    def __init__(self):
        self.p = PyAudio() #Pyaudio object
        self.ds = Model("deepspeech-0.9.3-models.pbmm") #Deepspeech model
        self.ds.enableExternalScorer("deepspeech-0.9.3-models.scorer")

    def get_result(self):
        """Returns the result of the audio"""
        stream = self.ds.createStream()
        print("Listening...")
        r_stream = self.p.open(format=FORMAT, channels=CHANNELS, rate=RATE_PROCESS, input=True,
                      frames_per_buffer=CHUNK)

        while pages.listening:
            buff = np.frombuffer(r_stream.read(CHUNK), dtype=np.int16)
            stream.feedAudioContent(buff)

        r_stream.stop_stream()
        r_stream.close()
        self.p.terminate()

        audio = stream.finishStream()
        print("Done!")

        return audio
