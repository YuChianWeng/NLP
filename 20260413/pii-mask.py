import os
import requests
import json
from faker import Faker
from dotenv import load_dotenv
load_dotenv(override=True)

endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
key = os.getenv("AZURE_LANGUAGE_KEY")

api_url = f"{endpoint}/language/:analyze-text?api-version=2025-11-15-preview"

headers = {
    "Ocp-Apim-Subscription-Key": key,
    "Content-Type": "application/json",
}

# Step 1: 用 Faker 產生 5 筆假 PII 資料
fake = Faker()
documents = []
for i in range(1, 6):
    name = fake.name()
    dob = fake.date_of_birth(minimum_age=20, maximum_age=60).strftime("%m-%d-%y")
    ssn = fake.ssn()
    email = fake.email()
    phone = fake.phone_number()
    text = f"My name is {name}. My DOB is {dob} and SSN is {ssn}. Email: {email}, Phone: {phone}."
    documents.append({"id": str(i), "language": "en", "text": text})

print("=== 原始假資料 ===")
for doc in documents:
    print(f"[{doc['id']}] {doc['text']}")

# Step 2: 送 Azure 遮蔽 PII
body = {
    "kind": "PiiEntityRecognition",
    "parameters": {
        "modelVersion": "latest",
        "redactionPolicy": {
            "policyKind": "characterMask",
            "redactionCharacter": "*"
        }
    },
    "analysisInput": {
        "documents": documents
    }
}

response = requests.post(api_url, headers=headers, json=body)
result = response.json()

print("\n=== 遮蔽後結果 ===")
with open("pii-mask-results.txt", "w", encoding="utf-8") as f:
    if "results" in result:
        for doc in result["results"]["documents"]:
            original = next(d["text"] for d in documents if d["id"] == doc["id"])
            f.write(f"[{doc['id']}] 原文:  {original}\n")
            f.write(f"[{doc['id']}] 遮蔽後: {doc['redactedText']}\n\n")
            print(f"[{doc['id']}] 原文:  {original}")
            print(f"[{doc['id']}] 遮蔽後: {doc['redactedText']}")
    else:
        print(json.dumps(result, indent=4, ensure_ascii=False))
