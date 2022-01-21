# mytwitterbot.py
# IAE 101, Fall 2019
# Project 02 - Building a Twitterbot
# Name: Harry Rajput       
# netid: hrrajput      
# Student ID: 112812876

import sys
import simple_twit
import random
import time

def main():
    # This call to simple_twit.create_api will create the api object that
    # Tweepy needs in order to make authenticated requests to Twitter's API.
    # Do not remove or change this function call.
    # Pass the variable "api" holding this Tweepy API object as the first
    # argument to simple_twit functions.
    api = simple_twit.create_api()
    # YOUR CODE BEGINS HERE
    
    #gathering all the snippets from a file
    choices = []
    
    newtweetid = 0
    
    for line in open("Extracts.txt"):
        line = line.strip()
        extract = line[:line.find("|")]
        line = line[line.find("|")+1:]
        artist = line[:line.find("|")]
        line = line[line.find("|")+1:]
        title = line[:line.find("|")]
        line = line[line.find("|")+1:]
        link = line[line.find("y"):]
        choices.append([extract, artist, title, link])
    
    #assembling the tweet
    chosen = random.choice(choices)
    snippet = "\n".join(chosen[0].split(";"))
    snippet = snippet.strip()
    final = "Today's Mystery Snippet:\n" + "\n" + "\"" + snippet + "\"\n" + "\n" + "Can you guys guess which song this is?\n" + "First person to reply with the name of the song gets a shoutout!"
    print("Initial tweet will look like this:\n\n", final, "\n")
    button = input("Do you want to post this snippet? Y or N:")
    
    
    #verification of proper tweet size
    testforlength = "".join(chosen[0].split(";"))
    if len(testforlength) > 144:
        print("\n ERROR SNIPPET TOO LONG (", len(testforlength), ")")
    elif button == "Y": #sending the tweet
        global newtweet
        newtweet = simple_twit.send_tweet(api, final)
        newtweetid = newtweet.id
        old_replies = simple_twit.get_mentions(api, 100)
        print("Tweet Sent! Going to sleep for 15 minutes")
        print("--------------------------------------------------------------")
        time.sleep(40) #waiting 15 minutes (900 seconds) for people to reply
        
        
    #checking for correct replies
        replies = simple_twit.get_mentions(api, 100)
        tobechecked = []
        #eliminating replies from other posts
        for x in replies:
            if x not in old_replies:
                tobechecked.append(x)
        tobechecked.reverse()
        print("There were ", len(tobechecked), " replies")
        print()
#        check = input("Do you want to check for the right answer? Y or N:")
        if len(tobechecked) > 0:
            print("Looking for \"", chosen[2], "\" in replies:")
            print()
            winnerfound = False
            timeschecked = 0
            while winnerfound == False:
                for reply in tobechecked:
                    print(reply.full_text, "\n")
                    if chosen[2].lower() in (reply.full_text).lower():
                        comment = (reply.full_text)[(reply.full_text).find(" "):]
                        shoutout = "Shoutout to @" + (reply.author).screen_name + " for winning today's Mystery Snippet Challenge!\n\n" + "Their comment was:\n" + comment + "\n\nLook out for tomorrow's mystery snippet to potentially win a shoutout!\n" + "Link to original song: " + chosen[3]
                        sendshoutout = simple_twit.send_tweet(api, shoutout)
                        winnerfound = True
#                        print(shoutout)
                    timeschecked += 1
                if timeschecked == len(tobechecked):
                    break
            if winnerfound == True:
                print("A winner was found and the shoutout was sent!")
            else:
                #sending the answer
                print("No winner was found, sending out the answer")
                answer = "@hrrajput_IAE101\n" + "This snippet is actually from the song \"" + chosen[2] + "\" by " + chosen[1] + "!\n" + "\n" + "Check out their song with the following link:\n" + chosen[3]
                #print("\nThe reply with the answer will look like this:\n\n", answer, "\n")
                #button2 = input("Are you sure you want to send out the answer? Y or N:")
                simple_twit.send_reply_tweet(api, answer, newtweetid)
    
          
          


if __name__ == "__main__":
       main()
