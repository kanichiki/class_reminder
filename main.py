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
    classes = {
        'レジリエンスコロキウム': {
            'url':'https://sites.google.com/g.ecc.u-tokyo.ac.jp/sdm-rc20/?pli=1&authuser=1',
            'evaluation_method':'2週間後までレポート',
            'extra':'オムニバス'
        }, 
        'システム設計科学': {
            'url':'https://zoom.us/j/92647589066?pwd=V05BcnpiZkh2WVlZK2N2dGZUOWFoZz09',
            'evaluation_method':'出席、レポート',
            'extra':'DJ'
        },
        'システム制御工学': {
            'url':'https://zoom.us/j/98093061286',
            'evaluation_method':'講義への態度（不定期に実施する講義内の演習課題など）、期末試験を40-60%程度',
            'extra':''
        },
        '量子力学': {
            'url':'https://zoom.us/j/96396500440?pwd=akxkWm5MV0NBbjZGb1Z6VWdTMUd4QT09',
            'evaluation_method':'出席、レポート',
            'extra':'クソムズイ'
        },
        '先端コンピューティング': {
            'url':'https://zoom.us/j/8062021054?pwd=L0dnRGJUa1hMa2RwdFJsd29lTEpzQT09',
            'evaluation_method':'出席、レポート',
            'extra':'材料力学'
        },
        '微分方程式の解法と可視化': {
            'url':'https://zoom.us/j/91850471543?pwd=M1pLcVBvR01sczFDMHU3cEZuVVJVUT09',
            'evaluation_method':'出席、レポート、期末試験',
            'extra':''
        },
        '電磁エネルギー基礎': {
            'url':'https://zoom.us/j/91882363434?pwd=Z1NzclFvR3VvS01uUEtNeGpMTGtxdz09',
            'evaluation_method':'主にレポート、期末試験',
            'extra':'講義・演習の出席、演習での割り当て問題の解答、理解度チェックテスト成績も適切に加味'
        },
        '形状モデリングと可視化': {
            'url':'https://zoom.us/j/99188357630?pwd=Q2xxQ0V5QnRUbmhlKzRWZEtnVzlzZz09',
            'evaluation_method':'レポート',
            'extra':'レポートはメール提出'
        },
        '有限要素法と構造解析': {
            'url':'https://zoom.us/j/95969192926?pwd=ckdmc05mdndxYml3NjFBZzROaUxrdz09',
            'evaluation_method':'授業内の理解度確認テストとレポート',
            'extra':''
        },
        '数理演習3B': {
            'url':'https://zoom.us/j/93081493741?pwd=QjBTRkZ6MWlWTC9RdlpiOXNMNmJvdz09',
            'evaluation_method':'出席とレポートと中間試験',
            'extra':'複素数'
        }
    }
    

    for k, v in classes.items():
        if event.message.text == k:
            try:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f'URL:{v["url"]}\n評価方法:{v["evaluation_method"]}\n備考:{v["extra"]}'))
            except LineBotApiError:
                return

    

@app.route('/hello')
def hello_world():
    return 'Hello, World!'


if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
