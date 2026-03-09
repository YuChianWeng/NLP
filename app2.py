import nltk

nltk.download("punkt_tab")
nltk.download("universal_tagset")
nltk.download('averaged_perceptron_tagger_eng')  
sentence = """
At eight o'clock on Thursday morning.
Arthur didn't feel very good.
"""

print(f"原文：{sentence}")

tokens = nltk.word_tokenize(sentence)


print(f"分詞結果：{tokens}")

tagged = nltk.pos_tag(tokens, tagset="universal")
print(f"標註結果：{tagged}")


import jieba
import jieba.posseg as pseg



sentence2 = """
2026世界棒球經典賽（WBC）預賽C組賽事進入尾聲。8日比賽中，日本以4比3擊敗澳洲，目前取得3勝戰績，確定晉級下一輪。捷克則已確定遭到淘汰，而中華隊已完成全部賽程，以2勝2敗結束小組賽，晉級與否仍需視今晚6點韓國對澳洲的比賽結果而定，以失分率來看，最低標準為韓國必須以8：3擊敗澳洲，中華隊才能晉級。
"""


print(f"原文：{sentence2}")

tokens2 = jieba.lcut(sentence2)
print(f"分詞結果：{tokens2}")

# 自訂映射到簡化標籤
tag_map = {
    "n": "NOUN",
    "nr": "NOUN",
    "ns": "NOUN",
    "v": "VERB",
    "a": "ADJ",
    "d": "ADV",
    "r": "PRON",
    "p": "ADP",
    "c": "CONJ",
    "m": "NUM",
    "t": "NOUN",
    "u": "PRT",
    "x": ".",
}

tagged2 = pseg.lcut(sentence2)
tagged2 = [(word, tag_map.get(flag, "X")) for word, flag in tagged2]
print(f"標註結果：{tagged2}")