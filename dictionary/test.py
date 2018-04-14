# -*- coding: utf-8 -*-

from pythainlp.tokenize import dict_word_tokenize

text=" กรุงเทพ-เชียงราย-พระธาตุดอยตุง-ตำหนักดอยตุง-สวนแม่ฟ้าหลวง-สามเหลี่ยมทองคำ-วัดพระธาตุ"
text = text.replace('จ.', '').replace('จังหวัด','').replace('ฯ', '').replace('อ.', '')

with open('../dictionary/word_cut.txt', 'r', encoding="utf8") as file:
    word = file.readlines()
print(len(max(word, key=len)))
print(dict_word_tokenize(text=text,file="../dictionary/word_cut.txt",engine="mm"))