from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64,pprint


class GetMail:
    def __init__(self):
        self.SCOPES = 'https://www.googleapis.com/auth/gmail.settings.basic https://mail.google.com/ https://www.googleapis.com/auth/userinfo.profile'
        store = file.Storage('token.json')
        self.creds = store.get()
        if not self.creds or self.creds.invalid:
            flow = client.flow_from_clientsecrets('client_id.json', self.SCOPES)
            self.creds = tools.run_flow(flow, store)

        user_info_service = build(
            serviceName='oauth2', version='v2',
            http=self.creds.authorize(Http()))
        user_info = None
        user_info = user_info_service.userinfo().get().execute()
        if user_info and user_info.get('id'):
            self.user_id = user_info.get('id')
            # print(self.user_id)
        else:
            raise NoUserIdException()

        self.service = build('gmail', 'v1', http=self.creds.authorize(Http()))


    def get_mail_id(self,*args):
        mail_data = []
        if (len(args) == 1):
            results = {}
            results['messages'] = []
            for mail_id in args[0]:
                results['messages'].append({'id': mail_id})
            # print(results)
        else:
            results = self.service.users().messages().list(userId=self.user_id,).execute()
            print(results)
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

    # def get_user_info(self):


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
    obj = GetMail()
    print(obj.get_mail_id(['1663f2ea2e0c9bad','1663f2ea2e0c9bad']))
