from gtts import gTTS
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from googletrans import Translator
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from humanfriendly import format_timespan, format_size, format_number, format_length

from flask import Flask, request, make_response

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import *

import time, random, sys, json, codecs, threading, glob, re, string, os, requests, six, ast, pytz, urllib3, urllib.parse, traceback, atexit, wikipedia

app = Flask(__name__)

line_bot_api = LineBotApi('cTWmUANh7KGLR4Cxc86sr9cO8OBFBBhBL+C5jq0d+3t4IgtAVqE/Rd9YVA/NgjeuttBPAeJW5QBEFn5ur3wHRfEViZcScGhbg2NrEMaTNeC0+V6N64JUwOmEbnbAkd69yv/MZ/+8SzrISK7SsOnbAwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5e4444d3b86cf740212e7d8e8764a1fc')

list_language = {
    "list_textToSpeech": {
        "id": "Indonesia",
        "af" : "Afrikaans",
        "sq" : "Albanian",
        "ar" : "Arabic",
        "hy" : "Armenian",
        "bn" : "Bengali",
        "ca" : "Catalan",
        "zh" : "Chinese",
        "zh-cn" : "Chinese (Mandarin/China)",
        "zh-tw" : "Chinese (Mandarin/Taiwan)",
        "zh-yue" : "Chinese (Cantonese)",
        "hr" : "Croatian",
        "cs" : "Czech",
        "da" : "Danish",
        "nl" : "Dutch",
        "en" : "English",
        "en-au" : "English (Australia)",
        "en-uk" : "English (United Kingdom)",
        "en-us" : "English (United States)",
        "eo" : "Esperanto",
        "fi" : "Finnish",
        "fr" : "French",
        "de" : "German",
        "el" : "Greek",
        "hi" : "Hindi",
        "hu" : "Hungarian",
        "is" : "Icelandic",
        "id" : "Indonesian",
        "it" : "Italian",
        "ja" : "Japanese",
        "km" : "Khmer (Cambodian)",
        "ko" : "Korean",
        "la" : "Latin",
        "lv" : "Latvian",
        "mk" : "Macedonian",
        "no" : "Norwegian",
        "pl" : "Polish",
        "pt" : "Portuguese",
        "ro" : "Romanian",
        "ru" : "Russian",
        "sr" : "Serbian",
        "si" : "Sinhala",
        "sk" : "Slovak",
        "es" : "Spanish",
        "es-es" : "Spanish (Spain)",
        "es-us" : "Spanish (United States)",
        "sw" : "Swahili",
        "sv" : "Swedish",
        "ta" : "Tamil",
        "th" : "Thai",
        "tr" : "Turkish",
        "uk" : "Ukrainian",
        "vi" : "Vietnamese",
        "cy" : "Welsh"
    },
    "list_translate": {    
        "af": "afrikaans",
        "sq": "albanian",
        "am": "amharic",
        "ar": "arabic",
        "hy": "armenian",
        "az": "azerbaijani",
        "eu": "basque",
        "be": "belarusian",
        "bn": "bengali",
        "bs": "bosnian",
        "bg": "bulgarian",
        "ca": "catalan",
        "ceb": "cebuano",
        "ny": "chichewa",
        "zh-cn": "chinese (simplified)",
        "zh-tw": "chinese (traditional)",
        "co": "corsican",
        "hr": "croatian",
        "cs": "czech",
        "da": "danish",
        "nl": "dutch",
        "en": "english",
        "eo": "esperanto",
        "et": "estonian",
        "tl": "filipino",
        "fi": "finnish",
        "fr": "french",
        "fy": "frisian",
        "gl": "galician",
        "ka": "georgian",
        "de": "german",
        "el": "greek",
        "gu": "gujarati",
        "ht": "haitian creole",
        "ha": "hausa",
        "haw": "hawaiian",
        "iw": "hebrew",
        "hi": "hindi",
        "hmn": "hmong",
        "hu": "hungarian",
        "is": "icelandic",
        "ig": "igbo",
        "id": "indonesian",
        "ga": "irish",
        "it": "italian",
        "ja": "japanese",
        "jw": "javanese",
        "kn": "kannada",
        "kk": "kazakh",
        "km": "khmer",
        "ko": "korean",
        "ku": "kurdish (kurmanji)",
        "ky": "kyrgyz",
        "lo": "lao",
        "la": "latin",
        "lv": "latvian",
        "lt": "lithuanian",
        "lb": "luxembourgish",
        "mk": "macedonian",
        "mg": "malagasy",
        "ms": "malay",
        "ml": "malayalam",
        "mt": "maltese",
        "mi": "maori",
        "mr": "marathi",
        "mn": "mongolian",
        "my": "myanmar (burmese)",
        "ne": "nepali",
        "no": "norwegian",
        "ps": "pashto",
        "fa": "persian",
        "pl": "polish",
        "pt": "portuguese",
        "pa": "punjabi",
        "ro": "romanian",
        "ru": "russian",
        "sm": "samoan",
        "gd": "scots gaelic",
        "sr": "serbian",
        "st": "sesotho",
        "sn": "shona",
        "sd": "sindhi",
        "si": "sinhala",
        "sk": "slovak",
        "sl": "slovenian",
        "so": "somali",
        "es": "spanish",
        "su": "sundanese",
        "sw": "swahili",
        "sv": "swedish",
        "tg": "tajik",
        "ta": "tamil",
        "te": "telugu",
        "th": "thai",
        "tr": "turkish",
        "uk": "ukrainian",
        "ur": "urdu",
        "uz": "uzbek",
        "vi": "vietnamese",
        "cy": "welsh",
        "xh": "xhosa",
        "yi": "yiddish",
        "yo": "yoruba",
        "zu": "zulu",
        "fil": "Filipino",
        "he": "Hebrew"
    }
}

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = (event.message.text).lower()
    msg = text.split()
    groupId = event.source.group_id
    userId = event.source.user_id
    profile = line_bot_api.get_profile(userId)
    profile_name = profile.display_name
    profile_picture = profile.picture_url
    profile_sm = profile.status_message

    if '/apakah ' in text:
        rep = text.replace("/apakah ","")
        txt = ["Ya","Tidak","Bisa Jadi","Mungkin","Hoax","Coba tanya lagi"]

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=random.choice(txt)))

    elif '/tr-' in text:
        separate = text.split("-")
        separate = separate[1].split(" ")
        lang = separate[0]
        say = text.replace("/tr-" + lang + " ","")
        if lang not in list_language["list_translate"]:
            return line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bahasa: " + lang + ". tidak ditemukan."))
        translator = Translator()
        hasil = translator.translate(say, dest=lang)
        tr = hasil.text
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=tr))

    elif '/carivideo ' in text:
        separate = text.split(" ")
        search = text.replace(separate[0] + " ","")
        params = {"search_query": search}
        source = requests.get("https://www.youtube.com/results", params = params)
        bsoup = BeautifulSoup(source.content, "html5lib")
        ret_ = "[ RESULT ]"
        datas = []
        num = 0
        for data in soup.select(".yt-lockup-title > a[title]"):
            if "&lists" not in data["href"]:
                datas.append(data)
        num += 1
        for data in datas:
            ret_ += "\n\n{}. Judul: {}".format(num, data["title"])
            ret_ += "\n    Link: https://www.youtube.com{}".format(data["href"])
        ret_ += "\n\n[ TOTAL: {} VIDEO ]".format(len(datas))
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=ret_))


if __name__ == "__main__":
    app.run()
