#!/usr/bin/python2.7
from NotificationHub import AzureNotification
from NotificationHub import AzureNotificationHub
#import datetime
import urllib
import requests
import datetime, pytz
import json
from pytz import timezone


def notify(msg):
	
	isDebug = True
	hub = AzureNotificationHub("Endpoint=sb://serving-fresh-notification-namespace.servicebus.windows.net/;SharedAccessKeyName=DefaultFullSharedAccessSignature;SharedAccessKey=Yy/PhzWba6vmrM8geyHmKTVQPocwrDVcVlqAiokvHe4=", "Serving-Fresh-Notification-Hub", isDebug)

	#wns_payload = "{\"aps\":{\"alert\":\"Notification Hub test notification\"}}"
	wns_payload = {
	    'aps':
	        {
	            'alert': msg
	        }
	}
	hub.send_apple_notification(0, wns_payload)

	#wns_payload ="""{\n\"notification\":{\n\"title\":\"Notification Hub Test Notification\",\n\"body\":\"This is a sample notification delivered by Azure Notification Hubs.\"\n},\n\"data\":{\n\"property1\":\"value1\",\n\"property2\":42\n}\n}"""

	wns_payload = {
		"notification":{
			"title":"Hi",
			"body":"Hi_Everyone!!!"
		},
		"data":{
			"property1":"value1",
			"property2":42
		}
	}
	#hub.send_google_notification(0, wns_payload)

utc_time =datetime.datetime.now(pytz.utc)
#utc_timezone = pytz.timezone('UTC')
#utc_time = utc_timezone.localize(utc_time)
#utc_time = utc_time.astimezone(utc_timezone)


url = 'https://3s3sftsr90.execute-api.us-west-1.amazonaws.com/dev/api/v2/getgoalsandroutines'
#    post_url = 'https://3s3sftsr90.execute-api.us-west-1.amazonaws.com/dev/api/v2/changeHistory/'
json_url = urllib.urlopen(url)
data=json.loads(json_url.read())
#print(data)

def getnotificationtime(op,t,obj):
	hours,mins,seconds = t.split(':')
	total_seconds = int(hours)*3600 + int(mins)*60 + int(seconds)
	print(t, total_seconds)
	if(op == 'before'):			
		result_time = obj -  datetime.timedelta(seconds=total_seconds)
	elif(op == 'during' or op == 'after'):
		result_time = obj +  datetime.timedelta(seconds=total_seconds)
	else:
		print('Unrecognized opcode!!!')
	tz = timezone('America/Los_Angeles')
	result_time= result_time.replace(tzinfo=tz)
	return result_time.astimezone(timezone('UTC'))

for d in data['result']:
	if(d['gr_unique_id'] == '300-000181'):
		print(d['start_day_and_time'])
		print(d['end_day_and_time'])
		start_day_and_time_obj = datetime.datetime.strptime(d['start_day_and_time'], '%m/%d/%Y, %I:%M:%S %p')
		end_day_and_time_obj = datetime.datetime.strptime(d['end_day_and_time'], '%m/%d/%Y, %I:%M:%S %p')
		start_day_and_time_obj = start_day_and_time_obj.replace(second = 0)
		end_day_and_time_obj = end_day_and_time_obj.replace(second = 0)
		#print(date_time_obj.strftime('%m/%d/%Y, %I:%M:%S %p'))
		for n in d['notifications']:
			if(n['before_is_enable'] == 'True'):
				before_not_time = getnotificationtime('before', n['before_time'], start_day_and_time_obj)
				time_diff= utc_time - before_not_time
				#notify(n['before_message']+n['before_time'])
				if(time_diff.total_seconds() < 10 and time_diff.total_seconds() > -10):
					notify(n['before_message']+n['before_time'])
				print(n['before_time'])
				print(n['before_message'])
				print(before_not_time)
				print(utc_time)
				print(time_diff.total_seconds())
				print('\n')
			if(n['during_is_enable'] == 'True'):
				during_not_time = getnotificationtime('during', n['during_time'], start_day_and_time_obj)
				time_diff= utc_time - during_not_time
				#notify(n['during_message']+n['during_time'])
				if(time_diff.total_seconds() < 10 and time_diff.total_seconds() > -10):
					notify(n['during_message']+n['during_time'])
				print(n['during_time'])
				print(n['during_message'])
				print(during_not_time)
				print(time_diff.total_seconds())
				print('\n')
			if(n['after_is_enable'] == 'True'):
				after_not_time = getnotificationtime('after', n['after_time'], end_day_and_time_obj)
				time_diff= utc_time - after_not_time
				#notify(n['after_message']+n['after_time'])
				if(time_diff.total_seconds() < 10 and time_diff.total_seconds() > -10):
					notify(n['after_message']+n['after_time'])
				print(n['after_time'])
				print(n['after_message'])
				print(after_not_time)
				print(time_diff.total_seconds())
				print('\n')	
			
		
















