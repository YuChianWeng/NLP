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
   South Korea’s baseball team lost 4-5 in a 10th-inning thriller against Taiwan 
   in the 2026 World Baseball Classic (WBC) Group C match held at Tokyo Dome on the 8th.
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