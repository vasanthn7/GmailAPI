from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64,pprint

from filter_parser import Parser

class GetMail:
    def __init__(self,user_id):
        self.SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
        self.user_id = user_id
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', self.SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('gmail', 'v1', http=creds.authorize(Http()))

    def get_mail_id(self):
        mail_data = []

        results = self.service.users().messages().list(userId=self.user_id,).execute()
        for message in results['messages']:
            data = {}
            content = self.service.users().messages().get(userId='me', id=message['id']).execute()

            data['id'] = message['id']
            data['labels'] = ' '.join(content['labelIds'])
            try:
                data['message'] = base64.urlsafe_b64decode(content['payload']['parts'][0]['body']['data']).decode('utf-8')
            except KeyError as err:
                try:
                    data['message'] = base64.urlsafe_b64decode(content['payload']['body']['data']).decode('utf-8')
                except KeyError as err:
                    if(0 == content['payload']['body']['size']):
                        print("Empty Message")
                        data['message'] = ''


            headers = content['payload']['headers']
            for header in headers:
                if header['name'] == 'Subject':
                    data['subject'] = header['value']
                elif header['name'] == 'Date':
                    data['date'] = header['value']
                elif header['name'] == 'From':
                    data['from'] = header['value']
                elif header['name'] == 'To':
                    data['to'] = header['value']
            mail_data.append(data)
        return mail_data

    # def update_mail(self,filename):
    #     # filter = Parser(filename).filter_mail()
    #     filter = {
    #         'criteria': {
    #             'from': 'vasanthn7.com'
    #         },
    #         'action': {
    #             'removeLabelIds': ['INBOX']
    #         }
    #     }
    #     result = self.service.users().settings().filters().create(userId='me', body=filter).execute()

if __name__ == '__main__':
    obj = GetMail('me')
    obj.get_mail_id()
