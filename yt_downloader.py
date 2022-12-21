from pytube import YouTube


def Download(link):
    yt = YouTube(link)
    yt = yt.streams.get_highest_resolution()
    try:
        yt.download()
    except:
        print("There has been an error in downloading your youtube video")
    print("This download has completed! Yahooooo!")


if __name__ == "__main__":
    dl_link = input("Put your youtube link here!! URL: ")
    Download(dl_link)