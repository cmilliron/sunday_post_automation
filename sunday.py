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
        self.tags = {}

    @staticmethod
    def get_bg_link(verse):
        y = verse.replace(" ", "+")
        z = y.replace(":", "%3A")
        v_link = f"https://www.biblegateway.com/passage/?search={z}&version=NRSVUE"
        return v_link

    def create_tags(self):
        self.tags['title_short'] = f'{self.sermon_title}'
        self.tags['title_long'] = f'"{self.sermon_title}" - Worship for {self.date}'
        self.tags['event_title'] = f'Worship for {self.date} - "{self.sermon_title}"'
        self.tags['date_proper'] = self.date
        self.tags['date_tag'] = self.other_date
        self.tags['sermon_tag'] = f'Join Rev Wesley Hall as he brings a sermon from {self.verses[0]}.'
        self.tags[
            'alt_text'] = f'Reeds UMC logo with sermon title, "{self.sermon_title}" with the date, "{self.date}." \n'
        self.tags['youtube_link'] = f'https://youtu.be/{self.yt_link}'
        self.tags['youtube_embed'] = f'https://youtube.com/embed/{self.yt_link}'
        self.tags["sermon_verse"] = self.verse_data[0]['verse_formal']
        self.tags["sermon_verse_link"] = self.verse_data[0]["bg_link"]
        """
        self.tags['opening_verse'] = get_verse_info(info["opening_verse"])
        self.tags['sermon_verse'] = get_verse_info(info["sermon_verse"])
        self.tags["c_matters"] = get_community_matters()
        self.tags['w_videos'] = info['w_videos']
        """

    def get_verse_info(self):
        if len(self.verses) == 0:
            return "None"
        else:
            for v in self.verses:
                # Sanitize import GET request function
                v_formal = v
                bg_link = self.get_bg_link(verse=v)
                san_v = v.replace(":", ".")
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