from PIL import Image, ImageFont, ImageDraw
from bs4 import BeautifulSoup
import requests
import json
from pytube import YouTube
import pprint


HEADERS = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
WP_TEMPLATE = "wordpress_template.txt"
YT_POST = "youtube_template.txt"

weekly_info = {
    'opening_verse': "Isaiah 7:10-16",
    'sermon_verse': "Matthew 1:18-25",
    'proper_date': "December 25, 2022",
    'tag_date': "2022-12-25",
    'sermon_title': "Merry F'ing Christmas",
    'youtube_tag': "liyu09s7",
    'w_videos': [{
        'v_title': 'Lo, He Comes With Clouds Descending - YouTube',
        'v_link': 'https://www.youtube.com/watch?v=suz0cQbjwm0'},
        {'v_title': 'I Want to be Ready - YouTube',
        'v_link': 'https://www.youtube.com/watch?v=iyW0x1JC3sc'}
    ]
}


def download(link):
    yt = YouTube(link)
    yt_stream = yt.streams.get_highest_resolution()
    try:
        yt_stream.download(output_path="output/")
    except:
        print("There has been an error in downloading your youtube video")
    print("This download has completed! Yahooooo!")


def text_to_image(file_date, formal_date, title):
    outfile = f"output/Reeds Weekly Logo - {file_date}.jpg"

    # Image for the background
    my_image = Image.open("resources/images/Reeds Weekly Logo.jpg")

    # Font used.
    title_font = ImageFont.truetype('resources/font/Roboto_Condensed/RobotoCondensed-Bold.ttf', 84)

    first_text = title
    second_text = f"Worship for {formal_date}"
    image_editable = ImageDraw.Draw(my_image)

    image_editable.text((960, 920), first_text, font=title_font, align='center', fill="white", anchor='ms')
    image_editable.text((960, 1020), second_text, font=title_font, align='center', fill="white", anchor='ms')
    my_image.save(outfile, "JPEG")


def get_verse_link(v):
    y = v.replace(" ", "+")
    z = y.replace(":", "%3A")
    v_link = f"https://www.biblegateway.com/passage/?search={z}&version=NRSVUE"
    return v_link


def convert_to_string(word_list):
    output_string = ''
    for line in word_list:
        output_string += line + "\n[===]\n"
    return output_string


def get_verses(url):
    r = requests.get(url, HEADERS)
    verses_list = []
    soup = BeautifulSoup(r.content, "html.parser")
    passage_panel = soup.find("div", {'class': 'passage-text'})
    verses = passage_panel.find_all("span")
    for v in verses:
        ver = v
        try:
            sup_tag = ver.sup.extract()
        except:
            pass
        verses_list.append(ver.text)
    # print(verses_list)
    verse_text = convert_to_string(verses_list)
    return verse_text



def wordpress_post(info, template):
    working_text = template
    working_text = working_text.replace('<TITLE>', info['title_short'])
    working_text = working_text.replace('<ALT_TEXT>', info['alt_text'])
    working_text = working_text.replace('<LONG_TITLE>', info['title_long'])
    working_text = working_text.replace('<YOUTUBE_EMBED>', info['youtube_embed'])
    working_text = working_text.replace('<SERMON_TAG>', info['sermon_tag'])
    working_text = working_text.replace('<YOUTUBE_LINK>', info['youtube_link'])
    working_text = working_text.replace('<BIBLE_LINK>', info['sermon_verse'][1])
    working_text = working_text.replace('<BIBLE_VERSE>', info['sermon_verse'][0])
    with open(f'output/Wordpress {info["date_tag"]}', 'w') as file:
        file.write(working_text)


def youtube_text(info, template):
    working_text = template
    working_text = working_text.replace('<SERMON_TAG>', info['sermon_tag'])
    vid_credit = ""
    for v in info["w_videos"]:
        vid_credit = vid_credit + " - ".join(v.values()) + "\n"
    working_text = working_text.replace('<YT_TAG>', vid_credit)
    # return working_text
    with open(f'output/Youtube {info["date_tag"]}', 'w') as file:
        file.write(working_text)

def get_verse_info(location):
    verse = [location, get_verse_link(location), input(f"What is the content of verse {location}? ")]
    return verse


def get_community_matters():
    c_matters = []
    while True:
        matter = input("Community Matters: (Enter to 'q' to quit) ")
        if matter.lower() == 'q':
            break
        else:
            c_matters.append(matter)
            # community_matters.append('<div style="text-align: center;" >********************************************************************************</div>')
    return c_matters


def consolidate_info(info):
    output_text = {}
    output_text['title_short'] = f'{info["sermon_title"]}'
    output_text['title_long'] = f'"{info["sermon_title"]}" - Worship for {info["proper_date"]}'
    output_text['event_title'] = f'Worship for {info["proper_date"]} - "{info["sermon_title"]}"'
    output_text['date_proper'] = info["proper_date"]
    output_text['date_tag'] = info["tag_date"]
    output_text['sermon_tag'] = f'Join Rev Wesley Hall as he brings a sermon from {info["sermon_verse"]}.'
    output_text['alt_text'] = f'Reeds UMC logo with sermon title, "{info["sermon_title"]}" with the date, "{info["proper_date"]}." \n'
    output_text['youtube_link'] = f'https://youtu.be/{info["youtube_tag"]}'
    output_text['youtube_embed'] = f'https://youtube.com/embed/{info["youtube_tag"]}'
    output_text['opening_verse'] = get_verse_info(info["opening_verse"])
    # f'Opening Verse - {opening_verse} - {opening_verse_link} \n\n {opening_verse_text} \n' + "*" * 20 + '\n'
    output_text['sermon_verse'] = get_verse_info(info["sermon_verse"])
    # f'Sermon Verse - {sermon_verse} - {sermon_verse_link} \n\n {sermon_verse_text} \n' + "*" * 20 + '\n'
    output_text["c_matters"] = get_community_matters()
    output_text['w_videos'] = info['w_videos']
    return output_text


def get_user_input():
    sermon_title = input("What is the sermon title? ")
    sunday_date = input("What is the date of the Sunday? ")
    youtube_tag = input("What is the YouTube link for Sunday? ")


def get_template(template):
    with open(f"Resources/{template}") as file:
        text = file.read()
    return text


if __name__ == "__main__":
    all_content = consolidate_info(weekly_info)
    wordpress_post(all_content, get_template(WP_TEMPLATE))
    youtube_text(all_content, get_template(YT_POST))
    #text_to_image(file_date=weekly_info['tag_date'], formal_date=weekly_info['proper_date'],
    #              title=weekly_info['sermon_title'])
    #with open(f'output/Worship for {weekly_info["tag_date"]}.txt', 'w') as worship_content:
    #    worship_content.write(json.dumps(all_content, indent=2))
    # for video in weekly_info['w_vidoes']:
    #    print(f'Trying to download {video["v_title"]}')
    #    download(video["v_link"])

"""output_text['alt_text'] = "Community Matters \n\n"
for i in community_matters:
    general_text += i + "\n" + '<div style="text-align: center; padding-top:10px">********************************************************************************</div>' + "\n"
"""
