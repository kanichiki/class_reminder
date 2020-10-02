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
from jinja2 import Environment, FileSystemLoader, select_autoescape

import os
import json

app = Flask(__name__)

# 環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = "ehF0YkL5idDvCzUiGTvqLfhbotMfetFL5jzFFK7VREjANv7N3zcASy7r6g1yECHDKba3LF/ZkYnizQUsJDVlT8t7d52EVg+2nfxcrIym50/6pxT5V1npQrx35+7Nu/qplitKaHWN5Hs6BbC3s6C/pAdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "2ea8ab957868172d5b299be619cb4c14"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


#
# template_env = Environment(
#     loader=FileSystemLoader('templates'),
#     autoescape=select_autoescape(['html', 'xml', 'json'])
# )

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


#
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     if event.reply_token == "00000000000000000000000000000000":
#         return
#
#
#     soup=scraping.load_site(URL)
#     notic_list=scraping.find_by_id(soup,"notic_list")
#     notic_students_list=scraping.find_by_id_2(soup,"notic_students_list")
#
#     notic_message=notic_list[0]["string"]+"\n"+notic_list[0]["href"]
#     notic_students_message=notic_students_list[0]["string"]+"\n"+notic_students_list[0]["href"]+"\n"+notic_students_list[0]["date"]+"\n"+notic_students_list[0]["course"]
#
#     if(event.message.text=="学科からのお知らせ"):
#         contents_notic = []
#         for i in notic_list:
#             contents_notic.append(make_template.notic_flex(i['string'], i['date'], i['href']))
#
#         line_bot_api.reply_message(
#             event.reply_token,
#             FlexSendMessage(
#                 alt_text="学科生の方へのお知らせ",
#                 contents={"type": "carousel", "contents": contents_notic}
#                 # contents=make_template.notic_flex(['string'], i['date'], i['href'])
#             )
#         )
#
#     # les = "les"
#     # template = template_env.get_template('temp.json')
#     # data = template.render(dict(items=les))
#
#     if(event.message.text=="学科生の方へのお知らせ"):
#         contents_students = []
#         for i in notic_students_list:
#             contents_students.append(make_template.students_flex(i['string'], i['course'], i['date'], i['href']))
#
#         line_bot_api.reply_message(
#             event.reply_token,
#             FlexSendMessage(
#                 alt_text="学科生の方へのお知らせ",
#                 contents={"type":"carousel","contents":contents_students}
#             )
#         )

@app.route('/hello')
def hello_world():
    return 'Hello, World!'


if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
