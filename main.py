#!/usr/bin/env python

import praw
import OAuth2Util
import properties
import re
from time import sleep
import os

r_instance = None
already_commented = []

def load_already_commented():
    with open("commented.txt", "rw") as file:
	already_commented = [i for i in file.readlines()]
	#cleaning code that may be used one day
	if len(already_commented) > 10000:
	   already_commented = already_commented[-10000:]
	   file.writelines(already_commented)
    return already_commented

def username_mentions():
    mentions = r_instance.get_mentions(limit=10)
    unreads = r_instance.get_unread(limit=None)
    for u in unreads:
        for m in mentions:
            if m == u:
                print "mentioned by: " + m.id " for " + m.comment.submission.id
                u.mark_as_read()
                build_reply(m.comment.submission)



def scan_submission(submission):
    print "scanning submission: " + submission.title + " " + submission.id
    if '[help]' in post.title.lower():
        if any(word in post.selftext.lower for word in models.general_words):
            build_reply(post)  

def build_comment(submission):
    global already_replied
    if submission.id not in already_replied:
        already_replied.append(post.id)
    reply = "taigei"
    post.add_comment(reply)

def main():
    global r_instance
    global already_commented
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
    print "successful! connecting to subreddit: " + properties.subreddit
    sub_r = r_instance.get_subreddit(properties.subreddit)
    already_commented = load_already_commented()

    while True:
        oauth_instance.refresh(force=True)
        for i in range(0,60):
            #username_mentions()
            for submission in sub_r.get_new(limit=3):
		if submission.id not in already_commented:
                  scan_submission(submission)
            sleep(59)
    

if __name__ == "main__":
    main()
