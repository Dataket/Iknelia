import json

from .es_nah import *

def load_corpus_from_json(path):
	with open(path, 'r') as json_file:
		return json.load(json_file)