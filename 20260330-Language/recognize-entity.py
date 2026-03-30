import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from dotenv import load_dotenv
load_dotenv(override=True)

endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
key = os.getenv("AZURE_LANGUAGE_KEY")

text_analytics_client = TextAnalyticsClient(
    endpoint=endpoint, 
    credential=AzureKeyCredential(key)
)

reviews = [
    "以色列繼續大規模轟炸伊朗，油價27日勁揚引發賣壓，美股主要指數均收黑，台股今天（30日）早盤開低下跌逾600點，最低32430點。權王台積電早盤失守1800元，下跌40元，低見1780元。",
]

result = text_analytics_client.recognize_entities(
    reviews,
    language="zh-Hant"
)
result = [review for review in result if not review.is_error]

for idx, review in enumerate(result):
    for entity in review.entities:
        print(f"Entity '{entity.text}' has category '{entity.category}'")
