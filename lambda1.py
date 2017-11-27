from __future__ import print_function
#import tweepy
import json
import boto3
import urllib2
import urlparse
print('Loading function')


import json

def lambda_handler(event, context):
    # this object is valid 
    message = "test"
    tweet_text = ""
    item="default"
    tweet_location=""
    sentiment = ""
    full_tweet = ""
    count =0
    location =""
    resp = "default"
    try:
        #reading from sns
        resp = json.loads(event['body'])
        item = resp['search_value'] #search value from web page
        client = boto3.client('sqs',aws_access_key_id='hahahahahahahah',aws_secret_access_key='hahahahahahahah',region_name='us-east-1')
        queue_url = "https://sqs.us-east-1.amazonaws.com/00000000000000/Messi"
        response = client.receive_message(QueueUrl=queue_url,AttributeNames=['SentTimestamp'],MaxNumberOfMessages=1,MessageAttributeNames=['All'],VisibilityTimeout=0,WaitTimeSeconds=0)
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        client.delete_message(QueueUrl=queue_url,ReceiptHandle=receipt_handle)
        tweet_text=message['MessageAttributes']['text']['StringValue']
        tweet_location=message['MessageAttributes']['twitter']['StringValue']
        full_tweet=message['MessageAttributes']['tweet']['StringValue']
        
        #end of sns
        
        #Sentiment analysis
        sentiment = "positive"
        values = {'data': [{'text': tweet_text}]}
        data = json.dumps(values)
        url = "http://www.sentiment140.com/api/bulkClassifyJson"
        response = urllib2.urlopen(url, data)
        page = response.read()
        page = json.loads(page)
        sentimentCode = page["data"][0]["polarity"]
        if sentimentCode == 0:
            sentiment = "negative"
        if  sentimentCode == 2: 
            sentiment == "neutral"
        if  sentimentCode == 4:
            sentiment = "positive"        #end of sentiment analysis
        
        # putting data into sqs to put new data
        #triggerring sns
        if item in full_tweet: #search for data
            url = "https://sqs.us-east-1.amazonaws.com/00000000000000/fabregas"
            response = client.send_message(QueueUrl=url,MessageAttributes={
                'twitter': {
            'DataType': 'String',
            'StringValue': tweet_location
        },
        'text': {
            'DataType': 'String',
            'StringValue': sentiment
        },
        'search': {
            'DataType': 'String',
            'StringValue': item
        }
    },
    MessageBody=(
        item
    ),
)
            client1 = boto3.client('sns',aws_access_key_id='hahahahahahahah',aws_secret_access_key='hahahahahahah',region_name='us-east-1')
            response = client1.publish(TopicArn='arn:aws:sns:us-east-1:00000000000000:twitter_analysis',Message='messi is GOAT',MessageAttributes={
                'twitter': {
            'DataType': 'String',
            'StringValue': 't'
        },
        'text': {
            'DataType': 'String',
            'StringValue': 't'
        },
         'tweet':{
             'DataType': 'String',
            'StringValue': 't'
            }
    })
            #message=req.read()
    except Exception as e:
        message = e.message
    
    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'application/json' ,
            'Access-Control-Allow-Origin' : '*'
        },
        'body': json.dumps({ 'username':  message, 'id': 20 }
        )
    }
