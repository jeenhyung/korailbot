# -*- coding: utf-8 -*-
import sys
from korail2 import *
from datetime import datetime
import json

with open('account.json') as account:
    account_data = json.load(account)

class Letskorail:
        def __init__(self):
                print ("Init LetsKorail!")
                self.korail = Korail(account_data["id"], account_data["pwd"])
                self.dep = "동대구"
                self.arr = "김천"
                self.date = datetime.today().strftime('%Y%m%d')
                self.time = datetime.today().strftime('%H%M%S')
                self.psgrs = [AdultPassenger(1)]
                self.trains = []

        def login(self):
                self.korail.login()

        def getInputString(self):
                return "출발역: {},\n도착역: {},\n날짜: {},\n시간: {}".format(self.dep, self.arr, self.date, self.time)

        def insert(self, type, value):
                if type == "dep":
                        self.dep = value
                elif type == "arr":
                        self.arr = value
                elif type == "date":
                        self.date = value
                elif type == "time":
                        self.time = value
        
        def getTrainsLength(self):
                return len(self.trains)

        def search(self, chat_id):
                try:
                        print ("dep:{}, arr:{}, date:{}, time:{}".format(self.dep, self.arr, self.date, self.time))
                        self.trains = self.korail.search_train(self.dep, self.arr, self.date, self.time, passengers=self.psgrs, include_no_seats=True)
                        return self.trains
                except KorailError as e:
                        print ("search error: {}".format(e))
                        
        
        def reserve(self, chat_id, num):
                seat = self.korail.reserve(self.trains[int(num)], self.psgrs, ReserveOption.GENERAL_ONLY)
                return seat