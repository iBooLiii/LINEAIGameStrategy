# 獲取特定路線勝率資料
def winrate(url):
    import requests
    from bs4 import BeautifulSoup
    
    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
            }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # 初始化英雄資料列表
    champions_data = [] 
    champion_rows = soup.find_all("tr")

    for row in champion_rows:
        # 爬取英雄
        champion_name_element = row.find("strong", class_="flex-1 truncate text-xs max-[420px]:sr-only")
        if champion_name_element:
            champion_name = champion_name_element.get_text(strip=True)
        else:
            champion_name = None

        # 爬取勝率
        win_rate_element = row.find("td", class_="text-xs text-gray-600")
        if win_rate_element:
            win_rate = win_rate_element.get_text(strip=True)
        else:
            win_rate = None
        
        # 爬取選取率
        pick_rate_elements = row.find_all("td", class_="text-xs text-gray-600")
        if pick_rate_elements:
            pick_rate = pick_rate_elements[1].get_text(strip=True)
        else:
            pick_rate = None
        
        if champion_name and win_rate and pick_rate:
            champions_data.append((champion_name, win_rate, pick_rate))

    return champions_data

