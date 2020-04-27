import boto3
from flask import Flask, request
import csv
import json
import time
import urllib


with open('accesskeys.csv', 'r') as input:
    next(input)
    reader = csv.reader(input)
    print(reader)
    for line in reader:
        access_key_id = line[0]
        secret_access_key = line[1]

#print(access_key_id)
#print(secret_access_key)
app = Flask(__name__)


@app.route('/')
def index():
    return '''<form method = POST enctype=multipart/form-data action="upload">
        <input type=file name=myfile>
        <input type = submit>
        </form>'''

@app.route('/upload', methods = ['POST'])
def upload():
    s3 = boto3.resource('s3',
     region_name='ap-south-1',
    aws_access_key_id = access_key_id, 
    aws_secret_access_key = secret_access_key)

    audio = request.files['myfile']

    filename = audio.filename
    object = s3.Object('group-onn', 'upload/'+ filename)
    ret = object.put(Body = audio)
    Transcribe = boto3.client('transcribe',
                         aws_access_key_id=access_key_id, 
                        aws_secret_access_key=secret_access_key, 
                        region_name='ap-south-1')
    job_name = filename
    job_uri = 's3://group-onn/upload/'+filename

    Transcribe.start_transcription_job(TranscriptionJobName=job_name,
                                     Media={'MediaFileUri': job_uri},
                                     MediaFormat='wav', 
                                     LanguageCode='en-US')
    k = 0                  
    while True:
        status = Transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet... " + str(k))
        k+=1
        time.sleep(5)
#print(status)

    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        response = urllib.request.urlopen(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
        data = json.loads(response.read())
        text = data['results']['transcripts'][0]['transcript']
        #print(text)



    return text

if __name__ == '__main__' :
    app.run(debug = True)