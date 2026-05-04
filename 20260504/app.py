import configparser

# Azure Speech
import azure.cognitiveservices.speech as speechsdk

# Config Parser
config = configparser.ConfigParser()
config.read('config.ini')

# Azure Speech Settings
speech_config = speechsdk.SpeechConfig(subscription=config['AzureSpeech']['SPEECH_KEY'], 
                                       region=config['AzureSpeech']['SPEECH_REGION'])
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

def azure_speech(user_input):
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio16Khz64KBitRateMonoMp3
    )
    # The language of the voice that speaks.
    # speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
    # speech_config.speech_synthesis_voice_name = "zh-TW-HsiaoChenNeural"
    speech_config.speech_synthesis_voice_name = "zh-CN-Xiaoxiao2:DragonHDFlashLatestNeural"
    file_name = "outputaudio.mp3"
    file_config = speechsdk.audio.AudioOutputConfig(filename="static/" + file_name)
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, 
        audio_config=file_config,
        # audio_config=audio_config
    )

    ssml_input = f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="zh-CN">
        <voice name="zh-CN-XiaoxiaoNeural">
            <mstts:express-as style="sad" styledegree="2">
                {user_input}
            </mstts:express-as>
        </voice>
    </speak>
    """


    # Receives a text from console input and synthesizes it to wave file.
    # result = speech_synthesizer.speak_text_async(user_input).get()
    result = speech_synthesizer.speak_ssml_async(ssml_input).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(
            "Speech synthesized for text [{}], and the audio was saved to [{}]".format(
                user_input, file_name
            )
        )
        
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

# target_text = "Hello, this is a test of Azure Speech Service."
target_text = "這禮拜是期中考，都還沒看。"

azure_speech(target_text)