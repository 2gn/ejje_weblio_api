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

def isCompleteSentence(sentence):
	return True if sentence[0].isupper() else False


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
