import nltk

nltk.download("punkt_tab")
nltk.download("universal_tagset")

# sentence = """
# At eight o'clock on Thursday morning.
# Arthur didn't feel very good.
# """

sentence = """
Strait of Hormuz: President Donald Trump urged Beijing to help address disruptions on the strait. He claimed there’s been “some positive response” after reaching out to countries for help with securing the strait and warned that NATO faces a “very bad” future if allies fail to assist. • War timeline: Trump said the US and Israel have “similar objectives” in their military goals. Trump administration officials had said they expect the conflict to end within weeks. Meanwhile, Israel told CNN it plans for its military campaign to continue for at least three more weeks. • Strikes exchanged: Israel claimed it struck more than 200 targets in Iran over the past day. Meanwhile, Iran said it fired about 700 missiles and 3,600 drones at US and Israeli targets since the war started.
"""

print(f"原文：{sentence}")

tokens = nltk.word_tokenize(sentence)

print(f"分詞結果：{tokens}")

tagged = nltk.pos_tag(tokens, tagset="universal")
print(f"標註結果：{tagged}")


# === Stemming & Lemmatization（英文）===
from nltk.stem import PorterStemmer, WordNetLemmatizer

nltk.download("wordnet")

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

print("\n=== Stemming & Lemmatization ===")
wn_pos_map = {"VERB": "v", "NOUN": "n", "ADJ": "a", "ADV": "r"}
lemmatized = []
for word, pos in tagged:
    stem = stemmer.stem(word)
    wn_pos = wn_pos_map.get(pos, "n")
    lemma = lemmatizer.lemmatize(word, pos=wn_pos)
    lemmatized.append((lemma, pos))
    if word != stem or word != lemma:
        print(f"  {word:15} → Stem: {stem:15} Lemma: {lemma}")

print(f"\nLemmatization 結果：{lemmatized}")


# === Stopping & Filtering（使用 Lemma 結果）===
from nltk.corpus import stopwords

nltk.download("stopwords")
stop_words = set(stopwords.words("english"))
filtered = [(word, pos) for word, pos in lemmatized if word.lower() not in stop_words and word.isalpha()]
print(f"\n=== Stopping & Filtering ===")
print(f"過濾停用詞與標點後：{filtered}")


# =============================================================
# === ① 詞頻統計 + 文字雲 ===
# =============================================================
from collections import Counter

# 詞頻統計
words_only = [word for word, pos in filtered]
word_freq = Counter(words_only)

print("\n=== 詞頻統計 ===")
for word, count in word_freq.most_common():
    print(f"  {word:15} → {count} 次")

# 依詞性分組統計
pos_freq = Counter(pos for word, pos in filtered)
print("\n=== 詞性分佈 ===")
for pos, count in pos_freq.most_common():
    print(f"  {pos:10} → {count} 次")

# 文字雲
try:
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    # 用詞頻產生文字雲
    text = " ".join(words_only)
    wc = WordCloud(
        width=800,
        height=400,
        background_color="white",
        colormap="viridis",
    ).generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("Word Cloud")
    plt.tight_layout()
    plt.savefig("wordcloud.png", dpi=150)
    plt.show()
    print("\n文字雲已儲存為 wordcloud.png")

except ImportError:
    print("\n⚠️ 請先安裝 wordcloud 和 matplotlib：")
    print("  pip install wordcloud matplotlib")
