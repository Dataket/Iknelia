# Here are the functions for Spanish to Nahuatl translate
from typing import Dict

from modules.tools.text_function import (
	split_text_for_special_chars, 
	super_normalize
)

def es_nah_translate(
	text: str,
	traductor: Dict[str, str],
	traductor_normalized: Dict[str, str],
	traductor_connection: Dict[str, str]
):
	"""Translates from Spanish to Nahuatl with the corpus loaded
	
	Keyword arguments:
		text: str = Text to be translated
		traductor: Dict[str, str] = A dictionary containing the translations for each sentence or word
		traductor_normalized: Dict[str, str] = A normalized dictionary containing the translations for each sentence or word
		traductor_connection: Dict[str, str] = A dictionary containing the keys of both traductors connected from normalized to not normalized {"cancion": "canción"}
	Return: 
		translate: str = The translation of the original text
	"""
	SPECIAL_CHARS = [',', '.', '-']
	text_normalized = super_normalize(text)
	# We need to separate per special characters like [".", ",", "-"]
	text_splitted = split_text_for_special_chars(text_normalized, SPECIAL_CHARS)
	# Translate every sub-string with sub_translate
	text_splitted_translated = []
	for ss in text_splitted:
		text_splitted_translated.append(
			sub_translate(
				ss,
				traductor, 
				traductor_normalized,
				traductor_connection
			)
		)

	# Merge the sub_translates
	translate = ''
	for phrase in text_splitted_translated:
		translate += phrase.strip()
		if phrase.strip() in SPECIAL_CHARS:
			translate += ' '

	return translate
	
	

def sub_translate(text, traductor, traductor_normalized, connection):
	translate = ''
	words = text.split(" ")
	start = 0
	end = len(words)
	while start != len(words):
		while start != end:
			phrase = ' '.join(words[start:end]).lower()
			if super_normalize(phrase) in traductor_normalized:
				not_normalized_key = connection[phrase]
				#! Here I just grab the first one
				translate += traductor[not_normalized_key].split(",")[0] + ' '
				start = end
				end = len(words)
				break
			else:
				if len(words[start:end]) == 1:
					translate += phrase + ' '
					start += 1
					end = len(words)
				else:
					end -= 1

	#print("translate:", translate)


	return translate