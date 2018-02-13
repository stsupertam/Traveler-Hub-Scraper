# -*- coding: utf-8 -*-

from pythainlp.tokenize import dict_word_tokenize

text="จ.อุดรฯ"
print(dict_word_tokenize(text=text,file="tag.txt",engine="mm"))