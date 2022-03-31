import json
import unicodedata

def dict_to_json(data, location):
	try:
		with open(location, 'w') as json_file:
			json.dump(data, json_file)
	except Exception as e:
		return False

	return True

def super_normalize(text):
	return ''.join(
		c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
	).lower()

def split_text_for_special_chars(text, SPECIAL_CHARS):
	text_splitted = []
	sub_text = ''
	for char in text:
		if char in SPECIAL_CHARS:
			text_splitted.append(sub_text.strip())
			text_splitted.append(char)
			sub_text = ''
		else:
			sub_text += char

	# Last sub_string
	text_splitted.append(sub_text.strip())

	return text_splitted