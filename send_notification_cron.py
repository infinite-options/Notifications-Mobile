#!/usr/bin/python2.7
from NotificationHub import AzureNotification
from NotificationHub import AzureNotificationHub
#import datetime
import urllib
import requests
import datetime, pytz
import json
import re
import os
from datetime import date
from pytz import timezone

import mysql.connector

mydb = mysql.connector.connect(
          host='io-mysqldb8.cxjnrciilyjq.us-west-1.rds.amazonaws.com',
          user='admin',
          password='prashant',
          database='manifest',
          port = 3306
                  )
def notify(msg,tag):
	#print(msg,tag)
	#return
	isDebug = True
	#hub = AzureNotificationHub("Endpoint=sb://serving-fresh-notification-namespace.servicebus.windows.net/;SharedAccessKeyName=DefaultFullSharedAccessSignature;SharedAccessKey=Yy/PhzWba6vmrM8geyHmKTVQPocwrDVcVlqAiokvHe4=", "Serving-Fresh-Notification-Hub", isDebug)
        hub = AzureNotificationHub("Endpoint=sb://manifest-notifications-namespace.servicebus.windows.net/;SharedAccessKeyName=DefaultFullSharedAccessSignature;SharedAccessKey=UWW7o7LFe8Oz6FZUQQ/gaNgqSfdN4Ckp6FCVCm3xuVg=", "Manifest-Notification-Hub", isDebug)



	#wns_payload = "{\"aps\":{\"alert\":\"Notification Hub test notification\"}}"
	wns_payload = {
	    'aps':
	        {
	            'alert': msg
	        }
	}
	hub.send_apple_notification(0, wns_payload,tag)

	#wns_payload ="""{\n\"notification\":{\n\"title\":\"Notification Hub Test Notification\",\n\"body\":\"This is a sample notification delivered by Azure Notification Hubs.\"\n},\n\"data\":{\n\"property1\":\"value1\",\n\"property2\":42\n}\n}"""

	wns_payload = {
		"notification":{
			"title":"Hi",
			"body": msg
		},
		"data":{
			"property1":"value1",
			"property2":42
		}
	}
	hub.send_google_notification(0, wns_payload,tag)

utc_time =datetime.datetime.now(pytz.utc)
#utc_time = utc_time + datetime.timedelta(seconds=170)

#utc_timezone = pytz.timezone('UTC')
#utc_time = utc_timezone.localize(utc_time)
#utc_time = utc_time.astimezone(utc_timezone)


url = 'https://3s3sftsr90.execute-api.us-west-1.amazonaws.com/dev/api/v2/getNotifications'
#    post_url = 'https://3s3sftsr90.execute-api.us-west-1.amazonaws.com/dev/api/v2/changeHistory/'
json_url = urllib.urlopen(url)
data=json.loads(json_url.read())
#print(data)

def getGUID(n):
	s = ''
	#debug print('inside getGUID')
	if 'guid' in n:
		guid = str(n['guid'])
		guid_list =guid.split(' ')
                l =[]
                print("guid_list_len")
		if(len(guid_list)> 1):
                    for i in range(len(guid_list)):
                        #if(guid_list[i]=="guid"):
                        if(re.search('guid', guid_list[i])):
                            s='guid_'+guid_list[i+1][1:-2]
                            print(s)
                            l.append(s)
                            s=''
                            print(l)
	return l
def changedate(obj):
	sdate = date.today()
	obj =obj.replace(day = sdate.day, month = sdate.month, year = sdate.year)
	return obj

def getnotificationtime(op,t,obj):
	hours,mins,seconds = t.split(':')
	total_seconds = int(hours)*3600 + int(mins)*60 + int(seconds)
	#debug print(t, total_seconds)
	if(op == 'before'):			
		result_time = obj -  datetime.timedelta(seconds=total_seconds)
	elif(op == 'during' or op == 'after'):
		result_time = obj +  datetime.timedelta(seconds=total_seconds)
	else:
		print('Unrecognized opcode!!!')
	tz = timezone('America/Los_Angeles')
        result_time = tz.localize(result_time)
	#result_time= result_time.replace(tzinfo=tz)
        print(result_time)
        #backup = result_time
	#result_time = result_time + datetime.timedelta(seconds=420)
        #result_time = result_time.replace(day = backup.day, month = backup.month, year = backup.year)
        print(result_time)
	return result_time.astimezone(timezone('UTC'))

#main
logfilename = str(datetime.datetime.now(pytz.UTC).date())+'.log'
logfilepath = '/home/sharmilasabarathinam/logs/notification/'+logfilename
if os.path.exists(logfilepath):
    fileop = "a"
else:
    fileop = "w" 
f= open(logfilepath,fileop)
#f.write("Inside manifest")
for d in data['result']:
  #if(d['gr_unique_id']=='300-000458'):
    if('notifications' in d):
        print(d['start_day_and_time'])
	print(d['end_day_and_time'])
	if(d['is_displayed_today'] == 'True' and d['is_complete'] == 'False'):
		start_day_and_time_obj = datetime.datetime.strptime(d['start_day_and_time'], '%m/%d/%Y, %I:%M:%S %p')
                print('start_time')
		start_day_and_time_obj =changedate(start_day_and_time_obj)
		end_day_and_time_obj = datetime.datetime.strptime(d['end_day_and_time'], '%m/%d/%Y, %I:%M:%S %p')
                print('end_time')
		end_day_and_time_obj = changedate(end_day_and_time_obj)
		start_day_and_time_obj = start_day_and_time_obj.replace(second = 0)
		end_day_and_time_obj = end_day_and_time_obj.replace(second = 0)
		#print(date_time_obj.strftime('%m/%d/%Y, %I:%M:%S %p'))
		for n in d['notifications']:
			if(n['before_is_enable'] == 'True'):
				before_not_time = getnotificationtime('before', n['before_time'], start_day_and_time_obj)
                                print('before_notification_time')
                                before_not_time = changedate(before_not_time)
                                print(before_not_time)
                                print("UTC Time")
                                print(utc_time)
				time_diff= utc_time - before_not_time
                                print('time_diff')
                                print(time_diff)
				#notify(n['before_message']+n['before_time'])
				if(time_diff.total_seconds() < 10 and time_diff.total_seconds() > -10):
                                    for id in getGUID(n):
				       #id = getGUID(n)
					if (id != ''):
						notify(n['before_message'],id)
                                                mycursor = mydb.cursor()
                                                sql = "UPDATE notifications SET before_is_set = 'True' WHERE notification_id = '"+str(n['notification_id'])+"'"
                                                mycursor.execute(sql)
                                                mydb.commit()
						f.write(n['before_message']+ ' ')
						f.write(id+' ')
						f.write(str(before_not_time)+ ' ')
						f.write('\n')
				print(n['before_time'])
				print(n['before_message'])
			
				print(utc_time)
				print(time_diff.total_seconds())
				print('\n')
			if(n['during_is_enable'] == 'True'):
				during_not_time = getnotificationtime('during', n['during_time'], start_day_and_time_obj)
                                during_not_time = changedate(during_not_time)
				time_diff= utc_time - during_not_time
				#notify(n['during_message']+n['during_time'])
				if(time_diff.total_seconds() < 10 and time_diff.total_seconds() > -10):
                                    for id in getGUID(n):
				       #id = getGUID(n)
					if (id != ''):
						notify(n['during_message'],id)
                                                mycursor = mydb.cursor()
                                                sql = "UPDATE notifications SET during_is_set = 'True' WHERE notification_id = '"+str(n['notification_id'])+"'"
                                                mycursor.execute(sql)
                                                mydb.commit()
						f.write(n['during_message']+ ' ')
						f.write(id+ ' ')
						f.write(str(during_not_time)+ ' ')
						f.write('\n')
				print(n['during_time'])
				print(n['during_message'])
				print(during_not_time)
				print(time_diff.total_seconds())
				print('\n')
			if(n['after_is_enable'] == 'True'):
				after_not_time = getnotificationtime('after', n['after_time'], end_day_and_time_obj)
                                after_not_time = changedate(after_not_time)
				time_diff= utc_time - after_not_time
				#notify(n['after_message']+n['after_time'])
				if(time_diff.total_seconds() < 10 and time_diff.total_seconds() > -10):
                                    for id in getGUID(n):
				       #id = getGUID(n)
					if (id != ''):
						notify(n['after_message'],id)
                                                mycursor = mydb.cursor()
                                                sql = "UPDATE notifications SET after_is_set = 'True' WHERE notification_id = '"+str(n['notification_id'])+"'"
                                                mycursor.execute(sql)
                                                mydb.commit()
						f.write(n['after_message']+ ' ')
						f.write(id+' ')
						f.write(str(after_not_time)+' ')
						f.write('\n')
				print(n['after_time'])
				print(n['after_message'])
			        print(after_not_time)
				print(time_diff.total_seconds())
				print('\n')	
f.close()
		

























































































