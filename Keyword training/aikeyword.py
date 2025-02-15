import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# 讀取訓練資料
with open('aitraining_updated.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 轉換資料
texts = [entry["user_input"] for entry in data]
keywords = [entry["keyword"] for entry in data]

# 提取關鍵字
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# 檢查句子是否含關鍵字
y = [1 if any(k in text for k in keywords) else 0 for text in texts]

# 分割資料：訓練80%、# 測試20%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 訓練模型
model = RandomForestClassifier() #隨機森林分類器
model.fit(X_train, y_train)

# 評估模型
#y_pred = model.predict(X_test)
#print(classification_report(y_test, y_pred))

# AI 關鍵字偵測函數
def aikeyword(input_text):
    input_features = vectorizer.transform([input_text])  # 使用已經訓練好模型
    prediction = model.predict(input_features)  # 使用預測模型來判斷是否是否包含關鍵字

    #如果有關鍵字，加入matched_keywords，並去除重複
    if prediction[0] == 1:  
        matched_keywords = [k for k in keywords if k in input_text]
        matched_keywords = list(set(matched_keywords))        
        return matched_keywords if matched_keywords else "文本中不包含關鍵字"        
    else:
        # 如果預測結果不包含關鍵字
        return "文本中不包含關鍵字"

# 測試新的文本
#new_input = "明天練看看打野的勝率，感覺還是挺強的。"
#result = aikeyword(new_input)
#print(result)
