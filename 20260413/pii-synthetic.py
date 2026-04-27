import os
import requests
import json
from dotenv import load_dotenv
load_dotenv(override=True)

endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
key = os.getenv("AZURE_LANGUAGE_KEY")

# 必須使用 2025-11-15-preview 版本
api_url = f"{endpoint}/language/:analyze-text?api-version=2025-11-15-preview"

headers = {
    "Ocp-Apim-Subscription-Key": key,
    "Content-Type": "application/json",
}

# target_text = """
# John's phone number is 123-456-7890.
# """

target_text = """ Hi Support - My name is Julie Walsh. I tried to purchase a life insurance policy online yesterday however the site said, "an unexpected error occurred." I tried to pay with a credit card. My DOB is 02-10-97 and SSN is 523-23-6145. Could you take a look on your end? """

body = {
    "kind": "PiiEntityRecognition",
    "parameters": {
        "modelVersion": "latest",
        "redactionPolicy": {
            "policyKind": "syntheticReplacement"  # 用假資料替換 PII
            # "policyKind": "noMask"  # 不遮蔽 PII，僅回傳辨識結果
            # "policyKind": "characterMask",  # 使用自訂遮蔽字元
            # "redactionCharacter": "#"  # 自訂遮蔽字元為 "#"
            # "policyKind": "entityMask" # 用類別名稱替換 PII，例如 [PHONE_NUMBER]、[CREDIT_CARD_NUMBER] 等
        }
    },
    "analysisInput": {
        "documents": [
            {
                "id": "1",
                "language": "en",
                "text": target_text
            }
        ]
    }
}

response = requests.post(api_url, headers=headers, json=body)
result = response.json()

# 取出遮蔽後的文字
if "results" in result:
    for doc in result["results"]["documents"]:
        print(f"\n原文: {body['analysisInput']['documents'][0]['text']}")
        print(f"替換後: {doc['redactedText']}")
        for entity in doc["entities"]:
            print(f"  - '{entity['text']}' → 類別: {entity['category']}")

print(json.dumps(result, indent=4, ensure_ascii=False))
