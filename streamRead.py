import os
import time
from slackclient import SlackClient
import pprint

BOT_ID = os.environ.get("BOT_ID")
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
standUpID = os.environ.get("STANDUP_CHANNEL_ID")
userData = {}
greet = "What are you up to :rage:"
def sendQuestions():
    for key in userData:
        slack_client.api_call("chat.postMessage", as_user="true:", channel=userData[key][1], text=greet)

def match(value):
    for key in userData:
        if value in userData or value in userData[key][1]:
            return True
    return False

def postMessage(userID, text):
    result = "This is " +userData[userID][0] +"'s update: " + text
    slack_client.api_call("chat.postMessage", as_user="true:", channel=standUpID, text = result)

def parse_slack_output(rtm_output):
    output_list = rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output['type'] == 'message':
                if output['type'] == 'message' and match(output['channel']) and match(output['user']):
                    return output['user'], output['text']
    return None, None    

def gatherUserInfo():
    userList = (slack_client.api_call("users.list"))
    for users in userList['members']:
        if users['is_bot'] == False:
            if users['id'] != 'USLACKBOT':
                userName = users['name']
                userID = users['id']
                clientChat = slack_client.api_call("im.open", user = userID)
                imMessageID = clientChat[u'channel'][u'id']
                userData[userID] = (userName, imMessageID)
    return userData 

if __name__ == "__main__":
    WEBSOCKET_DELAY= 1
    if slack_client.rtm_connect():
        print "success"
        userData = gatherUserInfo()
        sendQuestions()
        while True:
            userID, text = parse_slack_output(slack_client.rtm_read())
            if text and userID:
                postMessage(userID, text)
                del userData[userID]
            if not userData:
                break
            time.sleep(WEBSOCKET_DELAY)
    else: print "connection failed"   
        
