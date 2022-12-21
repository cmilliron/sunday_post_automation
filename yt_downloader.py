from pytube import YouTube


def download(link):
    yt = YouTube(link)
    yt_stream = yt.streams.get_highest_resolution()
    try:
        yt_stream.download(output_path="output/")
    except:
        print("There has been an error in downloading your youtube video")
    print("This download has completed! Yahooooo!")


if __name__ == "__main__":
    dl_link = input("Put your youtube link here!! URL: ")
    download(dl_link)