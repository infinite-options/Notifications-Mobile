#!/usr/bin/python2.7
from NotificationHub import AzureNotification
from NotificationHub import AzureNotificationHub
#import datetime
import urllib
import requests
import datetime, pytz
import json
from datetime import date
from pytz import timezone


def notify(msg,tag):
	#print(msg,tag)
	#return
	isDebug = True
	hub = AzureNotificationHub("Endpoint=sb://serving-fresh-notification-namespace.servicebus.windows.net/;SharedAccessKeyName=DefaultFullSharedAccessSignature;SharedAccessKey=Yy/PhzWba6vmrM8geyHmKTVQPocwrDVcVlqAiokvHe4=", "Serving-Fresh-Notification-Hub", isDebug)

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
		if(len(guid_list)> 1):
			s='guid_'+guid_list[2][1:-2]
	#debug print(s)
	return s
def changedate(obj):
	sdate = date.today() 
	obj =obj.replace(day = sdate.day, month = sdate.month, year = sdate.year)
	#debug print( obj)
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
	result_time= result_time.replace(tzinfo=tz)
	#debug print(result_time)
	return result_time.astimezone(timezone('UTC'))

f= open("sendnotification.log","a")
for d in data['result']:
	#if(d['gr_unique_id'] == '300-000181'):
	#debug print(d['start_day_and_time'])
	#debug print(d['end_day_and_time'])
	if(d['is_displayed_today'] == 'True'):
		start_day_and_time_obj = datetime.datetime.strptime(d['start_day_and_time'], '%m/%d/%Y, %I:%M:%S %p')
		start_day_and_time_obj =changedate(start_day_and_time_obj)
		end_day_and_time_obj = datetime.datetime.strptime(d['end_day_and_time'], '%m/%d/%Y, %I:%M:%S %p')
		end_day_and_time_obj = changedate(end_day_and_time_obj)
		start_day_and_time_obj = start_day_and_time_obj.replace(second = 0)
		end_day_and_time_obj = end_day_and_time_obj.replace(second = 0)
		#print(date_time_obj.strftime('%m/%d/%Y, %I:%M:%S %p'))
		for n in d['notifications']:
			if(n['before_is_enable'] == 'True'):
				before_not_time = getnotificationtime('before', n['before_time'], start_day_and_time_obj)
				time_diff= utc_time - before_not_time
				#notify(n['before_message']+n['before_time'])
				if(time_diff.total_seconds() < 10 and time_diff.total_seconds() > -10):
					id = getGUID(n)
					if (id != ''):
						notify(n['before_message'],id)
						f.write(n['before_message'])
						f.write(id+' ')
						f.write(str(before_not_time)+ ' ')
						f.write('\n')
				#debug print(n['before_time'])
				#debug print(n['before_message'])
			
				#debug print(utc_time)
				#debug print(time_diff.total_seconds())
				print('\n')
			if(n['during_is_enable'] == 'True'):
				during_not_time = getnotificationtime('during', n['during_time'], start_day_and_time_obj)
				time_diff= utc_time - during_not_time
				#notify(n['during_message']+n['during_time'])
				if(time_diff.total_seconds() < 10 and time_diff.total_seconds() > -10):
					id = getGUID(n)
					if (id != ''):
						notify(n['during_message'],id)
						f.write(n['during_message'])
						f.write(id+ ' ')
						f.write(str(during_not_time)+ ' ')
						f.write('\n')
				#debug print(n['during_time'])
				#debug print(n['during_message'])
				#debug print(during_not_time)
				#debug print(time_diff.total_seconds())
				print('\n')
			if(n['after_is_enable'] == 'True'):
				after_not_time = getnotificationtime('after', n['after_time'], end_day_and_time_obj)
				time_diff= utc_time - after_not_time
				#notify(n['after_message']+n['after_time'])
				if(time_diff.total_seconds() < 10 and time_diff.total_seconds() > -10):
					id = getGUID(n)
					if (id != ''):
						notify(n['after_message'],id)
						f.write(n['after_message'])
						f.write(id+' ')
						f.write(str(after_not_time)+' ')
						f.write('\n')
				#debug print(n['after_time'])
				#debug print(n['after_message'])
				#debug print(after_not_time)
				#debug print(time_diff.total_seconds())
				print('\n')	
f.close()
		












































