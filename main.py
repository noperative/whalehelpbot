#!/usr/bin/env python

import praw
import OAuth2Util
import models
import re
from time import sleep

r_instance = None
already_replied = []

def username_mentions():
    mentions = r_instance.get_mentions()
    unreads = r_instance.get_unread()
    for m in mentions:
        for u in unreads:
            if m == u:
                print(m)
                #build_reply(m.post), i have no idea what the parameter for the post is



def scan_post(post):
    print "scanning post: " + post.title
    if '[help]' in post.title.lower():
        if any(word in post.selftext.lower for word in models.general_words):
            build_reply(post)  

def build_reply(post):
    global already_replied
    if post.id not in already_replied:
        already_replied.append(post.id)
    reply = "taigei"
    post.add_comment(reply)

def main():
    global r_instance
    print "Hello World!" 
    while True:
        try:
            print "trying to login..."
            r_instance = praw.Reddit(models.user_agent)
            oauth_instance = OAuth2Util.OAuth2Util(r_instance)
            oauth_instance.refresh(force=True)
            break
        except Exception as e:
            print "error, retrying in 30 seconds"
            sleep(30)
    print "successful! connecting to subreddit: " + models.subreddit
    sub_r = r_instance.get_subreddit(models.subreddit)
    
    while True:
        oauth_instance.refresh(force=True)
        for i in range(0,60):
            #username_mentions()
            for post in sub_r.get_new(limit=3):
                scan_post(post)
            sleep(59)
    

if __name__ == "main__":
    main()