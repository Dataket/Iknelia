# Python Modules
from decouple import config
from fastapi import FastAPI, HTTPException, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
# My Modules
from modules.speech_recognition import speech_to_text
from modules.traductor import load_corpus_from_json, es_nah_translate
from modules.models.Text import Text

BUBU_KEY = config('BUBU_KEY')
requesting_key = False

app = FastAPI()

# CORS POLICY CORRECTION
origins = [
	'*'
]
methods = [
	'*'
]

app.add_middleware(
	CORSMiddleware,
	allow_origins = origins,
	allow_methods = methods
)

# Simple translate function
def on_path_translation(text):
	# Translate
	try:
		# Load corpus from json
		es_nah_dict            = load_corpus_from_json('./data/es_nah.json')
		es_nah_dict_normalized = load_corpus_from_json('./data/es_nah_normalized.json')
		es_nah_connection      = load_corpus_from_json('./data/es_nah_connection.json')
		translation            = es_nah_translate(
			text                 = text,
			traductor            = es_nah_dict,
			traductor_normalized = es_nah_dict_normalized,
			traductor_connection = es_nah_connection
		)
	except Exception as e:
		raise Exception('Something went wrong with the translation\n', e)

	return translation

@app.get('/')
def home_endpoint():
	return {
		'Hello': 'World'
	}


@app.post('/translate-audio')
async def post_audio_method(
	req: Request,
	audio_file: UploadFile
):
	# Key validation
	if req.headers.get('key') != BUBU_KEY and requesting_key:
		raise HTTPException(status_code=401, detail="You need the key")
	
	# Not empty File validation
	if not audio_file.filename:
		raise HTTPException(status_code=422, detail="Bad request, you need to send some file")

	# Speech to tect
	try:
		config = dict(language_code="es-MX")
		with audio_file.file as source:
			content = source.read()
		audio = {"content": content}
		audio_text, confidence_speech_to_text = speech_to_text(config, audio)
	except Exception as e:
		raise Exception('Something went wrong with the speech to text part', e)
	
	translation = on_path_translation(audio_text)

	return {
		"Original Text": audio_text,
		"Translation": translation,
		"Confidence of speech to text": confidence_speech_to_text
	}

@app.post("/translate-text")
async def translate_text_method(
	req: Request,
	data: Text
):
	text = data.text
	# Key validation
	if req.headers.get('key') != BUBU_KEY and requesting_key:
		raise HTTPException(status_code=401, detail="You need the key")

	# Empty string validation
	if not text:
		raise HTTPException(status_code=422, detail="Bad request, you need to send a non empty text")

	# Translate
	try:
		# Load corpus from json
		es_nah_dict            = load_corpus_from_json('./data/es_nah.json')
		es_nah_dict_normalized = load_corpus_from_json('./data/es_nah_normalized.json')
		es_nah_connection      = load_corpus_from_json('./data/es_nah_connection.json')
		translation            = es_nah_translate(
			text                 = text,
			traductor            = es_nah_dict,
			traductor_normalized = es_nah_dict_normalized,
			traductor_connection = es_nah_connection
		)
	except Exception as e:
		raise Exception('Something went wrong with the translation\n', e)

	return {
		"Original Text": text,
		"Translation": translation,
	}