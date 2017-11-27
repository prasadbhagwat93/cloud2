import tweepy
import json
#import boto3.s3
# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import os
import time
import boto3
import json
from paralleldots import set_api_key, get_api_key 
#set_api_key("ABCdef123MNO456PQR789xyz")
client = boto3.client('sqs')

queue_url="https://sqs.us-east-1.amazonaws.com//Messi"
from subprocess import call
# Variables that contains the user credentials to access Twitter API 
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""
file_name = "twitt" + str(time.time())
#os.mknod(file_name)
# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        try:
            #location = str(data["user"]["location"])
            print(type(data))
            data_real = data
            data = json.loads(str(data))
            try:
                location = str(data["user"]["location"])
            except:
                location = "None"    
            response = client.send_message(
            QueueUrl=queue_url,
            MessageAttributes={
                'twitter': {
            'DataType': 'String',
            'StringValue': location
        },
        'text': {
            'DataType': 'String',
            'StringValue': str(data['text'])
        },
         'tweet':{
             'DataType': 'String',
            'StringValue': data_real
         }
    },
    MessageBody=(
        'Information about current NY Times fiction bestseller '
        'week of 12/11/2016.'
    ),
    
)
            return True
        except Exception as e:
            print(str(e))

    def on_error(self, status):
        print (status)


if __name__ == '__main__':
    # This handles Twitter authentication and connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=['chelsea'])
                                       
