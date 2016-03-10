#!/usr/bin/python3

import praw
import OAuth2Util
import properties
import re
from time import sleep
from replybuilder import *
import os

r_instance = None
already_commented = []


def load_already_commented():
    with open("commented.txt", "r+") as f:
        already_commented_ids = [i for i in f.read().split()]
    # cleaning code that may be used one day
    if len(already_commented_ids) > 10000:
        already_commented_ids = already_commented_ids[-10000:]
        f.seek(0)
        f.writelines(already_commented_ids)
    return already_commented_ids


def username_mentions():
    mentions = r_instance.get_mentions(limit=10)
    unreads = r_instance.get_unread(limit=None)
    for u in unreads:
        print("unread message found")
        for m in mentions:
            if m == u:
                print("mentioned by: " + m.id + " for " + m.submission.id)
                u.mark_as_read()
                build_comment(m.submission)

def parse_submission(text):
    keywords = []
    for attr in replybuilder.iteritems():
        if attr in text:
            keywords.insert(attr)
    return keywords


def scan_submission(submission):
    print("scanning submission: " + submission.title + " " + submission.id)
    if '[help]' in submission.title.lower():
        # if any(word in submission.selftext.lower for word in properties.general_words):
            keywords = parse_submission(submission.selftext.lower())
            build_comment(submission, keywords)


def build_comment(submission, keywords=[]):
    global already_commented
    if submission.id not in already_commented:
        already_commented.append(submission.id)
        with open("commented.txt", "a") as f:
            f.write('{0!s}\n'.format(submission.id))
        comment = base_string
        for keyword in keywords:
            comment += getattr(replybuilder, keyword)
        comment += end_string
        submission.add_comment(comment)


def main():
    global r_instance
    global already_commented
    print("Hello World!")
    while True:
        try:
            print("trying to login...")
            r_instance = praw.Reddit(properties.user_agent)
            oauth_instance = OAuth2Util.OAuth2Util(r_instance)
            oauth_instance.refresh(force=True)
            break
        except Exception as e:
            print (e)
            print("error, retrying in 30 seconds")
            sleep(30)
    print("successful! connecting to subreddit: " + properties.subreddit)
    sub_r = r_instance.get_subreddit(properties.subreddit)
    already_commented = load_already_commented()
    print(already_commented)
    while True:
        oauth_instance.refresh(force=True)
        for i in range(0, 60):
            username_mentions()
            for submission in sub_r.get_new(limit=3):
                scan_submission(submission)
            sleep(59)
    

if __name__ == "__main__":
    main()
