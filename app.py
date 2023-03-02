import streamlit as st
import speech_recognition as sr
import os
from google.cloud import language
import io
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "sentimentanalysis-379314-9c65d1116d03.json"

## Required Functions

#r = sr.Recognizer()
#audio = sr.AudioFile("/content/phone_call.wav")


def speech2text(input_wav_file):
    speech_recognizer = sr.Recognizer()

    try:
        audio_data = sr.AudioFile(input_wav_file)
    except Exception as e:
        audio_data = sr.AudioFile(io.BytesIO(input_wav_file))

    with audio_data as source:
        audio_file = speech_recognizer.record(source)
        result = speech_recognizer.recognize_google(audio_file, language="en-IE")  # IN
    return result


def analyze_text_sentiment(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)

    response = client.analyze_sentiment(document=document)

    sentiment = response.document_sentiment
    results = {'score': f"{round(sentiment.score, 2)}", 'magnitude': f"{round(sentiment.magnitude, 2)}"}
    for k, v in results.items():
        print(f"{k:10}: {v}")
    return results


def classify_text(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)

    response = client.classify_text(document=document)

    for category in response.categories:
        print("=" * 80)
        print(f"category  : {category.name}")
        print(f"confidence: {category.confidence:.0%}")
    classification = {"category": category.name, "confidence": category.confidence}
    return classification



audio_text = "Nothing"


st.markdown("""<h1> Upload Audio File </h1>""",unsafe_allow_html=True)
upload_audio_file = st.file_uploader(" ",type={".wav"},accept_multiple_files=False)
if upload_audio_file is not None:
    bytes_data = upload_audio_file.getvalue()
    audio_text = speech2text(bytes_data)


if upload_audio_file is not None:
    if audio_text =="Nothing":
        st.info('Please Wait..', icon="ℹ️")
    else:
        st.success("**"+audio_text+"**")
        text_sentiment = analyze_text_sentiment(audio_text)

        st.markdown("""<h1> Scores </h1>""",unsafe_allow_html=True)
        st.write("Score: ", text_sentiment["score"])
        st.write("Magnitude: ", text_sentiment["magnitude"])

        text_classification = classify_text(audio_text)
        st.markdown("""<h1> Classification </h1>""", unsafe_allow_html=True)
        st.write("Category: ", text_classification["category"])
        st.write("Confidence: ", text_classification["confidence"])

