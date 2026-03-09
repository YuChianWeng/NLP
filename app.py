import nltk
nltk.download("punkt_tab")
nltk.download("universal_tagset")

sentence = """
At eight o'clock on Thursday morning.
Arthur didn't feel very good.
"""

print(f"原文：{sentence}")

tokens = nltk.word_tokenize(sentence)
print(f"分詞結果：{tokens}")

import jieba

sentence2 = """
禮拜四早上八點鐘。
阿瑟覺得不太舒服。
"""

print(f"原文：{sentence2}")

tokens2 = jieba.lcut(sentence2)
print(f"分詞結果：{tokens2}")