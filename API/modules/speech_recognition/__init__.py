# import speech_recognition as sr

# def speech_to_text(location):
# 	r = sr.Recognizer()
# 	audio_file = sr.AudioFile(location)
	
# 	with audio_file as source:
# 		audio = r.record(source)

# 	return r.recognize_google(audio, language='es-MX')


# Google API
from google.cloud import speech_v1 as speech

def speech_to_text(config, audio):
	client = speech.SpeechClient()
	response = client.recognize(config=config, audio=audio)
	for result in response.results:
		best_alternative = result.alternatives[0]
		transcript = best_alternative.transcript
		confidence = best_alternative.confidence
		return transcript, confidence