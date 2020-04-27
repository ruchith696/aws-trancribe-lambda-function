#import datetime
#t = datetime.datetime.utcnow()
#amzdate = t.strftime('%Y%m%dT%H%M%SZ')
#datestamp = t.strftime('%Y%m%d')
#print(amzdate)
#print(datestamp)



 
import boto3
#from boto3.s3.key import Key
import botocore
import csv 
import json 

with open('accesskeys.csv', 'r') as input:
    next(input)
    reader = csv.reader(input)
    #print(reader)
    for line in reader:
        access_key_id = line[0]
        secret_access_key = line[1]
keyId = access_key_id
sKeyId= secret_access_key

srcFileName="notes.json"
destFileName="package1.json"
bucketName="group-onn"
s3 = boto3.resource('s3',
     region_name='ap-south-1',
    aws_access_key_id = access_key_id, 
    aws_secret_access_key = secret_access_key)

#obj  = s3.Object(bucketName, 'output')

#Get the Key object of the given key, in the bucket
obj = s3.Object(bucketName,'output/notes.json' )
body = obj.get()['Body'].read()
#print(body)
#s3.Bucket(bucketName).download_file('output/notes.json','n.json')
#body = body.decode('utf-8')
#Get the contents of the key into a file 

#k.get_contents_to_filename(destFileName)

#body = json.dumps(body)
#text = body['results']['transcripts'][0]['transcript']
#print(text)

data = json.loads(body)
text = data['results']['transcripts'][0]['transcript']
print(text)