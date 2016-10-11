import os
import time
from slackclient import SlackClient
import json
import pprint
import MySQLdb as mdb
from warnings import filterwarnings

BOT_ID = os.environ.get("BOT_ID")
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
con = mdb.connect('localhost', 'testuser', 'test623', 'slackUsers')

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    with con:
        cur = con.cursor()
        print cur.execute("SELECT * FROM users") #probably end up deleting table here and remaking everytime
    if slack_client.rtm_connect():
        print("starterBot connected!")
        userList = (slack_client.api_call("users.list"))
        with con:
            cur = con.cursor()
            for users in userList['members']:
                if users["is_bot"] == False:
                    if users['id'] != 'USLACKBOT':
                        userID = users['id']
                        userName = users['name']
                        clientChat = slack_client.api_call("im.open", user = userID)
                        imMessageID = clientChat['channel']['id']
                        print "userID: " + userID + " userName: " + userName
                        cur.execute("INSERT INTO users(UserID, Name, IMID) VALUES('" + userID + "', '" + userName + "', '" + imMessageID + "')") 
                        
            
                
    else: print("connection failed.")
