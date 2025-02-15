# Line@ 開始運行
from flask import Flask, request # Flask創建 Web 應用
import json
from linebot import LineBotApi # LineBotApi 是 Line 的 API 接口
from linebot.models import TextSendMessage # 負責整理訊息內容給 Line API
import aikeyword # 提取關鍵字
import mobamix # 攻略函數
import writedocs # 寫入 Google Drive
import removedocs # 刪除 Google Drive 重複資料
from linebot import WebhookHandler # 處理來自 LINE 的事件並回應
import pythonjpg # 繪製圖表並上傳 Google Drive 與回傳網址


win = ['全部','打野','上路','中路','下路','輔助','勝率'] # 設定勝率關鍵字
app = Flask(__name__) # 創建 Flask 應用
processed_messages = set() # 設定處理過的訊息

@app.route("/", methods=['POST']) # 只處理 POST 請求
def linebot():
    body = request.get_data(as_text=True)  # 取得收到的訊息內容
    try:
        json_data = json.loads(body)  # JSON 格式化訊息內容
        access_token = 'access_token'
        secret = 'chanel secret'
        line_bot_api = LineBotApi(access_token)
        handler = WebhookHandler(secret)
        signature = request.headers['X-Line-Signature']  # 取得LINE的簽名
        handler.handle(body, signature)  # 處理訊息

        # 過濾重複訊息
        tk = json_data['events'][0]['replyToken']
        if tk in processed_messages: # 檢查這個訊息是否已經處理過
            return 'OK'

        # 取得 LINE 收到的訊息
        msg = json_data['events'][0]['message']['text']
        print(f"收到訊息: {msg}")
        keywords = aikeyword.aikeyword(msg) # 提取關鍵字

        #處理回覆訊息
        reply = ""
        if keywords:
            x = [[msg,keywords]]
            # 判斷是否為查詢勝率
            if all(keyword in win for keyword in keywords):
                keywords.remove('勝率')
                image_url = pythonjpg.pythonjpg(keywords[0])
                if image_url:
                    reply += f"這是分析結果圖：{image_url}\n"
            else:         
                # 關鍵字為英雄攻略      
                for keyword in keywords: 
                    print(f'{keyword}攻略:')
                    result = mobamix.mobamix(keyword)
                    if result:  # 確保有內容再加上關鍵字和攻略
                        reply += f"{keyword} 攻略:\n"
                    for i in result:
                        if isinstance(result[i], list):
                            output = '>'.join(result[i])
                        else:
                            output = result[i]
                        reply += f'{i}:\n{output}\n\n'
        if not reply:
            reply = "沒找到關鍵字喔～"
            x = [[msg, '']]

        writedocs.writedocs(x) #對話紀錄寫入 Google Drive
        processed_messages.add(tk) # 標記為已處理
        
        print(f"回應訊息: {reply}")
        line_bot_api.reply_message(tk, TextSendMessage(text=reply))  # 回傳訊息
        
    except Exception as e:
        print(f"發生錯誤: {e}")
        print(body)

    removedocs.removedocs() # 刪除 Google Drive 重複資料
    return 'OK'  # Webhook 驗證回應


if __name__ == "__main__": # 啟動 Flask 應用
    app.run()
