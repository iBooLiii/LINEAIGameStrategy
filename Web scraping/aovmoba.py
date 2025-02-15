#爬取傳說對決官方攻略
#奧義,技能點法,連招技巧,出裝順序.特長
def aovmoba(x):   
    import requests
    from bs4 import BeautifulSoup #解析 HTML 和 XML 

    # 英雄對應資料位子
    heros = {'牛魔王':20,'歐米茄':35,'美娜':None,'薩尼':38,'哥德爾':26,
            '查戈納爾':24,'渥馬爾':29,'塔拉':31,'贊尼爾':None,'阿杜恩':None,
            '麥克思':529,'伯頓':659,'諾可西':660,'古木':None,'維羅':None,
            '阿塔':920,'瑟斐斯':32,'呂布':39,'趙雲':34,'馬洛斯':160,
            '莫托斯':None,'愛里':237,'司科德':None,'祖卡':None,'超人':None,
            '凱格路士':None,'龍馬':None,'艾翠絲':None,'神力女超人':None,'夜叉':None,
            '洛克':605,'艾蜜莉':669,'瑞克':678,'緋淚':769,'弗洛倫':805,
            '埃羅':None,'葉娜':839,'筱清':None,'安格列':None,'亞連':None,
            '青硯':None,'霧己':None,'夜姬':None,'刀鋒':18,'納克羅斯':None,
            '悟空':173,'科里納卡':216,'蝙蝠俠':None,'拉茲':None,'莫拉':None,
            '齊爾':None,'閃電俠':591,'奎倫':728,'銀晝':None,'綺蘿':None,
            '潘因':921,'颯枷':None,'蘇離':None,'星葵':None,'布萊特':None,
            '薇菈':37,'阿茲卡':27,'盧蜜亞':None,'蘿兒':None,'貂蟬':41,
            '阿萊斯特':106,'克里希':25,'卡莉':21,'穆加爵':36,'普雷塔':None,
            '娜塔亞':132,'金納':137,'伊耿士':None,'圖倫':None,'莉莉安':552,
            '瑪迦':658,'瀾':752,'達爾西':None,'依夏':None,'狄拉克':None,
            '伊格':None,'洛里昂':None,'令月':None,'堇':23,'勇':40,
            '凡恩':19,'菲尼克':94,'史蘭茲':None,'特爾安娜絲':None,'小丑':None,
            '摩恩':None,'琳蒂':None,'靈靈':569,'蘇':695,'亥犽':817,
            '卡芬妮':798,'希露卡':None,'蘭鐸':None,'拉維爾':922,'索文':None,
            '緹莉':None,'愛麗絲':33,'克萊斯':122,'夸克':70,'朗博':113,
            '海倫':164,'提米':None,'艾瑞':629,'安奈特':None,'皮皮':None,
            '卡瑞茲':None,'若伊':923,'芽芽':None}
    
    data = {}
    if heros[x]:
        url = f'https://moba.garena.tw/pro/show/{heros[x]}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
    
        # 抓取奧義
        runes_names = soup.find_all(class_='items-runes__main-item-name')
        runes_list = [rune.text for rune in runes_names]
        data["奧義"] = runes_list

        # 抓取技能點法
        start_text = "技能點法："
        start_element = soup.find('span', string=start_text)
        if start_element:
            skill_points = []
            table = start_element.find_next('table')
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                for cell in cells:
                    skill = cell.text.strip()
                    if skill and skill not in ['等級', '→', 'V',] and not skill.isdigit():
                        skill_points.append(skill)
            data["技能點法"] = skill_points

        # 抓取連招技巧
        start_text = "連招技巧："
        start_element = soup.find('span', string=start_text)
        if start_element:
            combo_skills = []
            table = start_element.find_next('table')
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                skill_sequence = [cell.text.strip() for cell in cells if cell.text.strip() != '']  # 去除空白
                skill_sequence = [skill for skill in skill_sequence if skill != '→']
                combo_skills.extend(skill_sequence)
            cleaned_skills = [skill.replace('\r\n\t\t\t', '') for skill in combo_skills]
            data["連招技巧"] = cleaned_skills

        #抓取出裝1
        start_text = "順風局出裝："
        start_element = soup.find('span', string=start_text)
        if start_element:
            item_list = []
            next_elements = start_element.find_all_next(text=True)
            for text in next_elements[1:]:
                if "：" in text: 
                    item_name = text.split("：")[0].strip()
                    item_name = item_name.replace("「", "").replace("」", "")
                    item_list.append(item_name)
                if "技能點法" in text or "連招技巧" in text:
                    break
            item_list = [item for item in item_list if item not in ['開場兩種打野路線', '評語','總結']]
            item_list = [item for item in item_list if item]
            if item_list: 
                data["出裝順序"] = item_list[:6]

        #抓取出裝2
        start_text = "順風局出裝說明："
        start_element = soup.find('span', string=start_text)
        if start_element:
            item_list = []
            next_elements = start_element.find_all_next(text=True)
            for text in next_elements[1:]:
                if "：" in text: 
                    item_name = text.split("：")[0].strip()
                    item_name = item_name.replace("「", "").replace("」", "")
                    item_list.append(item_name)
                if "技能點法" in text or "連招技巧" in text:
                    break
            item_list = [item for item in item_list if item not in ['開場兩種打野路線', '評語','總結']]
            item_list = [item for item in item_list if item]
            if item_list: 
                data["出裝順序"] = item_list[:6]

        #抓取出裝3
        start_text = "順風局出裝順序："
        start_element = soup.find('span', string=start_text)
        if start_element:
            item_list = []
            next_elements = start_element.find_all_next(text=True)
            for text in next_elements[1:]:
                if "：" in text: 
                    item_name = text.split("：")[0].strip()
                    item_name = item_name.replace("「", "").replace("」", "")
                    item_list.append(item_name)
                if "技能點法" in text or "連招技巧" in text:
                    break
            item_list = [item for item in item_list if item not in ['開場兩種打野路線', '評語','總結']]
            item_list = [item for item in item_list if item]
            if item_list: 
                data["出裝順序"] = item_list[:6]

        #抓取特長
        start_text = "特長："
        start_element = soup.find('span', string=start_text)
        if start_element:
            description = start_element.find_next_sibling(text=True).strip()
            data["特長"] = description
        
    return data
