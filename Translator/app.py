import configparser
from pathlib import Path

# Azure Translation
from azure.ai.translation.text import TextTranslationClient
# from azure.ai.translation.text.models import InputTextItem
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

# Config Parser
config = configparser.ConfigParser()
config.read(Path(__file__).parent / ".env")

# Translator Setup
text_translator = TextTranslationClient(
    credential=AzureKeyCredential(config["AzureTranslator"]["Key"]),
    endpoint=config["AzureTranslator"]["Endpoint"],
    region=config["AzureTranslator"]["Region"],
)

def azure_translate(user_input):

    try:
        # 先偵測語言，再決定翻譯目標
        detect_response = text_translator.translate(
            body=[user_input], to_language=["en"]
        )
        detected = detect_response[0].detected_language.language if detect_response else None

        if detected == "zh-Hant" or detected == "zh-Hans":
            target_languages = ["en"]
        elif detected == "en":
            target_languages = ["zh-Hant"]
        else:
            target_languages = ["zh-Hant", "en"]

        response = text_translator.translate(
            body=[user_input], to_language=target_languages
        )
        translation = response[0] if response else None

        if translation:
            return_text = ""
            for item in translation.translations:
                return_text += f"[{item.to}] {item.text}\n"
            return return_text, detected

    except HttpResponseError as exception:
        print(f"Error Code: {exception.error}")
        print(f"Message: {exception.error.message}")

#sentence = "おひようございます！今日はいい天気ですね。"
#sentence = "Hello, how are you? "
sentence = "今天天氣真好！"

translation_result, detected_language = azure_translate(sentence)
print(f"原文：{sentence}（偵測語言：{detected_language}）")
print(translation_result)