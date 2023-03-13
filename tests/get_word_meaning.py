from ejje_weblio_api import Weblio as WeblioEN

myWeblio = WeblioEN()

behead_meaning_summary = myWeblio.search("behead")

print(behead_meaning_summary["meaning"])
