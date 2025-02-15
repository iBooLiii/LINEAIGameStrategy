def removedocs():
    import gspread
    gc = gspread.service_account(filename='token.json')
    # 透過 URL 來打開指定的 Google Sheets 文件
    sh = gc.open_by_url('google docs 地址')
    # 取得第 0 個工作表（即第一個工作表）
    worksheet = sh.get_worksheet(0)

    # 讀取所有資料
    rows = worksheet.get_all_values()

    # 用來追蹤已經出現過的值（例如第一欄的值）
    seen = set()

    # 準備一個要刪除的行列表
    rows_to_delete = []

    # 檢查是否有重複項目
    for idx, row in enumerate(rows):
        value1 = row[0]
        if value1 in seen:
            rows_to_delete.append(idx + 1)  # Google Sheets 索引從 1 開始
        else:
            seen.add(value1)

    # 刪除重複的行（從後向前刪除，避免刪除影響後續行的索引）
    for row_idx in reversed(rows_to_delete):
        worksheet.delete_rows(row_idx)

removedocs()