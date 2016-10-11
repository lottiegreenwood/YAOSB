import os
import time
from slackclient import SlackClient
import json
import pprint
import MySQLdb as mdb
from warnings import filterwarnings
import threading

BOT_ID = os.environ.get("BOT_ID")
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
threads =[]
standUpID = "C2G4A3VJL"

def parseOutput(rtm_output, imID, userID):
    output_list = rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output['type'] == 'message' and output['channel'] == imID and output['user'] == userID:
                print output
                return output['text']


def waitSendResponse(imID, userID):
    while True:
        message = parseOutput(slack_client.rtm_read(), imID, userID)
        if message:
            return message
                

def startConversation(userID, userName, imID):
    print "starting thread " + userName
    greeting = "hey what are you up to :rage:"
    slack_client.api_call("chat.postMessage", as_user="true:", channel=imID, text = greeting)     
    response2 = waitSendResponse(imID, userID)
    print response2
    response = "he"
    result = "This is " +userName +"'s update: " + response2
    slack_client.api_call("chat.postMessage", as_user="true:", channel=standUpID, text = result)
    


if __name__ == "__main__":
    if slack_client.rtm_connect():
        print("connected")
        userList = (slack_client.api_call("users.list"))
        for users in userList['members']:
            if users['is_bot'] == False:
                if users['id'] != 'USLACKBOT':
                    userName = users['name']
                    userID = users['id']
                    clientChat = slack_client.api_call("im.open", user = userID)
                    imMessageID = clientChat[u'channel'][u'id']
                    t = threading.Thread(name= 'conversation', target=startConversation, args=(userID, userName, imMessageID,))
                    threads.append(t)
                    t.start()
                    startConversation(userID, userName, imMessageID)
                    
            
