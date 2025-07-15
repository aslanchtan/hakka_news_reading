from GoogleNews import GoogleNews

# 建立物件（可設定語言與地區）
googlenews = GoogleNews(lang='zh-TW', region='TW')

# 抓取首頁頭條（即時新聞）
googlenews.get_news('')

# 取得結果
results = googlenews.results()

# 顯示前幾則頭條
print("📢 即時新聞頭條：\n")
for i, news in enumerate(results[:5], start=1):  # 顯示前 5 則
    print(f"{i}. 📰 {news['title']}")
    print(f"   📍 來源：{news['media']}")
    print(f"   ⏰ 發佈時間：{news['date']}")
    print(f"   🔗 連結：{news['link']}\n")