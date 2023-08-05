# Zetattel

An SDK to help send messages through the zettatel API

# Usage

## Quick sms

to use this package, you can either git clone or install using pip:

```
pip install message==0.1.3
```

This will install all the required packages. Next we need to initialize the packacge as shown below:

```
from zettatel.message import Client

message = Client(
    "username",
    "password",
    "senderId"
)
```

To send a quick message use the following sample:

```
message.send_quick_SMS('254712345678', "this is test from python package")
```

To send a scheduled quick sms :

```
message.send_quick_smartlink_sms(
    '254712345678', "this is test from python package",scheduleTime = '2023-09-16 13:24')
```

## Group SMS

1. To send message to a group:

```
message.send_group_sms("group name","message")
```

2. To send a scheduled group sms

```
message.send_group_scheduled_sms("group name","message","scheduledTime eg 2023-09-16 13:24")
```

## Delivery Status

1. Get delivery status by transaction ID:

```
message.delivery_status_by_transactionid("transactionid: int")
```

2. Get message delivery report of a particular day:

```
message.delivery_status_by_day("date")
```

3. Get overal delivery report summary:

```
message.delivery_status_by_summary()
```

## Sender ID

to get your sender Id use :

```

res = message.get_senderID()
print(res.text)

```

## Groups

1. To create a group:

```

message.create_group("groupname")

```

2. To get all the groups:

```

message.get_groups()

```

3. To update a group:

```

message.update_group("newgroupname","groupid")

```

## Contacts

This are teh contacts that will be available in the specified groups.

1. To create conntacts:

```

message.create_contact("contact name","mobile number","group id")

```

2. To update contact:

```

message.update_contact("contact name","mobile number","group id")

```

3. To get all the contacts in a group:

```

message.get_contact("group name")


```
