# -*- coding: utf-8 -*-

from pythainlp.tokenize import dict_word_tokenize

text=" กรุงเทพ-เชียงราย-พระธาตุดอยตุง-ตำหนักดอยตุง-สวนแม่ฟ้าหลวง-สามเหลี่ยมทองคำ-วัดพระธาตุ"
text = text.replace('จ.', '').replace('จังหวัด','').replace('ฯ', '').replace('อ.', '')
print(dict_word_tokenize(text=text,file="word_cut.txt",engine="mm"))