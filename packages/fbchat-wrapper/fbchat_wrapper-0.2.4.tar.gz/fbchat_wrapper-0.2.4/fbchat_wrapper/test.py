
import os
import random
import requests
import json
from bs4 import BeautifulSoup
from pytube import YouTube, Search
from gtts import gTTS
import py_fbchat as fbchat
from fbchat_wrapper import Wrapper
from datetime import datetime as dt
version = "1.2.1"

# majo ma ban, dezider ma ban, zdeno ma ban, a aj julo (už nie????)
# treba novy ucet (už nie???)
# facebook nema rad botov
# vpn?
client = Wrapper(prefix="!", email="0915255307", password="kubstein")
utils = client.utils()
def read_json(file: str):
    with open(file, "r") as f:
        return json.load(f)

def save_json(file: str,contents):
    with open(file,"rw") as f:
        inp = json.load(f)
        inp.update(contents)
        json.dump(f)
# logging
def logmsg(mid: str,file: str = "messages.json", text: str = "", author: str = "None", unsent: bool = False, reply_to: str = None,ts: float = dt.now(),thread: str = "None"):
    datestr = dt.fromtimestamp(ts).isoformat()
    dict = {mid:{"thread":thread,
                "text":text, 
                "author":author, 
                "unsent":unsent,
                "reply":reply_to,
                "datetime":datestr}}
    if not os.path.exists(file):
        with open(file,"w") as f:
            f.write("{}")
    infile = read_json(file)
    infile.update(dict)
    save_json(file,infile)

def toggle_unsent(mid: str, unsent: bool, file: str = "messages.json"):
    if not os.path.exists(file):
        raise FileNotFoundError
    infile = read_json(file)
    infile["unsent"] = unsent
    save_json(file,infile)

def logevent(file: str = "events.json", event: str = "None", author: str = "None",ts: float = dt.now()):
    datestr = dt.fromtimestamp(ts).isoformat()
    dict = {event:{"author":author,
                    "datetime":datestr}}
    if not os.path.exists(file):
        with open(file,"w") as f:
            f.write("{}")
    infile = read_json(file)
    infile.update(dict)
    save_json(file,infile)





# commands:
@client.Command("oneskorenie", [], "oneskorenie")
def oneskorenie(ts,**kwargs):
    print(ts, dt.now().timestamp())
    client.reply(round((dt.now().timestamp())-(ts/1000),1))

@client.Command("info",[],"")
def info(**kwargs):
    client.reply(f"""
    Using fbchat-wrapper: 
    Majo3: {version}
    Copyright (c) SneznyKocur 2023""")
@client.Command("help", [], "pošle help")
def majohelp(**kwargs):
    """
    Aplication command
    """
    client.sendFile(client.utils_genHelpImg(footer=f"Majo3 {version}"))

@client.Command("say", ["sprava"], "napíše vec")
def say(args, **kwargs):
    """
    Aplication command
    """
    if args:
        print(args)
        client.reply(args["sprava"])

@client.Command("tts", ["vec"], "povie vec")
def tts(args, **kwargs):
    """
    Aplication command
    """
    filename = "tts.mp3"
    slovo = args["vec"]
    slovo.replace("\n", "").replace(":", "").replace("'", "").replace("\\", "")
    if not len(slovo) + 4 > 1000:
        gTTS(slovo, lang="sk").save(filename)
        client.sendFile(filename)

@client.Command("gfoto", ["vec"], "najde na googly fotku")
def googlefoto(args, **kwargs):
    """
    Aplication command
    """
    from google_images_search import GoogleImagesSearch

    gis = GoogleImagesSearch(
        "AIzaSyA3YguR6_IFNDMzVzfazCW11JlsN_ZKnjQ", "720a9ec42ba2344e9"
    )
    _searchparams = {"q": args["vec"], "num": 5, "fileType": "jpg"}
    gis.search(search_params=_searchparams)
    for image in gis.results():
        try:
            client.sendFile(image.url)
        except Exception:
            pass

@client.Command("pracuješ", [], "zisti ci majo pracuje")
def pracujes(**kwargs):
    """
    Aplication command
    """
    count = client.utils_threadCount() - 2
    if count:
        client.reply(f"jj {count}")
    else:
        client.reply("nn")

@client.Command("zmaz", ["kolko"], "zmaze spravy")
def zmaz(args, thread, **kwargs):
    """
    Aplication command
    """
    thread_id = thread[0]
    test = 0
    num = int(args["kolko"])
    messages = client.fetchThreadMessages(thread_id=thread_id, limit=10 * num)
    for message in messages:
        if message.author == client.uid and not message.unsent:
            if test < num:
                client.unsend(message.uid)
                test += 1
    client.reply(f"zmazané {num} správ.")

@client.Command("yt", ["link/vec"], "pošle video")
def vid(args, thread, **kwargs):
    """
    Aplication command
    """
    if client.utils_isURL(args["link/vec"]):
        filename = "video.mp4"
        filename2 = "video1.mp4"
        video = YouTube(args["link/vec"]).streams.filter(file_extension="mp4").first()
        video.download(output_path=os.getcwd(), filename=filename)
        client.utils_compressVideo(filename, filename2)
        os.remove(filename)
    else:
        filename = "video.mp4"
        filename2 = "video1.mp4"
        search = Search(args["link/vec"])
        video_results = search.results[0]
        video_results.streams.filter(file_extension="mp4").first().download(
            output_path=os.getcwd(), filename=filename
        )
        client.utils_compressVideo(input=filename, output=filename2)
        os.remove(filename)

    client.sendFile(filename2, args["link/vec"],thread=thread)

@client.Command("slovnik", ["vec"], "najde vec na slovniku")
def slovnik(args, **kwargs):
    """
    Aplication command
    """
    slovo = args["vec"]
    end = ""
    rt = requests.get(f"https://slovnik.juls.savba.sk/?w={slovo}", timeout=2)
    soup = BeautifulSoup(rt.content)
    try:
        for x in soup.body.form.section.div.find_all("p"):
            end += x.get_text() + "\n"

        client.reply(end.strip())
    except AttributeError:
        client.reply("take slovo nie je")

@client.Command("nazor", ["vec"], "da nazor na vec")
def nazor(args, **kwargs):
    """
    Aplication command
    """
    if random.randint(1, 2) == 1:
        client.reply("👍")
    else:
        client.reply("🤢🤮👎")

@client.Command("sprava", ["meno[i]/id","sprava"], "posle spravu")
def sprava(args, **kwargs):
    id = args["meno[i]/id"]
    sprava = args["sprava"]
    thread = client.utils_getThreadFromUserIndex(id)
    client.sendmsg(sprava,thread)

@client.Command("ludia", ["meno"], "vyhlada ludi")
def ludia(args, **kwargs):
    meno = args["meno"]
    _ = ""
    for i,x in enumerate(client.utils_searchForUsers(meno)):
        name = client.utils_getUserName(x)
        _+= f"{i} | {name} | {x}\n"
    client.reply(_)

@client.Command("spravy", ["meno[i]/id"], "posle konverzaciu")
def spravy(args, **kwargs):
    id = args["meno[i]/id"]
    thread = client.utils_getThreadFromUserIndex(id)
    spravy = client.fetchThreadMessages(thread[0], limit=50)
    spravy.reverse()
    for message in spravy:
        list += f"{client.fetchUserInfo(message.author)[message.author].name} -> {message.text}\n"

@client.Command("uinfo", ["meno[i]/id"], "zisti info")
def userinfo(args, **kwargs):
    id= client.utils_getIDFromUserIndex(args["meno[i]/id"])
    user = client.fetchUserInfo(id)[id]
    pfp = user.photo
    url = user.url
    count = user.message_count or 0
    name = user.name
    message = f"""
    {name}:
        Správy: {count}
        Url: {url}
    """
    thread = client.reply(message)
    client.sendFile(pfp,"Fotka:",thread)


# events:
@client.Event()
def onMessage(thread_id,mid,author_id,ts,message_object, **kwargs):
    print("recieved event")
    logmsg(mid,
    "messages.json",
    message_object.text,
    utils.getUserName(author_id),
    message_object.unsent,
    message_object.replied_to,
    ts,
    client.fetchThreadInfo(thread_id)[thread_id].name)

@client.Event()
def onMessageUnsent(mid, **kwargs):
    toggle_unsent(mid,False)
print(client._event_list, client._command_list)
client.listen(markAlive=True)
