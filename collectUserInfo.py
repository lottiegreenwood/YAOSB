import os
import time
from slackclient import SlackClient
import json
import pprint
import MySQLdb as mdb
from warnings import filterwarnings

BOT_ID = os.environ.get("BOT_ID")
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
userList = ""
con = mdb.connect('localhost', 'testuser', 'test623', 'slackUsers')
ii = 0
def first_setup():
    #with con:
     #   cur = con.cursor()
    print "reached here!"        

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    filterwarnings('ignore', category = mdb.Warning)
    with con:
        cur = con.cursor()
        cur._defer_warnings = True
        cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("CREATE TABLE users(Id INT PRIMARY KEY AUTO_INCREMENT, \
                    Name VARCHAR(20), UserID VARCHAR(20))")
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True: #if get rid of the 'break' it will basically loop6eva 
            userList = (slack_client.api_call("users.list"))
            for users in userList['members']:
                print "yes"    
                #if ii == len(userList['members']):
            #        break
            #    ii+=1
                if users['is_bot'] == False: 
                    if users['id'] != 'USLACKBOT':
                        with con:
                            cur = con.cursor()
                            userName = users['name']
                            userID = users['id']
                            clientChat = slack_client.api_call("im.open", user = userID)
                            imMessageID = clientChat[u'channel'][u'id']
                            print "userID: " + userID + " userName: " + userName
                            cur.execute("INSERT INTO users(userID) VALUES('" + userID + "')")
#			    #cur.execute("INSERT INTO users
#		 	    cur.execute("DROP TABLE IF EXISTS users")
                            time.sleep(READ_WEBSOCKET_DELAY)

    else:
        print("Connection failed. Invalid Slack token or bot ID?")

	
