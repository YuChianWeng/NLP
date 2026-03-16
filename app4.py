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