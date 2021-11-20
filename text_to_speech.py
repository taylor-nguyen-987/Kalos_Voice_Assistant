import pyttsx3

def t_t_s(intent):
    reply = ""
    if intent == 'welcome':
        reply = "Hello Trainer."
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 200)
    engine.say(reply)
    engine.runAndWait()