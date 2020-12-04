#!/usr/bin/python2.7
from NotificationHub import AzureNotification
from NotificationHub import AzureNotificationHub
import datetime

x = datetime.datetime.now()


now = x.strftime("%c")

isDebug = True
hub = AzureNotificationHub("Endpoint=sb://serving-fresh-notification-namespace.servicebus.windows.net/;SharedAccessKeyName=DefaultFullSharedAccessSignature;SharedAccessKey=Yy/PhzWba6vmrM8geyHmKTVQPocwrDVcVlqAiokvHe4=", "Serving-Fresh-Notification-Hub", isDebug)

#wns_payload = "{\"aps\":{\"alert\":\"Notification Hub test notification\"}}"
wns_payload = {
    'aps':
        {
            'alert': 'Alert Created at '+ now
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

