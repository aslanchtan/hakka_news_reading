import re
from gtts import gTTS
import os
from dotenv import load_dotenv

# def split_chinese_english_segments(text):
#     pattern = r'[a-zA-Z\']+|[^a-zA-Z\']+'
#     return re.findall(pattern, text)

# def split_smart_segments(text):
#     def is_english_char(c):
#         return c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
#     def is_punctuation(c):
#         return c in " ，。'\",()0123456789:!?."

#     segments = []
#     if not text:
#         return segments

#     current = text[0]
#     is_eng = is_english_char(current)
#     print(is_eng)
#     for c in text[1:]:
#         if is_punctuation(c):
#             current += c
#         elif is_english_char(c) == is_eng:
#             current += c
#         else:
#             segments.append(current)
#             current = c
#             is_eng = is_english_char(c)

#     segments.append(current)
#     return [seg for seg in segments if seg.strip()]  # 移除全是空白的段落




# a = "另外，明代士人徐應秋所撰《玉芝堂談蕙．卷十》也有收錄幾則男扮女裝的江湖傳聞，例如廣州有位雌雄同體的尼姑，仗 著出家人身分與身體的特殊從事不法(涉詐騙、淫亂以及間諜行為)或是男孩從小被養父母當成女孩養大、學習不少歌舞，以此賣藝為生，最終被識破身分。"

# b = split_smart_segments(a)

# print(b)
# print('找'.isdigit())
# print("找".isalpha())



load_dotenv()  # 讀取 .env 檔案
url = os.getenv("url")
ttsUrl = os.getenv("ttsUrl")
username = os.getenv("account")
password = os.getenv("password")
print("🔍 DEBUG:", url, ttsUrl, username, password)


