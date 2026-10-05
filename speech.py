#speech.py This module converts voice to text.

import speech_recognition as sr

recognizer = sr.Recognizer()


def listen():

    try:

        with sr.Microphone() as source:

            print("\n Listening...")

            recognizer.adjust_for_ambient_noise(source, duration=1)

            audio = recognizer.listen(source)

        text = recognizer.recognize_google(audio)

        print(f"\nYou said: {text}")

        return text

    except sr.UnknownValueError:

        print("Sorry, I couldn't understand your voice.")

    except sr.RequestError:

        print("Speech Recognition service unavailable.")

    except Exception as e:

        print("Error:", e)

    return None