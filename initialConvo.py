import os
import time
from slackclient import SlackClient
import json

BOT_ID = os.environ.get("BOT_ID")
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
userList = ""

def lastMessageFromUser(im_history):
	print im_history
	message = 1
	return message


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
	    print("success!")
	    print "Finding all users in chat room"
	    userList = (slack_client.api_call("users.list"))
	    for members in userList['members']:
		username = members[u'name']
		userID = members[u'id']
		clientChat = slack_client.api_call("im.open", user=userID)
		greeting = "Hi %s test greeting pls ignore" % username
		if u'error' in clientChat:
		    print "I am a bot"
		else:
		    id = clientChat[u'channel'][u'id']
		    print slack_client.api_call("chat.postMessage", as_user="true:", channel=id, text = greeting)
		    time.sleep(20) #need to know have recieved a reply?
		    print lastMessageFromUser(slack_client.api_call("im.history", channel=id, count = 1))
	    break
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

	
