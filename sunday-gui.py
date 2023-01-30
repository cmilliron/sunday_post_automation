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

weekly_info = {
    "verses": []
}

sunday_info = Sunday()

"""
LABEL_FONT = font=("Courier", 14, "bold")
password_characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                      'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B',
                      'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                      'V', 'W', 'X', 'Y', 'Z', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-']

"""

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

# Gathering addition date




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
    sunday_info.community_matters.append(matter.get())
    matter.delete(0, 'end')
    matter.insert(0, "Success! Add another.")
    print(sunday_info.community_matters)


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
    sunday_info.get_verse_info()
    pprint.pprint(sunday_info.verse_data)


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


# ---------------------------- UI SETUP ------------------------------- #

window = tk.Tk()
window.title("Sunday Automation")

window.config(pady=25, padx=50)

canvas = tk.Canvas(height=200, width=400)

logo_image = tk.PhotoImage(file="Reeds-UMC.png")
# canvas.create_image(325, 100, image=logo_image)
canvas.create_image(200, 60, image=logo_image)
canvas.grid(row=0, column=1, sticky=("S"))

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

yt_link_label = tk.Label(text='Youtube Link:')
yt_link_label.grid(row=2, column=0, sticky="E")

yt_link = tk.Entry(width=35)
yt_link.grid(row=2, column=1, sticky="W")
yt_link.insert(0, "Sermon Verse")

yt_link_button = tk.Button(text="Add", width=18, command=add_yt_link)
yt_link_button.grid(row=2, column=2)  # columnspan=2)

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

com_matters_label = tk.Label(text='Community Matters:')
com_matters_label.grid(row=8, column=0, sticky="E")

matter = tk.Entry(width=35)
matter.grid(row=8, column=1, sticky="W")
matter.insert(0, "Community Matters")

yt_link_button = tk.Button(text="Add", width=18, command=add_community_matters)
yt_link_button.grid(row=8, column=2)  # columnspan=2)

# --------------------Process Button-----------------------------------#

add_button = tk.Button(text="Process", width=36, command=process_data)
add_button.grid(row=10, column=1, columnspan=2)

# --------------------Main Loop Call-----------------------------------#

window.mainloop()
