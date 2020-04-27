
import json
import time
import boto3
import urllib
from urllib.request import urlopen
#import datatime
import datetime


transcribe = boto3.client('transcribe')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    if event:
        t = datetime.datetime.utcnow()
        amzdate = t.strftime('%Y%m%dT%H%M%SZ')
        
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        file_name =  urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        format = file_name.split('.')[1]
        s3_uri = create_uri(bucket_name, file_name)
        job_name = amzdate
        
        transcribe.start_transcription_job(TranscriptionJobName = job_name,Media = {'MediaFileUri': s3_uri},MediaFormat =  format,LanguageCode = "en-US")
        k=0
        while True:
            print(k)
            k+=1
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            print(status['TranscriptionJob']['TranscriptionJobStatus'])
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            print("Not ready yet...")
            time.sleep(5)
           
            
        print('i am here')
        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            print('completed')
            load_url = urlopen(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
            load_json = json.dumps(json.load(load_url))
        
            s3.put_object(Bucket = bucket_name, Key = 'output/{}.json'.format(job_name), Body = load_json )

    return {
        'statusCode': 200,
        'body': json.dumps('Transcription job created!')
    }

def create_uri(bucket_name, file_name):
    return "s3://"+bucket_name+"/"+file_name