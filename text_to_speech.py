import pyttsx3

class SpeakerOutput:

    def t_t_s(self, response):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 200)
        engine.say(response)
        engine.runAndWait()