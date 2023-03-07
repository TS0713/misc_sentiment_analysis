# -*- coding: utf-8 -*-
"""Audio_Diarization_Sample.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TxmOOscJOwJJ26tU2XFaLNyq08bVFeuR
"""

!pip install --upgrade google-cloud-language
!pip install --upgrade google-cloud-speech
!pip install pytube
!pip install ffmpeg-python
!pip install pydub
!pip install SpeechRecognition

"""## Loading all Necessary Libraries"""

import json
import os
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
from google.cloud import language_v1
from pydub import AudioSegment
from pydub.silence import split_on_silence
from google.cloud import speech
from google.cloud import storage
from google.cloud import speech_v1p1beta1 as speech

#json_file = "/content/sentimentanalysis-379314-a4a6d6259d79.json"
json_file = "/content/sentimentanalysis-379314-0c54bdecee97.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=json_file

audio_file = "/content/drive/MyDrive/Datasets/phone_call.wav"

#speech_file = "/content/Call Center Services.mp3"
speech_file = "/content/drive/MyDrive/Datasets/phone_call.wav"
#speech_file = "/content/audio50.wav"
client = speech.SpeechClient()

with open(speech_file, "rb") as audio_file:
    content = audio_file.read()

"""## Function to upload File/ Audio File to Google Cloud Storage Bucket"""

def upload_file_GCS(colab_file_path,bucket_name,destination_name):

  
  storage_client = storage.Client()
  #bucket_name = "tsp-sample"
  bucket = storage_client.bucket(bucket_name)
  #blob = bucket.blob("call_recordings.wav")
  blob = bucket.blob(destination_name)
  generation_match_precondition = 0
  #source_file_name = "/content/phone_call.wav"
  source_file_name = colab_file_path
  try:
    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)
    print ("Successfully Uploaded  "+colab_file_path +"  to GCS Bucket - "+ bucket_name)
  except Exception as e:
    print ("Failed to Uploaded  "+colab_file_path +"  to GCS Bucket - "+ bucket_name)
    print (e)

"""## Function to get Speakers Details with text based on Input Audio File using Google Speech Client



"""

def create_transcript(enter_audio_file,uri=False,model_name=None):
  
  #speech_file = enter_audio_file 
  client = speech.SpeechClient()
  if uri:
    audio = speech.RecognitionAudio(uri=enter_audio_file)
  else:
    with open(enter_audio_file, "rb") as audio_file:
      content = audio_file.read()
      audio = speech.RecognitionAudio(content=content)
    
  
  diarization_config = speech.SpeakerDiarizationConfig(
    enable_speaker_diarization=True,
    min_speaker_count=2,
    max_speaker_count=10
    )
  if model_name is None:
    model_name = "latest_long"
    
  config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="en-US",
    diarization_config=diarization_config,
    model=model_name #"latest_long"    
    )
  try:
    if uri:
      operation = client.long_running_recognize(config=config, audio=audio)
      response = operation.result(timeout=90)

    else:
      response = client.recognize(config=config, audio=audio)

  except Exception as e:
    print ("==============================")
    print (e)
    print ("==============================")
  
  result = response.results[-1]
  
  words_info = result.alternatives[0].words
  text_script = [(word_info.word, "speaker_tag: "+str(word_info.speaker_tag)) for word_info in words_info]
  return text_script

"""## Uploading File to google cloud storage bucket"""

upload_file_GCS(
    colab_file_path = "/content/phone_call.wav",
    bucket_name = "tsp-sample",
    destination_name = "new_audio.wav"
                )

"""## Getting Speakers and Text Details based on Audio Input"""

#inp_path = "/content/audio_50_1.wav"
inp_path = "gs://tsp-sample/new_phone_call.wav"
inp_path = "gs://tsp-sample/call_recordings.wav"
inp_path = "gs://tsp-sample/new_audio.wav"
audio_recording = create_transcript(enter_audio_file=inp_path,uri=True)
recordings = [i[0] for i in audio_recording]
print (" ".join(recordings))

audio_recording

#audio_50_1_convo = create_transcript("/content/audio_50_1.wav")#,model_name="phone_call")
#audio_50_2_convo = create_transcript("/content/audio_50_2.wav")#,model_name="phone_call")
#audio_50_3_convo = create_transcript("/content/audio_50_3.wav")#,model_name="phone_call")
#audio_50_4_convo = create_transcript("/content/audio_50_4.wav")#,model_name="phone_call")