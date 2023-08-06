import fbchat_wrapper as fbw
# from revChatGPT.ChatGPT import Chatbot
# majo ma ban, dezider ma ban, zdeno ma ban, a aj julo (už nie????)
# treba novy ucet (už nie???)
# facebook nema rad botov
# vpn?
client = fbw.Wrapper(prefix="!", email="0915255307", password="kubstein")

@client.Event()
def onMessage(message_object,**kwargs):
    print(f"message event called: {message_object.text}")

client.listen(markAlive=True)
