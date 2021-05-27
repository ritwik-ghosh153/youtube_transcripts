import youtube_dl
import webvtt
import os
import re
import csv
import sys

application_path=""

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))


# def resource_path(relative):
#     return os.path.join(
#         os.environ.get(
#             "_MEIPASS2",
#             os.path.abspath(".")
#         ),
#         relative
#     )

def download_subs(url, lang, auto=False):
    print(lang)
    opts = {
        "outtmpl": os.path.join(application_path, "subs/%(title)s"),
        "skip_download": True,
        "writeautomaticsub": auto,
        "writesubtitles": True,
        "subtitlesformat": "vtt",
        "subtitleslangs": [lang],
        # "listsubtitles": True
    }

    with youtube_dl.YoutubeDL(opts) as yt:
        yt.download([url])

links=[]
with open(os.path.join(application_path, 'links.csv')) as f:
    reader= csv.reader(f)
    for row in reader:
        links.append(row[0])
links=links[1:]

for url in links:
    # url = "https://www.youtube.com/watch?v=32laLeJozDM"
    download_subs(url, lang="en", auto=True)
    download_subs(url, lang="zh-Hans", auto=False)
    download_subs(url, lang="ko", auto=False)

for file in os.listdir(os.path.join(application_path, 'subs/')):
    if file.endswith(".vtt"):
        vtt = webvtt.read(os.path.join(application_path, f'subs/{file}'))
        transcript = ""

        lines = []
        for line in vtt:
            # Strip the newlines from the end of the text.
            # Split the string if it has a newline in the middle
            # Add the lines to an array
            lines.extend(line.text.strip().splitlines())

        # Remove repeated lines
        previous = None
        for line in lines:
            if line == previous:
                continue
            transcript += " " + line
            previous = line

        # print(transcript)
        txt_name =  re.sub(r'.vtt$', '.txt', file)
        if not os.path.exists(os.path.join(application_path, 'transcripts/')):
            os.makedirs(os.path.join(application_path, 'transcripts/'))
        with open(os.path.join(application_path, f'transcripts/{txt_name}'),'w') as f:
            f.write(transcript)

        # for caption in webvtt.read('Negotiating M&A deal terms-32laLeJozDM.en.vtt'):
        #     print(caption.start)
        #     print(caption.end)
        #     print(caption.text)
        #     webvtt.from_sbv('captions.sbv').save()