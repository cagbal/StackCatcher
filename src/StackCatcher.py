#!/usr/bin/python

import sys
import time
import threading
import requests
import json
import datetime

# define a user requests class
class UserRequests:
    
    def __init__(self):
        self.tag_name = "python" # default tag is python
        self.check_interval_minute = 1 # default checking interval 1 minute

        self.askInput()
    
    # Ask for user input
    def askInput(self):
        self.tag_name = raw_input("Enter the Tag names seperated by space: ").split(' ')


# define a parser class
class Parser:

    def __init__(self, user_requests):
        self.options = user_requests
        self.url = "https://api.stackexchange.com/2.2/questions?order=desc&sort=creation&site=stackoverflow"
        self.fromdate = None #(datetime.datetime.utcnow()-datetime.datetime(1970,1,1)).total_seconds()
        self.thread = None

        print "Tag names: ", self.options.tag_name

    def get(self):

        if self.fromdate:
            r = requests.get(self.url + '&fromdate=' + str(self.fromdate))
        else:   
            r = requests.get(self.url)

        if r.status_code == 200:
            return r.text
        else:
            print "Status Code Error: ", r.status_code
            sys.exit()
            
    # parse the json object and return a list of specific tagged questions
    def parse(self):
        
        r = json.loads(self.get()) # get

        question_list = [] # create a list 
   
        # check if our tags exist in recent questions
        for question in r['items']:
            tags = question['tags'] # get the tags of question
            for tag in self.options.tag_name:
                if tag in tags:
                    question_list.append(question)
         
        return question_list

    # find if found questions are new
    def run(self):

        threading.Timer(self.options.check_interval_minute*60, self.run).start() # start thread

        question_list = self.parse() # parse the response

        if question_list: # check if question list is empty  
            self.fromdate = question_list[0]['creation_date'] + 1 # update the from date 

            # print the questions
            for question in question_list:
                print "\n\n*******************************************************"
                print "\nNew question: ", question['title']
                print "\nLink: ", question['link']



def main():
     
    # User requests object
    ur = UserRequests()

    # Parser object
    p = Parser(ur)
  
    # start the thread
    p.run()

if __name__ == '__main__': 
    main()
