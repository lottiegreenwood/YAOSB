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

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) >0:
	for output in output_list:
	    if output[u'type'] == u'message':
		return output[u'text'], output[u'channel']
    return 0,0 



if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True: #if get rid of the 'break' it will basically loop6eva 
	    print("success!")
	    print "Finding all users in chat room"
	    userList = (slack_client.api_call("users.list"))
	    for members in userList['members']:
		username = members[u'name']
		userID = members[u'id']
		clientChat = slack_client.api_call("im.open", user=userID)
		greeting = "Hi %s what are you up to" % username
		ending = "Cheers, til tomorrow"
		if u'error' in clientChat:
		    print "I am a bot"
		else:
		    id = clientChat[u'channel'][u'id']
		    print "I am not"
		    print slack_client.api_call("chat.postMessage", as_user="true:", channel=id, text = greeting)
		    command, channel = parse_slack_output(slack_client.rtm_read())
		    print command
		    if command != 0:
			print command #store it here
			slack_client.api_call("chat.postMessage", as_user="true:", channel=id, text = ending)
			
		    time.sleep(READ_WEBSOCKET_DELAY)
	    #break
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

	
