# 爬取英雄聯盟 op.gg 英雄攻略
def lolopgg(x):
    import requests
    from bs4 import BeautifulSoup

    heros = {
    '阿卡麗': 'akali', '安妮': 'annie', '艾希': 'ashe', '布朗姆': 'braum', '卡特琳娜': 'katarina',
    '凱莎': 'kaiSa', '卡瑪': 'karma', '李星': 'leesin', '路西恩': 'lucian', '瑪爾札哈': 'malzahar',
    '奧恩': 'ornn', '賽恩': 'sion', '索拉卡': 'Soraka', '塔莉雅': 'Taliyah', '維克托': 'Viktor',
    '贾克斯': 'Jax', '辛吉德': 'Singed', '蛇女': 'Cassiopeia', '烏迪爾': 'Udyr', '約里克': 'Yorick',
    '佐伊': 'Zoe', '齊勒斯': 'Xerath', '艾瑞莉亞': 'Irelia', '賽勒斯': 'Sylas', '希維爾': 'Sivir',
    '星朵拉': 'Syndra', '提摩': 'Teemo', '菲艾': 'Vi', '雷茲': 'Ryze', '艾克': 'Ekko',
    '蒙多醫生': 'DrMundo', '凱特琳': 'Caitlyn', '希瓦娜': 'Shyvana', '極靈': 'Zilean',
    '巴德': 'Bard', '姍娜': 'Senna', '悠咪': 'Yuumi', '布里茨': 'Blitzcrank', '科加斯': 'Chogath',
    '拉克絲': 'Lux', '雷文': 'Riven', '凱爾': 'Kayle', '嘉文四世': 'JarvanIV', '茂凯': 'Maokai',
    '阿璃': 'Ahri', '泰達米爾': 'Talon', '寇格魔': 'KogMaw', '葵恩': 'Quinn', '伊澤瑞爾': 'Ezreal',
    '賽恩': 'Sion', '赫克林': 'Hecarim', '維克多': 'Viktor', '魔甘娜': 'Morgana',
    '崔絲塔娜': 'Tristana', '卡爾瑟斯': 'Karthus', '燼': 'Jhin', '卡莎碧雅': 'Cassiopeia',
    '瑟菈紛': 'Seraphine', '菲歐拉': 'Fiora', '娜米': 'Nami', '卡蜜兒': 'Camille',
    '銳兒': 'Rell', '妮可': 'Neeko', '凱能': 'Kennen', '達瑞斯': 'Darius',
    '埃爾文': 'Ivern', '貝爾薇斯': 'Belveth', '烏爾加特': 'Urgot', '珍娜': 'Janna', '瑟雷西': 'Thresh',
    '努努和威朗普': 'Nunu', '塔莉雅': 'Taliyah', '斯溫': 'Swain', '巴德': 'Bard',
    '睿娜妲': 'Renata', '吶兒': 'Gnar', '古拉格斯': 'Gragas', '剎雅': 'Xayah',
    '扎克': 'Zac', '雷歐娜': 'Leona', '露璐': 'Lulu'
    }

    url = f'https://www.op.gg/champions/{heros[x]}/build/?hl=zh_TW'
    
    # 取得網頁內容
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    runes = []
    skill = []
    skillorder = []
    equipment = []
    data = {}

    #抓取勝率
    win_rate_elements = soup.find_all("li", class_="flex justify-between border-b-[1px] pb-1.5")
    for element in win_rate_elements:
        label = element.find("em", class_="text-[12px] not-italic text-gray-500")
        if label and "勝率" in label.text:
            win_rate = element.find("b", class_="text-[12px]")
            if win_rate:
                data["勝率"] = f"{win_rate.text.strip()}"

    # 抓取符文名字
    target_classes = ["overflow-hidden", "rounded-[50%]", "bg-[#000]", "hover:bg-[#000]", "size-6", "md:size-7",
                      "mx-auto"]
    img_elements = soup.find_all("img", class_=target_classes, alt=True)
    for img_tag in img_elements:
        classes = img_tag.get('class', [])
        if any("opacity-100" in cls for cls in classes):
            alt_text = img_tag["alt"]
            if alt_text not in runes:  # 檢查勝率是否有在
                runes.append(alt_text)  # 提取勝率較高的符文
                data["符文"] = runes

    #抓取召喚師技能
    class_name = "flex h-[46px] items-center gap-1 md:h-12"
    elements = soup.find_all(class_=class_name)
    for element in elements[0:1]:
        img_tags = element.find_all("img", alt=True)
        if len(img_tags) > 1:
            skill.append(img_tags[0]["alt"])
            skill.append(img_tags[1]["alt"])
            data["召喚師技能"] = skill

    #抓取技能順序
    class_name = "relative cursor-pointer w-[32px]"
    elements = soup.find_all(class_=class_name)
    for element in elements:
        img_tags = element.find_all("img", alt=True)
        for img in img_tags:
            skillorder.append(img["alt"])
            data["技能順序"] = skillorder

    #裝備順序
    class_name = "flex-start flex flex-wrap items-center gap-1 whitespace-pre-wrap"
    elements = soup.find_all(class_=class_name)
    for element in elements[0:1]:
        img_tags = element.find_all("img", alt=True)
        for img in img_tags:
            equipment.append(img["alt"])
            data["裝備順序"] = equipment

    return data