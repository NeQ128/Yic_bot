from flask import Flask,request,abort
from linebot import (LineBotApi , WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from bot_1A2B import game as game_1A2B

import os

app = Flask(__name__)
#Channel access token
line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
#Channel secret
hander = WebhookHandler(os.environ['CHANNEL_SECRET'])

player_list = {}

#監聽所有來自 /callback 的 Post Request
@app.route('/callback',methods=['POST'])
def callback():
    #get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    #get request body as text
    body = request.get_data(as_text=True)
    app.logger.info('Request body : '+ body)
    #handle webhook body
    try:
        hander.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

#處理訊息
@hander.add(MessageEvent,message=TextMessage)
def handle_message(event):
    message = '輸入錯誤，請重新輸入'
    game_end = False

    profile = line_bot_api.get_profile(event.source.user_id)
    player_id = profile.user_id
    player_message = str(event.message.text)
    if player_message.startswith('開始新遊戲:'):
        if player_id in player_list.keys():
            player_list.pop(player_id)
        
        player_list[player_id] = {}
        
        game_type = player_message.split('開始新遊戲:')[1]
        if game_type.startswith('1A2B'):
            mode = game_type.split('_')[1] if len(game_type.split('_')) == 2 else '4'
            if game_1A2B.Mode_Check(mode):
                player_list[player_id]['game_type'] = '1A2B'
                player_list[player_id]['game_mode'] = int(mode)
                player_list[player_id]['game_answer'] = game_1A2B.Answer_Make(player_list[player_id]['game_mode'])
                message = f'1A2B({mode})遊戲已開始'

    elif player_id in player_list.keys():
        game_type = player_list[player_id]['game_type']
        if game_type == '1A2B':
            player_list[player_id]['user_input'] = player_message
            if game_1A2B.Input_Check(player_list[player_id]):
                player_list[player_id],game_end = game_1A2B.Answer_Check(player_list[player_id])
                message = player_list[player_id]['game_message']
                if game_end:
                    player_list.pop(player_id)

    if player_id not in player_list.keys() and not game_end:
        message = TemplateSendMessage(alt_text='ConfirmTemplate',
            template=ConfirmTemplate(
                text='請選擇要開始的遊戲↓',
                actions=[
                    MessageAction(
                        label='1A2B(4字)',
                        text='開始新遊戲:1A2B'
                    ),
                    MessageAction(
                        label='1A2B(5字)',
                        text='開始新遊戲:1A2B_5'
                    )
                ]
            )
        )
    else:
        message = TextSendMessage(message)

    line_bot_api.reply_message(event.reply_token,message)

if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0',port=port)
