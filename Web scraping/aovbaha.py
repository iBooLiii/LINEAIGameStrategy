# 爬取巴哈姆特討論區｢傳說對決-達人文章｣
def aovbaha(x):
    import requests
    from bs4 import BeautifulSoup #解析 HTML 和 XML 
    ans ={}
    url = f'https://forum.gamer.com.tw/search.php?bsn=30518&q={x}&page=1&type=daren&advancedSearch=1&sortType=gp%27'

    # 設置User-Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
    }

    # 解析網頁內容
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到 h2 標籤（屬性是 search-result_title）
    titles = soup.find_all('h2', class_='search-result_title')

    # 抓取前3標題和網址
    for title in titles[:3]:
        link = title.find('a', href=True)  # 找到帶有 href 屬性的 <a> 標籤
        if link:
            ans[title.get_text(strip=True)] = link['href']
    return ans