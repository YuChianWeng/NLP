from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from dotenv import load_dotenv
import os
load_dotenv()
from pprint import pprint

credential = AzureKeyCredential(os.getenv("AZURE_LANGUAGE_KEY"))
text_analytics_client = TextAnalyticsClient(
    endpoint=os.getenv("AZURE_LANGUAGE_ENDPOINT"), 
    credential=credential,
    default_language="zh"
)

documents = [
    "難得抽到客家幣～剛好可以來桃園玩！今天以漫威影迷的身分入住中壢賓利酒店，第一眼看到大廳滿滿的角色公仔，真的有種瞬間進入英雄宇宙的興奮感！無論是鋼鐵人、雷神還是美國隊長，都擺得超氣勢，在等待辦理入住的時間完全不無聊，還忍不住多拍了好幾張照片。房間乾淨舒適，設計感也不錯，住起來相當放鬆。最讓人意外的是早餐選擇很多，中西式都有，從熱食、沙拉到甜點都很用心，對喜歡慢慢享受早餐的人來說超加分。整體入住體驗像是英雄迷的小確幸行程，入住一晚彷彿補滿能量值。"
]
result = text_analytics_client.analyze_sentiment(
    documents, 
    show_opinion_mining=True
)
docs = [doc for doc in result if not doc.is_error]

print("Let's visualize the sentiment of each of these documents")
for idx, doc in enumerate(docs):
    print(f"Document text: {documents[idx]}")
    pprint(vars(doc))
    print(f"Overall sentiment: {doc.sentiment}")
    print("=="*20)
    print(f"整體情緒分析： {doc.sentiment}")
    i = 1 
    for sentence in doc.sentences:
        print(f"{i}.{sentence.text} : {sentence.sentiment}(",end="")
        o = True
        for opinion in sentence.mined_opinions:
            if(o):
                print(f"{opinion.target.text}", end="")
                o = False
            else:
                print(f",{opinion.target.text}" , end="")
        i += 1
        print(")")


    