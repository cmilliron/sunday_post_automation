# imports and nescessar modules
import tkinter as tk
from tkinter import messagebox
import random
import pandas as pd
import requests
from sunday import Sunday
from PIL import Image, ImageFont, ImageDraw
from bs4 import BeautifulSoup
import requests
import json
from pytube import YouTube
import pprint

WP_TEMPLATE = "wordpress_template.txt"
YT_POST = "youtube_template.txt"
COMMUNITY_MATTER = "community_matters.txt"
LABEL_FONT = font=("Courier", 14, "bold")

sunday_info = Sunday()


def make_community_matters(matters):
    output_text = ""
    for m in matters:
        if output_text == "":
            output_text = f'<h2 class="null" style="text-align: center; padding-bottom: 15px">{m["title"]}</h2>\n'
            output_text = output_text + f'<p>{m["matter"]}</p>\n'
        else:
            output_text = output_text + '<hr style="margin-top: 20px; margin-bottom: 20px" />\n'
            output_text = output_text + f'<h2 class="null" style="text-align: center; padding-bottom: 15px">{m["title"]}</h2>\n'
            output_text = output_text + f'<p>{m["matter"]}</p>\n'
    make_file(output_text, f"Community Matters - {sunday_info.other_date}")


def download(link):
    yt = YouTube(link)
    yt_stream = yt.streams.get_highest_resolution()
    try:
        yt_stream.download(output_path="output/")
    except:
        print("There has been an error in downloading your youtube video")
    print("This download has completed! Yahooooo!")


def yt_download_videos(video_list):
    for video in video_list:
        print(f'Trying to download {video["title"]}')
        download(video["link"])


def get_verse_link(v):
    y = v.replace(" ", "+")
    z = y.replace(":", "%3A")
    v_link = f"https://www.biblegateway.com/passage/?search={z}&version=NRSVUE"
    return v_link


def get_verse_content(v):
    BIBLE_URL = "http://bible.oremus.org/"
    san_v = v.replace(":", ".")
    inquiry = {
        "passage": san_v,
        "version": "NRSV",
        "vnum": "NO"
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
    # make_file(openlp, san_v)
    return openlp


# Receives text as and imput and a file name and writes tha text to a file.
def make_file(content: object, name: object) -> object:
    with open(f'output/{name}.txt', 'w') as file:
        file.write(content)


# Adds text to the templates.
def create_thumbnail(file_date, formal_date, title):
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


# Loads the template and returns the text
def get_template(template):
    with open(f"Resources/{template}") as file:
        text = file.read()
    return text


# Takes youtube template and inserts relevant text
def youtube_text(info, template):
    working_text = template
    working_text = working_text.replace('<SERMON_TAG>', info.tags['sermon_tag'])
    vid_credit = ""
    for v in info.yt_videos:
        vid_credit = vid_credit + " - ".join(v.values()) + "\n"
    working_text = working_text.replace('<YT_TAG>', vid_credit)
    make_file(working_text, f'youtube_{info.tags["date_tag"]}')


# Takes Wordpress template and inserts relevant text
def wordpress_post(info, template):
    working_text = template
    working_text = working_text.replace('<TITLE>', info['title_short'])
    working_text = working_text.replace('<ALT_TEXT>', info['alt_text'])
    working_text = working_text.replace('<LONG_TITLE>', info['title_long'])
    working_text = working_text.replace('<YOUTUBE_EMBED>', info['youtube_embed'])
    working_text = working_text.replace('<SERMON_TAG>', info['sermon_tag'])
    working_text = working_text.replace("<EVENT_TITLE>", info['event_title'])
    working_text = working_text.replace('<YOUTUBE_LINK>', info['youtube_link'])
    working_text = working_text.replace('<BIBLE_LINK>', info['sermon_verse'])
    working_text = working_text.replace('<BIBLE_VERSE>', info['sermon_verse_link'])
    make_file(working_text, f'wordpress_{info["date_tag"]}')


# --------------------tkinter forms input ----------------------  #

def add_verse():
    sunday_info.verses.append(verse.get())
    print(sunday_info.verses)
    verse.delete(0, 'end')
    verse.insert(0, "Success! Add another.")


def add_yt_link():
    sunday_info.yt_link = yt_link.get()
    yt_link.delete(0, 'end')
    yt_link.insert(0, "Success!")


def add_yt_video():
    title = yt_video_title.get()
    link = yt_video_link.get()
    sunday_info.yt_videos.append({"title": title,
                                  "link": link
                                  })
    print(sunday_info.yt_videos)
    yt_video_title.delete(0, 'end')
    yt_video_title.insert(0, "Success! Add another.")
    yt_video_link.delete(0, 'end')


def add_community_matters():
    title = matter_title.get()
    matters = matter.get()
    sunday_info.community_matters.append({"title": title,
                                          "matter": matters
    })
    matter.delete(0, 'end')
    matter_title.delete(0, 'end')
    matter.insert(0, "Success! Add another.")
    # print(sunday_info.community_matters)


def add_formal_date():
    sunday_info.date = date.get()
    date.delete(0, 'end')
    date.insert(0, "Success!")


def add_other_date():
    sunday_info.other_date = other_date.get()
    other_date.delete(0, 'end')
    other_date.insert(0, "Success!")


def add_sermon_title():
    sunday_info.sermon_title = sermon_title.get()
    sermon_title.delete(0, 'end')
    sermon_title.insert(0, "Success!")


def process_data():
    """sunday_info.get_verse_info()
    sunday_info.create_tags()
    create_thumbnail(sunday_info.other_date, sunday_info.date, sunday_info.sermon_title)
    wordpress_post(sunday_info.tags, get_template(WP_TEMPLATE))
    youtube_text(sunday_info, get_template(YT_POST))
    yt_download_videos(sunday_info.yt_videos)"""
    make_community_matters(sunday_info.community_matters)
    # pprint.pprint(sunday_info.verse_data)


    """
    all_content = consolidate_info(weekly_info)
    wordpress_post(all_content, get_template(WP_TEMPLATE))
    youtube_text(all_content, get_template(YT_POST))
    text_to_image(file_date=weekly_info['tag_date'], formal_date=weekly_info['proper_date'],
                  title=weekly_info['sermon_title'])
    with open(f'output/Worship for {weekly_info["tag_date"]}.txt', 'w') as worship_content:
        worship_content.write(json.dumps(all_content, indent=2))
    for video in weekly_info['w_videos']:
        print(f'Trying to download {video["v_title"]}')
        download(video["v_link"])
"""

"""
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    global password_characters
    password_box.delete(0, 'end')
    pd_file = ''
    for _ in range(20):
        new_char = random.choice(password_characters)
        pd_file += new_char
    password_box.insert(0, pd_file)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    w_site = website_box.get()
    username = username_box.get()
    password = password_box.get()
    if w_site == "" or username == "" or password == '':
        messagebox.showinfo(title="oops", message="You left a field empty.")
    else:
        is_ok = messagebox.askokcancel(title=w_site, message="Are you sure you want to continue?")
        if is_ok:
            for_file = w_site + " | " + username + " | " + password + "\n"
            with open("passwords.txt", 'a') as date_file:
                date_file.write(for_file)
            website_box.delete(0, 'end')
            password_box.delete(0, 'end')
"""

if __name__ == "__main__":
    # ---------------------------- UI SETUP ------------------------------- #

    window = tk.Tk()
    window.title("Sunday Automation")

    window.config(pady=25, padx=50)

    canvas = tk.Canvas(height=200, width=400)

    logo_image = tk.PhotoImage(file='Reeds-UMC.png')
    # canvas.create_image(325, 100, image=logo_image)
    canvas.create_image(200, 60, image=logo_image)
    canvas.grid(row=0, column=1, sticky="S")

    # -----------------------------Verse---------------------------------------#

    verse_label = tk.Label(text='Verse:')
    verse_label.grid(row=1, column=0, sticky="E")

    verse = tk.Entry(width=35)
    verse.grid(row=1, column=1, sticky="W") # , columnspan=2)
    verse.insert(0, "Verse")
    verse.focus()

    verse_button = tk.Button(text="Add", width=18, command=add_verse)
    verse_button.grid(row=1, column=2)  # columnspan=2)

    # --------------------------Youtube Link-----------------------------------#

    yt_link_label = tk.Label(text='Streaming Link:')
    yt_link_label.grid(row=2, column=0, sticky="E")

    yt_link = tk.Entry(width=35)
    yt_link.grid(row=2, column=1, sticky="W")
    yt_link.insert(0, "Youtube Streaming Link")

    yt_link_button = tk.Button(text="Add", width=18, command=add_yt_link)
    yt_link_button.grid(row=2, column=2)

    # ---------------------------YouTube Videos---\----------------------------#

    yt_video_title_label = tk.Label(text='Youtube Video Title:')
    yt_video_title_label.grid(row=3, column=0, sticky="E")

    yt_video_title = tk.Entry(width=35)
    yt_video_title.grid(row=3, column=1, sticky="W")
    yt_video_title.insert(0, "Youtube Video Title")

    yt_video_link_label = tk.Label(text='Youtube Video Link:')
    yt_video_link_label.grid(row=4, column=0, sticky="E")

    yt_video_link = tk.Entry(width=35)
    yt_video_link.grid(row=4, column=1, sticky="W")
    yt_video_link.insert(0, "Youtube Link")

    yt_video_button = tk.Button(text="Add", width=18, command=add_yt_video)
    yt_video_button.grid(row=4, column=2)  # columnspan=2)


    # --------------------------Sunday Date-----------------------------------#

    date_label = tk.Label(text='Formal Date:')
    date_label.grid(row=5, column=0, sticky="E")

    date = tk.Entry(width=35)
    date.grid(row=5, column=1, sticky="W")
    date.insert(0, "Formal Date")

    date_button = tk.Button(text="Add", width=18, command=add_formal_date)
    date_button.grid(row=5, column=2)  # columnspan=2)

    # ---------------------Sunday Date for files------------------------------#

    other_date_label = tk.Label(text='Other Date:')
    other_date_label.grid(row=6, column=0, sticky="E")

    other_date = tk.Entry(width=35)
    other_date.grid(row=6, column=1, sticky="W")
    other_date.insert(0, "2023-xx-xx")

    other_date_button = tk.Button(text="Add", width=18, command=add_other_date)
    other_date_button.grid(row=6, column=2)  # columnspan=2)

    # ---------------------Sunday Date for files------------------------------#

    sermon_title_label = tk.Label(text='Sermon Title:')
    sermon_title_label.grid(row=7, column=0, sticky="E")

    sermon_title = tk.Entry(width=35)
    sermon_title.grid(row=7, column=1, sticky="W")
    sermon_title.insert(0, "Sermon Title")

    yt_link_button = tk.Button(text="Add", width=18, command=add_sermon_title)
    yt_link_button.grid(row=7, column=2)  # columnspan=2)

    # ---------------------Community Matters------------------------------#

    com_matters_title_label = tk.Label(text='Matters Title:')
    com_matters_title_label.grid(row=8, column=0, sticky="E")

    matter_title = tk.Entry(width=35)
    matter_title.grid(row=8, column=1, sticky="W")
    matter_title.insert(0, "Title")

    com_matters_label = tk.Label(text='Community Matters:')
    com_matters_label.grid(row=9, column=0, sticky="E")

    matter = tk.Entry(width=35)
    matter.grid(row=9, column=1, sticky="W")
    matter.insert(0, "Community Matters")

    yt_link_button = tk.Button(text="Add", width=18, command=add_community_matters)
    yt_link_button.grid(row=9, column=2)  # columnspan=2)

    # --------------------Process Button-----------------------------------#

    add_button = tk.Button(text="Process", width=36, command=process_data)
    add_button.grid(row=10, column=1, columnspan=2)

    # --------------------Main Loop Call-----------------------------------#

    window.mainloop()
