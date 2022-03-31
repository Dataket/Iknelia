from bs4 import BeautifulSoup

from modules.tools.text_function import super_normalize

def get_page(location):
	with open(location, 'r') as page:
		bd4_page = BeautifulSoup(page, 'html.parser')

	return bd4_page


def get_corpus(location):
	"""This function takes de page corpus from https://aulex.org/es-nah/
	and converts it to a list with all the spanish words and all the nahuatl
	words in the corpus, it also returns a "translate" dictionary. 
	
	Keyword arguments: 
		location -- Location of the file downloaded from the link above
	Return:
		spanish_words   :List['string']
		nahuatl_words   :List['string']
		spa_to_nah_dict :Dict['string', 'string']
	"""
	# ========== Scrap the page ========== #
	page = get_page(location)
	paragraphs = page.find_all('p')[2:]
	spanish_words = []
	nahuatl_words = []

	# ========== Convert the tags into lists ========== #
	for p in paragraphs:
		spans = p.find_all('span')
		if len(spans) == 2:
			spanish_words.append(spans[0].get_text()[:-1].strip())
			nahuatl_words.append(spans[1].get_text().strip())

	# ========== Convert this lists into dictionaries ========== # 
	# The traductor dictionary
	spa_to_nah_dict = {es:nah for (es, nah) in zip(spanish_words, nahuatl_words)}
	
	# Normalized version of the traductor dictionary
	spa_to_nah_dict_normalized = {
		super_normalize(es): super_normalize(nah)
		for (es, nah) in zip(spanish_words, nahuatl_words)
	}

	# We need a connection between these two so
	not_normalized_to_normalized = {
		super_normalize(es): es
		for es in spanish_words
	}



	return (
		spanish_words,
		nahuatl_words, 
		spa_to_nah_dict, 
		spa_to_nah_dict_normalized,
		not_normalized_to_normalized
	)