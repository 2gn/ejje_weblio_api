from bs4 import BeautifulSoup, SoupStrainer
from requests import Session

SELECTORS = {
	"INFO": "mainBlock non-member hlt_SUMRY",
	"MEANING": "content-explanation ej",
	"PRONOUNCIATION": "phoneticEjjeDesc",
	"SENTENCE_LIST": "mainBlock hlt_SNTCE",
	"SENTENCE": "qotC",
	"SENTENCE_EN": "qotCE",
	"SENTENCE_JP": "qotCJ"
}

EJ_DOMAIN = "https://ejje.weblio.jp/"

def removeSymbol(string: str, symbol: str):
	return string.replace(symbol, "")

def removeDictionaryName(string):
	return string.split("\xa0-\xa0")[0]

def beautifyString(string: str):
	return removeSymbol(
		removeSymbol(
				removeSymbol(
					removeDictionaryName(string),
					"例文帳に追加"
				),
				"\n"
			),
		"  "
	)

class Weblio():
	def __init__(self):
		self.session = Session()

	def isCompleteSentence(self, sentence):
		return True if sentence[0].isupper() else False

	def get_example_sentence(self, word: str):
		result_raw_html = self.session.get(f"{EJ_DOMAIN}sentence/content/{word}").text

		strainer = SoupStrainer(class_=SELECTORS["SENTENCE"])

		soup = BeautifulSoup(result_raw_html, "lxml", parse_only=strainer)

		sentences = soup.find_all(class_=SELECTORS["SENTENCE"])

		for index, sentence in enumerate(sentences):
			sentence_english = sentence.find(class_=SELECTORS["SENTENCE_EN"]).text
			if self.isCompleteSentence(sentence_english):
				return [
					sentence_english,
					sentence.find(class_=SELECTORS["SENTENCE_JP"]).text
				]

	def search(self, word: str):
		result_raw_html = self.session.get(f"{EJ_DOMAIN}content/{word}").text

		strainer = SoupStrainer(class_=SELECTORS["INFO"])

		soup = BeautifulSoup(
			result_raw_html,
			"lxml",
			parse_only=strainer
		)

		word_meaning = soup.find(class_=SELECTORS["MEANING"]).text

		pronounciation = soup.find(class_=SELECTORS["PRONOUNCIATION"]).text

		s_english, s_japanese = self.get_example_sentence(word)

		return {
			"meaning": beautifyString(word_meaning),
			"pronounciation": beautifyString(pronounciation),
			"example_sentence": beautifyString(s_english),
			"example_sentence_meaning": beautifyString(s_japanese)
		}

if __name__ == '__main__':
	myWeblio = Weblio()
	word_datas = myWeblio.search("berate")

	print(word_datas)