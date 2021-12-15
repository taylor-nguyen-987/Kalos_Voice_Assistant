import speech_recognition as sr

class VoiceInput:

    """Takes in voice input and returns a corrected string of the input"""

    def get_input(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            input = None

            try:
                input = r.recognize_google(audio)
            except Exception as e:
                print(f"Exception: {str(e)}")
        
        return input.lower()
