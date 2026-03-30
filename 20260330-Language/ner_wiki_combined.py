import os
import requests
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from dotenv import load_dotenv
load_dotenv(override=True)


def fetch_wiki_summary(wiki_url: str) -> str:
    """Fetch the first paragraph summary from Wikipedia REST API."""
    # Extract page title from URL: https://en.wikipedia.org/wiki/PAGE_TITLE
    title = wiki_url.split("/wiki/")[-1]
    api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    try:
        resp = requests.get(api_url, timeout=5,
                            headers={"User-Agent": "ner-wiki-demo/1.0"})
        if resp.status_code == 200:
            return resp.json().get("extract", "(no summary)")
        return f"(HTTP {resp.status_code})"
    except requests.RequestException as e:
        return f"(request failed: {e})"

endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
key = os.getenv("AZURE_LANGUAGE_KEY")

client = TextAnalyticsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

documents = [
    """
    President Donald Trump said Iran has agreed to “most of” the 15-point list of demands from the US to end the war. Last week, however, Tehran had not immediately accepted the plan and signaled skepticism of Washington’s position. Trump added he’s still considering whether to seize key fuel hub Kharg Island, and claimed there has been “regime change” in Iran.
    """
]

# ── 1. NER: 人事時地物 analysis ──────────────────────────────────────────────

# Map Azure NER categories to 人事時地物
CATEGORY_MAP = {
    "Person":           "人 (Person)",
    "Organization":     "事 (Organization/Event)",
    "Event":            "事 (Organization/Event)",
    "DateTime":         "時 (Time)",
    "Location":         "地 (Location)",
    "Product":          "物 (Thing/Product)",
    "Skill":            "物 (Thing/Product)",
    "PhoneNumber":      "物 (Thing/Product)",
    "URL":              "物 (Thing/Product)",
    "IPAddress":        "物 (Thing/Product)",
    "Quantity":         "物 (Thing/Product)",
}

ner_result = client.recognize_entities(documents)
ner_docs = [doc for doc in ner_result if not doc.is_error]

print("=" * 60)
print("  人事時地物 NER Analysis")
print("=" * 60)

buckets = {
    "人 (Person)": [],
    "事 (Organization/Event)": [],
    "時 (Time)": [],
    "地 (Location)": [],
    "物 (Thing/Product)": [],
}

for doc in ner_docs:
    for entity in doc.entities:
        label = CATEGORY_MAP.get(entity.category, f"物 (Thing/Product)")
        buckets[label].append(
            f"{entity.text!r}  [category={entity.category}, confidence={entity.confidence_score:.2f}]"
        )

for label, items in buckets.items():
    print(f"\n{label}:")
    if items:
        for item in items:
            print(f"  • {item}")
    else:
        print("  (none found)")

# ── 2. Entity Linking: Wikipedia summaries ───────────────────────────────────

link_result = client.recognize_linked_entities(documents)
link_docs = [doc for doc in link_result if not doc.is_error]

print("\n" + "=" * 60)
print("  Wikipedia Entity Links")
print("=" * 60)

for doc in link_docs:
    for entity in doc.entities:
        if entity.data_source == "Wikipedia":
            mentions = len(entity.matches)
            summary = fetch_wiki_summary(entity.url)
            print(f"\n• {entity.name}")
            print(f"  Mentioned : {mentions} time(s)")
            print(f"  Wikipedia : {entity.url}")
            print(f"  Summary   : {summary}")
