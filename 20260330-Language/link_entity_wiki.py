import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from dotenv import load_dotenv
load_dotenv(override=True)
from pprint import pprint

endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
key = os.getenv("AZURE_LANGUAGE_KEY")

text_analytics_client = TextAnalyticsClient(
    endpoint=endpoint, 
    credential=AzureKeyCredential(key)
)

documents = [
    """
   President Donald Trump said Iran has agreed to “most of” the 15-point list of demands from the US to end the war. Last week, however, Tehran had not immediately accepted the plan and signaled skepticism of Washington’s position. Trump added he’s still considering whether to seize key fuel hub Kharg Island, and claimed there has been “regime change” in Iran.
    """
]

result = text_analytics_client.recognize_linked_entities(
    documents,
)
docs = [doc for doc in result if not doc.is_error]

for idx, doc in enumerate(docs):
    print(f"Document text: {documents[idx]}")
    pprint(vars(doc))


print(
    "Let's map each entity to it's Wikipedia article. I also want to see how many times each "
    "entity is mentioned in a document\n\n"
)
entity_to_url = {}
for doc in docs:
    for entity in doc.entities:
        print("Entity '{}' has been mentioned '{}' time(s)".format(
            entity.name, len(entity.matches)
        ))
        if entity.data_source == "Wikipedia":
            entity_to_url[entity.name] = entity.url
print("All items with a Wikipedia URL: ")
pprint(entity_to_url)


import wikipediaapi

wiki_zh = wikipediaapi.Wikipedia('ryan-agent-zh', 'zh')
wiki_en = wikipediaapi.Wikipedia('ryan-agent-en', 'en')

for entity_name, url in entity_to_url.items():
    page_py_zh = wiki_zh.page(entity_name)
    page_py_en = wiki_en.page(entity_name)
    if page_py_zh.exists():
        print(f"{entity_name} \n")
        print(f"摘要 : {page_py_zh.summary}")
        print("=="*20)
    if page_py_en.exists():
        print(f"{entity_name} \n")
        print(f"Summary : {page_py_en.summary}")
        print("=="*20)
    
