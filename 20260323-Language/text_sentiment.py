from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from dotenv import load_dotenv
import os
load_dotenv()

credential = AzureKeyCredential(os.getenv("AZURE_LANGUAGE_KEY"))
text_analytics_client = TextAnalyticsClient(
    endpoint=os.getenv("AZURE_LANGUAGE_ENDPOINT"), 
    credential=credential
)

documents = [
    "The breakfast was good.",
    "The room is ok.",
    "The hotel was not clean."
]

result = text_analytics_client.analyze_sentiment(
    documents, 
    show_opinion_mining=True
)
docs = [doc for doc in result if not doc.is_error]

print("Let's visualize the sentiment of each of these documents")
for idx, doc in enumerate(docs):
    print(f"Document text: {documents[idx]}")
    print(f"Overall sentiment: {doc.sentiment}")