from get_mail import GetMail
from filter_parser import Parser

class UpdateMail:
    def __init__(self,filename):
        self.filename = filename
        self.filter = Parser(self.filename).filter_mail()
        print(self.filter)

    def update_mail(self):
        obj = GetMail('me')
        result = obj.service.users().settings().filters().\
                 create(userId='me', body=self.filter).execute()
        print(result)
        
if __name__ == '__main__':
    obj = UpdateMail('rule.json')
    obj.update_mail()
