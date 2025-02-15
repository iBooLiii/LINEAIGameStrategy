# 繪製英雄勝率圖片並上傳至 Google Drive
import matplotlib
matplotlib.use('Agg')  # 使用非交互式後端
import matplotlib.pyplot as plt
from matplotlib import font_manager
import winrate
from io import BytesIO
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import time

def pythonjpg(a):
    position = {'全部': 'all', '上路': 'top', '打野': 'jungle', '中路': 'mid', '下路': 'adc', '輔助': 'support'}
    url = f"https://www.op.gg/champions?position={position.get(a, 'all')}" # 提供了預設值避免錯誤
    
    # 設置字體
    font_path = "C:/Windows/Fonts/msyh.ttc"
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rc('font', family=font_prop.get_name())

    # 獲取英雄勝率資料
    try:
        champions_data = winrate.winrate(url)
    except Exception as e:
        print(f"獲取資料失敗: {e}")
        return None

    # 分割英雄、勝率、選取率
    x, y, labels = [], [], []
    for champion, win_rate, pick_rate in champions_data:
        x.append(float(pick_rate.replace("%", "")))
        y.append(float(win_rate.replace("%", "")))
        labels.append(champion)

    # 繪製散點圖
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(x, y, c=y, cmap='jet', s=100)
    for i, label in enumerate(labels):
        plt.text(x[i], y[i] + 0.1, label, fontsize=10.5, va='bottom', ha='center', color='black')

    # 設置圖表標籤
    plt.title(f"LOL-{a}前幾強分析")
    plt.xlabel("選取率 (%)")
    plt.ylabel("勝率 (%)")
    plt.grid(axis='y')
    plt.colorbar(scatter)

    # 儲存圖片到位元組流
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()
    image_stream.seek(0)

    # 設置圖片名稱
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    image_filename = f"champions_scatterplot_{timestamp}.jpg"

    # 設置 Google Drive 金鑰
    SCOPES = ['google drive 地址']
    SERVICE_ACCOUNT_FILE = 'driveupload.json'

    try:
        # 上傳至 Google Drive
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)

        UPLOAD_FOLDER = '資料夾ID'
        media = MediaIoBaseUpload(image_stream, mimetype='image/png')
        file_metadata = {'name': image_filename, 'parents': [UPLOAD_FOLDER]}
        
        file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        file_id = file.get("id") # 獲取上傳檔案ID

        # 設置公開
        service.permissions().create(fileId=file_id, body={'type': 'anyone', 'role': 'reader'}).execute()
        return f"https://drive.google.com/uc?id={file_id}"

    except Exception as e:
        print(f"上傳 Google Drive 失敗: {e}")
        return None

#x = ['中路', '勝率']
#if '勝率' in x:
#   x.remove('勝率')

#print(pythonjpg(x[0]))




