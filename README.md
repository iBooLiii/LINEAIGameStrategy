# Line@ 智能遊戲攻略 AI

## 📌 專案簡介
一個基於 Flask 本地伺服器與 LINE Bot 建置的遊戲攻略機器人，用戶可透過關鍵字查詢《傳說對決》等遊戲攻略，並由機器人即時回應對應內容。

## 🔧 使用技術
- Python（Flask）
- LINE Messaging API
- BeautifulSoup / requests
- TfidfVectorizer

## ⚙️ 系統架構
- 用戶透過 LINE 發送文字訊息
- 機器人接收後解析關鍵字
- 利用關鍵字爬取的攻略內容回覆
- 將數據整理成可視化圖表
- 結果存儲於 Google 雲端平台，便於後續查詢

## ✨ 核心功能
- 關鍵字即時比對與查詢
- API 回應
- 指令列表功能、預設回應邏輯

## 🔗 web 爬蟲網站
https://www.op.gg/champions
https://moba.garena.tw/pro/hot/
https://forum.gamer.com.tw/B.php?bsn=30518
