import nltk

#sentence = """
#At eight o'clock on Thursday morning.
#Arthur didn't feel very good.
#"""

sentence = """
餐點偏鹹一點，但味道還不錯，人很多、空間大、服務好，酒自備的話，一桌9000左右，有提供停車位，有提供幼兒座椅

"""


nltk.download("vader_lexicon")

from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

# 分析原文
print("\n=== 情感分析（VADER）===")
print(f"\n原文：{sentence.strip()}")
scores = sia.polarity_scores(sentence)
print(
    f"詞數比例：正面{scores['pos']*100:.2f}% VS. 中性 {scores['neu']*100:.2f}% VS. 負面 {scores['neg']*100:.2f}%"
)
if scores["compound"] >= 0.05:
    sentiment = "😊 正面"
elif scores["compound"] <= -0.05:
    sentiment = "😞 負面"
else:
    sentiment = "😐 中性"
print(f"情感強度分數(compound)：{scores['compound']:.3f} {sentiment}")

# 個別句子分析
test_sentences = [
    "At eight o'clock on Thursday morning.",
    "Arthur didn't feel very good."
]

print("\n=== 多句情感分析 ===")
for s in test_sentences:
    print(f"\n句子：{s}")
    scores = sia.polarity_scores(s)
    compound = scores["compound"]
    if compound >= 0.05:
        label = "正面 😊"
    elif compound <= -0.05:
        label = "負面 😞"
    else:
        label = "中性 😐"
    print(f"情感強度分數(compound)：{compound:.3f} {label}")
