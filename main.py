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
    # classes = [
    #     {"class_name":"基礎プロジェクト","zoom_url":"https://zoom.us~",}
    # ]

    try:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))
    except LineBotApiError:
        return

@app.route('/hello')
def hello_world():
    return 'Hello, World!'


if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
