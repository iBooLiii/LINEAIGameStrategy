# 將資料寫入 Google Docs
def writedocs(x):
    import gspread

    # 設定金鑰與地址
    gc = gspread.service_account(filename='token.json')
    sh = gc.open_by_url('google docs 地址')
    worksheet = sh.get_worksheet(0)

    # 儲存資料，設定空集合
    existing_data = worksheet.get_all_values()
    processed_keywords = set()

    # 整理資料格式
    for row in x:
        value1 = row[0]
        if isinstance(row[1], list):
            value2_value3 = ",".join(row[1])
        else:
            value2_value3 = row[1]

        # 檢查資料是否已經存在
        if (value1, value2_value3) in processed_keywords:
            continue

        # 檢查資料是否已經存在於 Google Docs
        data_exists = False
        for existing_row in existing_data:
            if existing_row[0] == value1 and existing_row[1] == value2_value3:
                data_exists = True
                break

        if not data_exists:
            worksheet.append_row([value1, value2_value3])
        
        # 標記此關鍵字為已處理
        processed_keywords.add((value1, value2_value3))
