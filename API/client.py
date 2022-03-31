import json
from decouple import config
import requests

BUBU_KEY = config('BUBU_KEY')

app_engine_speech_to_text_url = "https://iknelia-api.uc.r.appspot.com/translate-audio"
app_engine_text_url = "https://iknelia-api.uc.r.appspot.com/translate-text"
local_speech_to_text_url = "http://127.0.0.1:8000/translate-audio"
local_text_url = "http://127.0.0.1:8000/translate-text"


def speech_translate(url):
	# Reading the file
	try:
		audio_file = open('./data/hola_buenas_tardes.wav', 'rb')  # use (r"path/to/file") when using windows path
		payload = audio_file.read()
		number_of_bytes = len(payload)
	except FileNotFoundError:
		print("Sorry brocito, hubo un error con tu archivo")
		exit()

	print("========== FILE FEATURES ==========")
	print("Payload:", payload[:10])
	print("Number of Bytes:", number_of_bytes)
	print("===================================")

	headers = {
		'accept': 'application/json',
		'key': BUBU_KEY
	}

	files = {
		'audio_file': ('hola_buenas_tardes.wav;type=audio/wav', open('./data/hola_buenas_tardes.wav', 'rb')),
	}

	res = requests.post(url, headers=headers, files=files)

	print("========== RESPONSE ==========")
	print("Status:", res.status_code)
	print("JSON")
	print(res.json())
	print("===================================")

def text_translate(url, text):
	headers = {
		'accept': 'application/json',
		'key': BUBU_KEY
	}

	data = json.dumps({
		"text": text
	})

	print(data)

	res = requests.post(url, headers=headers, data=data)

	print("========== RESPONSE ==========")
	print("Status:", res.status_code)
	print("JSON")
	print(res.json())
	print("===================================")

def main():
	speech_translate(local_speech_to_text_url)
	print('========================')
	text_translate(local_text_url, "Hola, buenas tardes")

if __name__ == "__main__":
	main()

