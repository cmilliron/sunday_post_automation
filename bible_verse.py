import pprint
import requests
from bs4 import BeautifulSoup

BIBLE_URL = "http://bible.oremus.org/"

inquiry = {
    "passage": "Genesis 1.1-10",
    "version": "NRSV",
    "vnum" : "NO"
}

response = requests.get(url=BIBLE_URL, params=inquiry)
soup = BeautifulSoup(response.content, "html.parser")
passage = soup.find("div", {"class": "bibletext"})
verses = passage.find("p")

for v in verses("sup"):
    v.decompose()
    # verses_final.append(v)

verses_final = verses.text.splitlines()[1:]
# print(verses_final)

openlp = f"{inquiry['passage']}"
for v in verses_final:
    if len(v) > 0:
        openlp = openlp + "\n[===]\n" + v


print(openlp)