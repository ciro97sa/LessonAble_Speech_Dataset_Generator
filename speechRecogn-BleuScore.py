import speech_recognition as sr
from nltk.translate.bleu_score import sentence_bleu

reference_text = 'e poi ci siamo lasciati fottuti e rivisti e poi ci siamo baciati nei posti più tristi'
reference_array = reference_text.split(' ')
reference_matrix = [reference_array]

from os import path
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "out9.wav")
 # formati riconosciuti: .aiff .flac .wav

recognizer_instance = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    recognizer_instance.pause_threshold = 3.0
    audio = recognizer_instance.listen(source)
    print("Ok! sto ora elaborando il messaggio!")
try:
    candidate_text = recognizer_instance.recognize_google(audio, language="it-IT")
    candidate_array = candidate_text.split(' ') 
    print("Google ha capito: \n", candidate_text)
    score = sentence_bleu(reference_matrix, candidate_array)
    print("Bleu score: \n", score)
except Exception as e:
    print(e)
