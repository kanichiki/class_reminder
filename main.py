from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,
    LineBotApiError
)
from linebot.models import (
    FlexSendMessage, MessageEvent, TextMessage, TextSendMessage, CarouselContainer
)
import configparser

import os
import json

app = Flask(__name__)

config_file = configparser.ConfigParser()
config_file.read('./config.ini')

# 環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = config_file.get('LINE', 'channel_access_token')
LINE_CHANNEL_SECRET = config_file.get('LINE', 'channel_secret')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/webhook", methods=['POST'])
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
    class_urls = {'レジリエンスコロキウム': 'https://sites.google.com/g.ecc.u-tokyo.ac.jp/sdm-rc20/?pli=1&authuser=1', 
    'システム設計科学': 'https://zoom.us/j/92647589066?pwd=V05BcnpiZkh2WVlZK2N2dGZUOWFoZz09',
    'システム制御工学': 'https://zoom.us/j/98093061286',
    '量子力学': 'https://zoom.us/j/96396500440?pwd=akxkWm5MV0NBbjZGb1Z6VWdTMUd4QT09',
    '先端コンピューティング': 'https://zoom.us/j/8062021054?pwd=L0dnRGJUa1hMa2RwdFJsd29lTEpzQT09',
    '微分方程式の解法と可視化': 'https://zoom.us/j/91850471543?pwd=M1pLcVBvR01sczFDMHU3cEZuVVJVUT09',
    '電磁エネルギー基礎': 'https://zoom.us/j/91882363434?pwd=Z1NzclFvR3VvS01uUEtNeGpMTGtxdz09',
    '形状モデリングと可視化': 'https://zoom.us/j/99188357630?pwd=Q2xxQ0V5QnRUbmhlKzRWZEtnVzlzZz09',
    '有限要素法と構造解析': 'https://zoom.us/j/95969192926?pwd=ckdmc05mdndxYml3NjFBZzROaUxrdz09',
    '数理演習3B': 'https://zoom.us/j/93081493741?pwd=QjBTRkZ6MWlWTC9RdlpiOXNMNmJvdz09'
    }

    for k, v in class_urls.items():
        if event.message.text == k:
            try:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=v))
            except LineBotApiError:
                return

    

@app.route('/hello')
def hello_world():
    return 'Hello, World!'


if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
