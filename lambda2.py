import json
import boto3
import urllib2
print('Loading function')


def lambda_handler(event, context):
    search_data = ""
    try:
        message = ""

        
        client = boto3.client('sqs',aws_access_key_id='hahahahahah',aws_secret_access_key='hahahahahahaha',region_name='us-east-1')
        queue_url = "https://sqs.us-east-1.amazonaws.com/00000000000000/fabregas"
        response = client.receive_message(QueueUrl=queue_url,AttributeNames=['SentTimestamp'],MaxNumberOfMessages=1,MessageAttributeNames=['All'],VisibilityTimeout=0,WaitTimeSeconds=0)
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        client.delete_message(QueueUrl=queue_url,ReceiptHandle=receipt_handle)
        tweet_text=message['MessageAttributes']['text']['StringValue']
        tweet_location=message['MessageAttributes']['twitter']['StringValue']
        search_data = message['Body']
        data="{\"location\":\""+tweet_location+"\",\"sentiment\":\""+tweet_text+"\"}"
        req=urllib2.urlopen("https://search-twwits-7bmrnjvevlel3kx2ghihkc73ruum.us-east-1.es.amazonaws.com/"+search_data+"/test", data=data)
        #message = req.read()
    except Exception as e:
        message=e.message
        
    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'application/json' ,
            'Access-Control-Allow-Origin' : '*'
        },
        'body': json.dumps({ 'username':  search_data, 'id': 20 }
        )
        }