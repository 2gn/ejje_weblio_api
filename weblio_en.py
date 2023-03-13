from bs4 import BeautifulSoup, SoupStrainer
from requests import Session
from utils import *

class Weblio():
	def __init__(self):
		self.session = Session()

	def _make_soup(self, class_name, html_to_parse):
		strainer = SoupStrainer(class_=SELECTORS[class_name])

		return BeautifulSoup(html_to_parse, "lxml", parse_only=strainer)

	def _select_class_get_text(
		self,
		soup: str,
		class_name: str
	):
		return soup.find(class_=SELECTORS[class_name]).text

	def get_example_sentence(
		self,
		word: str
	):
		result_raw_html = self.session.get(f"{EJ_DOMAIN}sentence/content/{word}").text

		soup = self._make_soup("SENTENCE", result_raw_html)

		sentences = soup.find_all(class_=SELECTORS["SENTENCE"])

		for index, sentence in enumerate(sentences):
			sentence_english = sentence.find(class_=SELECTORS["SENTENCE_EN"]).text
			if isCompleteSentence(sentence_english):
				return [
					sentence_english,
					sentence.find(class_=SELECTORS["SENTENCE_JP"]).text
				]

	def search(
		self,
		word: str
	):
		result_raw_html = self.session.get(f"{EJ_DOMAIN}content/{word}").text

		soup = self._make_soup("INFO", result_raw_html)

		word_meaning = self._select_class_get_text(soup,"MEANING")

		pronounciation = self._select_class_get_text(soup,"PRONOUNCIATION")

		s_english, s_japanese = self.get_example_sentence(word)

		result_keys = {
			"meaning":word_meaning,
			"pronounciation":pronounciation,
			"example_sentence":s_english,
			"example_sentence_meaning": s_japanese
		}

		beautified_result = {key: beautifyString(result_keys[key]) for key in result_keys}

		return beautified_result

if __name__ == '__main__':
	myWeblio = Weblio()
	word_datas = myWeblio.search("berate")
	print(word_datas)