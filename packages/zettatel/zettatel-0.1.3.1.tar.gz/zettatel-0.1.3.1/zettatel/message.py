import requests
from messages.resources import send_sms
from zettatel.utils import send_request
import json
import os
from dotenv import load_dotenv
load_dotenv()


class Client:

    def __init__(self, username, password, senderid, output='json', duplicatecheck='true') -> None:
        self.userid = username
        self.password = password
        self.senderid = senderid
        self.output = output
        self.duplicatecheck = duplicatecheck

    def get_api_key(self):
        '''used to read the existing apikey'''

        url = f"https://portal.zettatel.com/SMSApi/apikey/read?userid={self.userid}&password={self.password}&output={self.output}"

        return send_request(url, "GET")

    def create_api_key(self):
        '''used to create a new apikey'''

        response = send_request(
            "https://portal.zettatel.com/SMSApi/apikey/create",
            "POST",
            {'userid': self.userid, 'password': self.password, 'output': self.output})

        return response

    def api_exist(self):
        '''Used to check if an APIKEY registered to the account attached is available and if not it creates one .'''
        global apikey
        api = self.get_api_key()

        if api.json()['response']['code'] == "253":
            try:

                res = self.create_api_key()
                if res.json()["response"]["status"] == 'error':
                    raise ValueError(res.json()["response"]["msg"])

                else:
                    res = self.get_api_key()
                    apikey = res
                    return res.json()['response']['apikeyList']['apikey']

            except Exception as err:
                return str(err)

        else:
            apikey = api
            return api.json()['response']['apikeyList']['apikey']

     # ***********************QUICK SMS*******************************

    def send_quick_SMS(self, to: str, msg: str,):
        """Used to send a quick message to the provided mobile number."""
        try:
            res = send_sms(self.userid, self.password, self.senderid,
                           self.output, self.duplicatecheck, msg, to=to,)
            return res
        except Exception as err:
            return str(err)

    def send_quick_smartlink_sms(self, to: str, msg: str, smartLinkTitle: str):
        """Used to send a message with a link in it. The link will be shortened and assigned the provided smartlink title."""

        try:
            res = send_sms(self.userid, self.password, self.senderid,
                           self.output, self.duplicatecheck, msg, to=to, smartLinkTitle=smartLinkTitle)
            return res
        except Exception as err:
            return str(err)

    def send_quick_sms_Schedule(self, to: str, msg: str, scheduleTime):
        """Sends a scheduled SMS. 'scheduleTime' argument should be passed for it to work"""
        try:
            res = send_sms(self.userid, self.password, self.senderid,
                           self.output, self.duplicatecheck, msg, to=to, scheduleTime=scheduleTime)
            return res
        except Exception as err:
            return str(err)

    # ***********************GROUP SMS*******************************

    def send_group_sms(self, group: str, msg: str):
        '''used to send group message using the zettatel API'''

        try:
            res = send_sms(self.userid, self.password, self.senderid,
                           self.output, self.duplicatecheck, msg, group=group)
            return res
        except Exception as err:
            return str(err)

    def send_group_scheduled_sms(self, group: str, msg: str, scheduleTime):
        '''used to send a scheduled froup message'''

        try:
            res = send_sms(self.userid, self.password, self.senderid,
                           self.output, self.duplicatecheck, msg, group=group, scheduleTime=scheduleTime)
            return res
        except Exception as err:
            return str(err)

    def send_group_smartlink_sms(self, group: str, msg: str, smartLinkTitle):
        '''used to send group message with smartlink in it'''
        try:
            res = send_sms(self.userid, self.password, self.senderid,
                           self.output, self.duplicatecheck, msg, group=group, smartLinkTitle=smartLinkTitle)
            return res
        except Exception as err:
            return str(err)

     # **********************SMS DELIVERY STATUS****************************

    def delivery_status_by_transactionid(self, transactionid: int):
        '''used to get delivery status of a particular message using their transaction ID'''

        url = f"https://portal.zettatel.com/SMSApi/report/status?userid={self.userid}&password={self.password}&apikey= {self.api_exist()}&output={self.output}&uuid={transactionid}"

        return send_request(url, "POST")

    def delivery_status_by_summary(self, groupby='date'):
        '''used to get a summary on message delivery reports'''

        url = f"https://portal.zettatel.com/SMSApi/report/smsSummary?userid={self.userid}&password={self.password}&apikey= {self.api_exist()}&groupby={groupby}&output={self.output}"

        return send_request(url, "POST")

    def delivery_status_by_day(self, date):
        '''Used to get message delivery reports of the particular date given.'''

        url = f"https://portal.zettatel.com/SMSApi/report/day?userid={self.userid}&password={self.password}&apikey= {self.api_exist()}&date={date}&output={self.output}"

        return send_request(url, "POST")

     # **********************Sender ID****************************

    def get_senderID(self):
        '''used to get the senderID registered to the account with the provided credentials'''
        try:
            res = send_request(
                "https://portal.zettatel.com/SMSApi/senderid/read?userid=levin&password=n1xnS9qM&output=json", "GET")
            return res

        except Exception as err:
            return str(err)

    # ********************** Groups ****************************

    def create_group(self):
        try:
            pass
        except Exception as err:
            return str(err)

    def create_group(self, groupname: str):
        '''Used to create a text group'''

        try:
            url = "https://portal.zettatel.com/SMSApi/group/create"

            payload = {'userid': self.userid,
                       'password': self.password,
                       'groupname': groupname,
                       'output': self.output}

            response = send_request(url, "POST", payload)

            return response

        except Exception as err:
            return str(err)

    def get_groups(self):
        '''used to get all the groups attached to the account'''

        try:
            res = send_request(
                f"https://portal.zettatel.com/SMSApi/group/read?userid={self.userid}&password={self.password}&output={self.output}", "GET")
            return res

        except Exception as err:
            return str(err)

    def update_group(self, newgroupname: str, groupid: str):
        '''used to update group name '''

        try:
            url = "https://portal.zettatel.com/SMSApi/group/update"

            payload = {'userid': self.userid,
                       'password': self.password,
                       'groupname': newgroupname,
                       'id': groupid,
                       'output': self.output}
            response = send_request(url, "POST", payload)

            return response

        except Exception as err:
            return str(err)

    def create_group(self, groupid):
        '''used to delete a group'''

        try:
            url = "https://portal.zettatel.com/SMSApi/group/delete"

            payload = {'userid': self.userid,
                       'password': self.password,
                       'id': groupid,
                       'output': self.output}
            response = send_request(url, "POST", payload)

            return response

        except Exception as err:
            return str(err)

    # ********************** Cantacts ****************************

    def create_contact(self, contact_name, mobile_number, group_id):
        '''used to create a new contact in a group'''

        try:
            url = "https://portal.zettatel.com/SMSApi/contact/create"

            payload = {'userid': self.userid,
                       'password': self.password,
                       'contactname': contact_name,
                       'mobileno': mobile_number,
                       'groupid': group_id,
                       'output': 'json'}
            response = send_request(url, "POST", payload)

            return response
        except Exception as err:
            return str(err)

    def update_contact(self, contact_name, mobile_number, group_id):
        '''used to update an existing contact in a group'''

        try:
            url = "https://portal.zettatel.com/SMSApi/contact/upload"

            payload = {'userid': self.userid,
                       'password': self.password,
                       'contactname': contact_name,
                       'mobileno': mobile_number,
                       'groupid': group_id,
                       'output': 'json'}
            response = send_request(url, "POST", payload)

            return response
        except Exception as err:
            return str(err)

    def get_contact(self, group_name):
        '''used to get all contacts in a given group'''

        try:
            response = send_request(
                f"https://portal.zettatel.com/SMSApi/contact/read?userid={self.userid}&password={self.password}&groupname={group_name}&output=json", "GET")

            return response
        except Exception as err:
            return str(err)

    def update_contact(self, contact_name, mobile_number, group_id, contact_id):
        '''used to update a given contact in a group'''

        try:
            url = "https://portal.zettatel.com/SMSApi/contact/update"

            payload = {'userid': self.userid,
                       'password': self.password,
                       'contactname': contact_name,
                       'mobileno': mobile_number,
                       'groupid': group_id,
                       'id': contact_id,
                       'output': 'json'}
            response = send_request(url, "POST", payload)

            return response
        except Exception as err:
            return str(err)

    def delete_contact(self, contact_ids: str):
        '''used to delete a given contact in a group'''

        try:
            url = "https://portal.zettatel.com/SMSApi/contact/delete"

            payload = {'userid': self.userid,
                       'password': self.password,
                       'id': contact_ids,
                       'output': self.output}
            response = send_request(url, "POST", payload)

            return response
        except Exception as err:
            return str(err)
