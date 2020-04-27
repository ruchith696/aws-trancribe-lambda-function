import boto3
import time
import urllib
import json
import os
import datetime


access_key = os.environ.get('AWS_ACCESS_KEY_ID')
secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')


Transcribe = boto3.client('transcribe',
                         aws_access_key_id=access_key, 
                        aws_secret_access_key=secret_key, 
                        region_name='ap-south-1')
t = datetime.datetime.utcnow()
amzdate = t.strftime('%Y%m%dT%H%M%SZ')
#datestamp = t.strftime('%Y%m%d')
job_name = amzdate
job_uri = 's3://group-onn/upload/bantu_sent.wav'

Transcribe.start_transcription_job(TranscriptionJobName=job_name,
                                     Media={'MediaFileUri': job_uri},
                                     MediaFormat='wav', 
                                     LanguageCode='en-US')
                            
while True:
    status = Transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    print("Not ready yet...")
    time.sleep(5)
#print(status)

if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
    response = urllib.request.urlopen(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
    data = json.loads(response.read())
    text = data['results']['transcripts'][0]['transcript']
    
import docx
doc = docx.Document()
doc.add_paragraph(text)
doc.save('ouput_aws.docx')
