from get_mail import GetMail
from validate_rule import Parser
from datetime import datetime
import pprint
from store_data import StoreData

class UpdateMail:
    def __init__(self,filename):
        self.filter = Parser(filename).validate_data()
        # print(self.filter)

    def filter_mail(self):
        obj = GetMail()
        mails = obj.get_mail_id()
        self.user_id = obj.user_id
        self.service = obj.service
        mail_ids = []
        filter_mail = []
        for rule in self.filter['criteria']:
            if self.filter['predicate'] == 'all':
                filter_mail = []
            for mail in mails:
                if (self.filter['predicate'] == 'any') and (mail['id'] in mail_ids):
                    break
                if rule['field'] == 'date':                                                         #Date Filter
                    try:
                        mail_date = datetime.strptime(mail['date'], '%a, %d %b %Y %H:%M:%S %z')
                    except ValueError as err:
                        mail_date = datetime.strptime(mail['date'][:-6] , '%a, %d %b %Y %H:%M:%S %z')

                    if rule['predicate'] == 'after':
                        if(mail_date > rule['value']):
                            filter_mail.append(mail)
                            mail_ids.append(mail['id'])
                    elif rule['predicate'] == 'before':
                        if(mail_date < rule['value']):
                            filter_mail.append(mail)
                            mail_ids.append(mail['id'])

                elif rule['predicate'] == 'contains':
                    if (mail[rule['field']].find(rule['value']) != -1):
                        filter_mail.append(mail)
                        mail_ids.append(mail['id'])

                elif rule['predicate'] == 'does_not_contain':
                    if (mail[rule['field']].find(rule['value']) == -1):
                        filter_mail.append(mail)
                        mail_ids.append(mail['id'])

                elif rule['predicate'] == 'equal_to':
                    if (mail[rule['field']] == rule['value']):
                        filter_mail.append(mail)
                        mail_ids.append(mail['id'])

                elif rule['predicate'] == 'not_equal_to':
                    if (mail[rule['field']] != rule['value']):
                        filter_mail.append(mail)
                        mail_ids.append(mail['id'])

            if(self.filter['predicate'] == 'all'):
                mails = filter_mail

        mail_ids = [x['id'] for x in filter_mail]
        return mail_ids

    def update_mail(self):
        # self.filter_mail()
        action_body = {}
        action_body['ids'] = self.filter_mail()
        for action in self.filter['action']:
            try:
                action_body[action] = self.filter['action'][action]
            except KeyError as err:
                action_body[action] = []
                action_body[action] = self.filter['action'][action]
        return_status = self.service.users().messages().batchModify(userId=self.user_id, body=action_body).execute()
        print(return_status)
        obj = StoreData()
        print(type(action_body['ids']))
        print(action_body['ids'])
        obj.add_data(action_body['ids'])


if __name__ == '__main__':
    obj = UpdateMail('rule.json')
    obj.update_mail()
