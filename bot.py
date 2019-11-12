# -*- coding: utf-8 -*-
import sys
import time as timeObject
import telepot
from telepot.loop import MessageLoop
from korail2 import *
from datetime import datetime
from Letskorail import Letskorail
import threading

letsKorail = Letskorail()
type(letsKorail)

is_reserved = False

def async_reserve(chat_id, text_arr):
        global is_reserved
        is_reserved = True
        while is_reserved:
                try:
                        timeObject.sleep(0)
                        seat = letsKorail.reserve(chat_id, text_arr[1])
                        # print (seat)
                        bot.sendMessage(chat_id, str("[예약완료] {}".format(seat)))
                        is_reserved = False
                except Exception as e:
                        e_arr = str(e).split(' ')
                        if e_arr[0] == "승차일,열차,승차구간이":
                                bot.sendMessage(chat_id, str(e))
                                is_reserved = False
                        print("expection in while: {}".format(e_arr))



def handle(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        # print(content_type, chat_type, chat_id, msg['text'])

        text_arr = msg['text'].split(' ')
        
        if content_type == 'text':
                if text_arr[0] == "/start":
                        bot.sendMessage(chat_id, "안녕하세요. 코레일 자동 예메 봇 '리차' 입니다.")
                        bot.sendMessage(chat_id, "다음을 입력해 주세요.\n 1) 출발역: '/dep 동대구'\n 2) 도착역: '/arr 김천'\n 3) 날짜: '/date 20190101'\n 4) 시간: '/time 000000'\n 5) 입력값 확인: '/show'\n-------------------------------------\n 6) 여정 검색: '/search'\n")
                        bot.sendMessage(chat_id, "원하는 값을 입력(1~4)하고, 여정을 검색(6) 해 주세요.")

                        letsKorail.login()
                elif text_arr[0] == "/dep":
                        letsKorail.insert("dep", text_arr[1])
                        bot.sendMessage(chat_id, "출발역이 입력 되었습니다.")
                elif text_arr[0] == "/arr":
                        letsKorail.insert("arr", text_arr[1])
                        bot.sendMessage(chat_id, "도착역이 입력 되었습니다.")
                elif text_arr[0] == "/date":
                        letsKorail.insert("date", text_arr[1])
                        bot.sendMessage(chat_id, "날짜가 입력 되었습니다.")
                elif text_arr[0] == "/time":
                        letsKorail.insert("time", text_arr[1])
                        bot.sendMessage(chat_id, "시간이 입력 되었습니다.")
                elif text_arr[0] == "/search":
                        try:
                                trains = letsKorail.search(chat_id)
                                # print(trains)
                                for i, train in enumerate(trains):
                                        bot.sendMessage(chat_id, str("{}. {}".format(i,train)))
                                
                                bot.sendMessage(chat_id, "예약 할 번호를 입력해주세요. 예) '/reserve 0'")
                        except (TypeError, KorailError) as e:
                                print (e)
                                bot.sendMessage(chat_id, "입력값을 확인해주세요.(출발역, 도착역, 날짜, 시간)")
                elif text_arr[0] == "/reserve":
                        try:
                                if letsKorail.getTrainsLength() == 0:
                                        bot.sendMessage(chat_id, "검색된 여정이 없습니다. '/search'를 입력해주세요.")
                                        raise Exception
                                
                                # if(text_arr[1].isdigit()):
                                #train_num = text_arr[1]
                                bot.sendMessage(chat_id, "예약 시도")

                                # async_reserve(is_reserved)
                                t = threading.Thread(target=async_reserve, args=(chat_id, text_arr))
                                t.start()
          
                        except Exception as e :
                                print("expection: {}".format(e))
                elif text_arr[0] == "/stop":
                        global is_reserved
                        is_reserved = False
                        bot.sendMessage(chat_id, "자동 예매가 종료되었습니다.")      

                elif text_arr[0] == "/show":
                        bot.sendMessage(chat_id, letsKorail.getInputString())

                # bot.sendMessage(chat_id, msg['text'])

TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
        timeObject.sleep(10)
        # pass
