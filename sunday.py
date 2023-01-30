import requests
from bs4 import BeautifulSoup

BIBLE_URL = "http://bible.oremus.org/"
get_parameters = {
        "version": "NRSV",
        "vnum": "NO"
    }


class Sunday:

    def __init__(self):
        self.verses = []
        self.verse_data = []
        self.community_matters = []
        self.yt_videos = []

    @staticmethod
    def get_bg_link(verse):
        y = verse.replace(" ", "+")
        z = y.replace(":", "%3A")
        v_link = f"https://www.biblegateway.com/passage/?search={z}&version=NRSVUE"
        return v_link

    def get_verse_info(self):
        if len(self.verses) == 0:
            return "None"
        else:
            for v in self.verses:
                # Sanitize import GET request function
                v_formal = v
                bg_link = self.get_bg_link(verse=v)
                san_v: object = v.replace(":", ".")
                get_parameters['passage'] = san_v
                response = requests.get(url=BIBLE_URL, params=get_parameters)
                soup = BeautifulSoup(response.content, "html.parser")
                passage = soup.find("div", {"class": "bibletext"})
                verses = passage.find("p")
                for v in verses("sup"):
                    v.decompose()
                    # verses_final.append(v)
                verses_final = verses.text.splitlines()[1:]
                openlp = f"{san_v}"
                for lines in verses_final:
                    if len(lines) > 0:
                        openlp = openlp + "\n[===]\n" + lines
                self.verse_data.append({
                    "verse_formal": v_formal,
                    "verse_sanitized": san_v,
                    "bg_link": bg_link,
                    "openlp": openlp
                })
                # make_file(openlp, san_v)

                #  return openlp


"""
    def verse_info(self):
        
        san_v = self.verses.replace(":", ".")
        inquiry["passage"] = san_v
        response = requests.get(url=BIBLE_URL, params=inquiry)
        soup = BeautifulSoup(response.content, "html.parser")
        passage = soup.find("div", {"class": "bibletext"})
        verses = passage.find("p")
        for v in verses("sup"):
            v.decompose()
            # verses_final.append(v)
        verses_final = verses.text.splitlines()[1:]
        # print(verses_final)
        return self.convert_to_openlp(passage=verses_final, loc=f"{inquiry['passage']})
        openlp = f"{inquiry['passage']}"
        for v in verses_final:
            if len(v) > 0:
                openlp = openlp + "\n[===]\n" + v
        make_file(openlp, san_v)
        return openlp

    def convert_to_openlp(self, passage, loc):
        pass
"""