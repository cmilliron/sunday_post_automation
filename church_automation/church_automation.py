from PIL import Image, ImageFont, ImageDraw
from bs4 import BeautifulSoup
import requests
import json
import pprint


HEADERS = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
WORDPRESS_SERMON = """[column width="1/1" last="true" title="<Title>" title_type="single" implicit="true"]

[iframe src="https://youtube.com/embed/<YouTube>" width="100%" height="600px"]

[/iframe]

[/column]

[column parallax_bg="disabled" parallax_bg_inertia="-0.2" extended="" extended_padding="1" background_color="" background_image="" background_repeat="" background_position="" background_size="auto" background_attachment="" hide_bg_lowres="" background_video="" vertical_padding_top="0" vertical_padding_bottom="0" more_link="" more_text="" left_border="transparent" class="" id="" title="" title_type="single" animation="none" width="1/1" last="true"]

[column_1 width="1/1" last="true" title="<Title>" title_type="single" animation="none" implicit="true"]

<SermonTag>

<strong>Sermon</strong>: "<a href="https://youtu.be/<YouTube>"><Title></a>"

<strong>Scripture</strong>: <a href="<Bible_link>"><Bible_verse></a>

<strong>Prayer Concerns</strong> - Email your prayer concerns to <a href="mailto:whall@wnccumc.net">Rev Wesley Hall</a>

Keep up with everything going on at our church by subscribing to our newsletter. <a href="http://eepurl.com/cRUaer">Click here</a>.

Songs are done under CCLI Streaming License.

[/column_1]

[divider type="1"]

[/divider]

[column_1 width="1/5" last="true" title="undefined" title_type="undefined" animation="none" implicit="true"]

[team_member name="Wesley Hall" position="Senior Pastor" url="/" email="whall@wnccumc.net" phone="" picture="https://reedsumc.org/wp-content/uploads/2021/07/wesleyhall.jpg" googleplus="/" linkedin="" facebook="/" twitter="/" youtube="/" instagram="/" dribble="/" vimeo="/"]

[/team_member]

[/column_1]

[/column]
 """
weekly_info = {
    'opening_verse': "Isaiah 7:10-16",
    'sermon_verse': "Matthew 1:18-25",
    'proper_date': "December 25, 2022",
    'tag_date': "2022-12-25",
    'sermon_title': "Merry F'ing Christmas",
    'youtube_tag': "liyu09s7",
}

wordpress_base = WORDPRESS_SERMON


def text_to_image(file_date, formal_date, title):
    outfile = f"Reeds Weekly Logo - {file_date}.jpg"

    # Image for the background
    my_image = Image.open("Reeds Weekly Logo.jpg")

    # Font used.
    title_font = ImageFont.truetype('Roboto_Condensed/RobotoCondensed-Bold.ttf', 84)

    first_text = title
    second_text = f"Worship for {formal_date}"
    image_editable = ImageDraw.Draw(my_image)

    image_editable.text((960, 920), first_text, font=title_font, align='center', fill="white", anchor='ms')
    image_editable.text((960, 1020), second_text, font=title_font, align='center', fill="white", anchor='ms')
    my_image.save(outfile, "JPEG")


def get_verse_link(v):
    # https://www.biblegateway.com/passage/?search=Matthew+6%3A11-16&version=NRSV
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


def wordpress_text(text):
    pass


def youtube_text():
    pass


def get_verse_info(location):
    verse = [location]
    verse.append(get_verse_link(location))
    verse.append(input(f"What is the content of verse {location}?"))
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
    output_text['title'] = f'"{info["sermon_title"]}" - Worship for {info["proper_date"]}'
    output_text['event_title'] = f'Worship for {info["proper_date"]} - "{info["sermon_title"]}"'
    output_text['sermon_tag'] = f'Join Rev Wesley Hall as he brings a sermon from {info["sermon_verse"]}.'
    output_text['alt_text'] = f'Reeds UMC logo with sermon title, "{info["sermon_title"]}" with the date, "{info["proper_date"]}." \n'
    output_text['youtube_link'] = f'https://youtu.be/{info["youtube_tag"]}'
    output_text['youtube_embed'] = f'https://youtube.com/embed/{info["youtube_tag"]}'
    output_text['opening_verse'] = get_verse_info(info["opening_verse"]) # opening_verse_content
    # f'Opening Verse - {opening_verse} - {opening_verse_link} \n\n {opening_verse_text} \n' + "*" * 20 + '\n'
    output_text['sermon_verse'] = get_verse_info(info["sermon_verse"]) #sermon_verse_content
    # f'Sermon Verse - {sermon_verse} - {sermon_verse_link} \n\n {sermon_verse_text} \n' + "*" * 20 + '\n'
    output_text["c_matters"] = get_community_matters()
    return output_text


# opening_verse_content = get_verse_info(weekly_info["opening_verse"])
# sermon_verse_content = get_verse_info(weekly_info["sermon_verse"])

"""
sermon_title = input("What is the sermon title? ")
sunday_date = input("What is the date of the Sunday? ")
youtube_tag = input("What is the YouTube link for Sunday? ")
"""

text_to_image(file_date=weekly_info['tag_date'], formal_date=weekly_info['proper_date'], title=weekly_info['sermon_title'])


all_content = consolidate_info(weekly_info)
with open(f'Worship for {weekly_info["tag_date"]}.txt', 'w') as worship_content:
    worship_content.write(json.dumps(all_content, indent=2))

"""output_text['alt_text'] = "Community Matters \n\n"
for i in community_matters:
    general_text += i + "\n" + '<div style="text-align: center; padding-top:10px">********************************************************************************</div>' + "\n"
"""

"""
Commented out for testing.
add_title = wordpress_base.replace('<Title>', sermon_title)
add_youtube = add_title.replace("<YouTube>", youtube_tag)
add_bverse = add_youtube.replace("<Bible_verse>", sermon_verse)
add_verse_link = add_bverse.replace("<Bible_link>", sermon_verse_link)
final_wordpress = add_verse_link.replace("<SermonTag>", sermon_tag)
"""

"""
print(general_text)
print()
print(final_wordpress)"""