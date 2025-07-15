import requests
from bs4 import BeautifulSoup
import re
from deep_translator import GoogleTranslator
import tts_main

if __name__ == '__main__':

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    # Step 1: 擷取新聞列表頁
    url = 'https://www.ettoday.net/news/news-list.htm'
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # Step 2: 抓第一則有效新聞連結
    news_items = soup.select('div.part_list_2 a')
    news_url = None
    for a in news_items:
        href = a['href']
        if '/news/' in href and href.startswith('https://'):
            news_url = href
            break

    if not news_url:
        print("❌ 找不到新聞連結")
        exit()

    # Step 3: 抓新聞內容
    res = requests.get(news_url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    title = soup.find('h1', class_='title').text.strip()
    time = soup.find('time').text.strip()
    content_div = soup.find('div', class_='story')
    paragraphs = content_div.find_all('p')

    translator = GoogleTranslator(source='auto', target='zh-TW')

    # Step 4: 處理段落並翻譯英文
    translated_paragraphs = []
    num = 2

    for p in paragraphs:
        # ❗ 移除所有圖說 strong 標籤內容（但保留其他文字）
        figcaption = p.find_all('strong')
        if figcaption:
            for _ in figcaption:
                _.extract()  # ✅ 從 HTML 樹中移除圖說元素

        text = p.get_text(strip=True)
        if not text:
            continue

        # 若含英文則翻譯
        if re.search(r'[a-zA-Z]', text):
            try:
                translated = translator.translate(text)
                print(f"🌐 翻譯原文：{text}\n➡️ 翻譯後：{translated}\n")
                text = translated
            except Exception:
                print("⚠️ 翻譯錯誤，保留原文：", text)

        translated_paragraphs.append(text)
        num = num + 1

    # Step 5: 整合成完整內文
    content = '\n'.join(translated_paragraphs)
    full_text = f"{title}\n{time}\n{content}"

    # Step 6: 儲存為 txt 檔案
    safe_title = re.sub(r'[\\/*?:"<>|]', '', title)
    filename = f"news/ETtoday_{safe_title}.txt"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(full_text)

    print(f"\n✅ 已儲存新聞至檔案：{filename}")
    # return filename, num


    
    # file_status = web_crawling()

    tts_main.tts_api(filepath = filename, threadcount = num)
