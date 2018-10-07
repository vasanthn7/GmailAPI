import json, pprint, pytz
from datetime import datetime

class Parser:
    def __init__(self,filename):
        with open(filename) as json_file:
            self.data = json.load(json_file)
            if(self.data['predicate'] != 'any' and self.data['predicate'] != 'all'):
                print("Invalid predicate \'" + self.data['predicate'] + "\'")
                print("Setting predicate to \'all\'")
                self.data['predicate'] = 'all'

    def validate_data(self):
        action_dict = { "mark_read": ["removeLabelIds", 'UNREAD'],
                        "mark_unread":["addLabelIds", 'UNREAD'],
                        "add_label":["addLabelIds"],
                        "delete":["addLabelIds", 'TRASH'],
                        "starred":["addLabelIds", 'STARRED'],
                        "archive_message":["removeLabelIds", 'INBOX'],
                        "restore_message":["addLabelIds", 'INBOX']
                    }
        filter_list = ["from","to","subject","label","date","message"]
        date_predicate = ['after','before']
        other_predicate = ['contains', 'does_not_contain', 'equal_to', 'not_equal_to']

        filter = {}
        filter['criteria'] = []
        filter['predicate'] = self.data['predicate']
        for rule in self.data['rules']:
            if rule['field'] in filter_list:
                if((rule['field'] == 'date' and rule['predicate'] in date_predicate) or (rule['field'] != 'date' and rule['predicate'] in other_predicate)):
                    if rule['field'] == 'date':
                        try:
                            rule['value'] = datetime.strptime(rule['value'], '%Y/%m/%d')
                            rule['value'] = rule['value'].replace(tzinfo=pytz.timezone('Asia/Kolkata'))
                        except ValueError as err:
                            print("Invalid date format, Omitting")
                            break
                    filter['criteria'].append(rule)
                else:
                    print("Invalid filter predicate \'" + rule['predicate']+ " \', Omitting")
            else:
                print("Invalid Filter \'" + rule['field']+ " \', Omitting")
        if 'actions' in self.data:
            filter['action'] = {}
            for action in self.data['actions']:
                if action in action_dict.keys():
                    try:
                        filter['action'][action_dict[action][0]].append(action_dict[action][1])
                    except KeyError as err:
                        filter['action'][action_dict[action][0]] = []
                        filter['action'][action_dict[action][0]].append(action_dict[action][1])
                else:
                    print("Invalid Action \'" + action + "\', Omitting")

        return filter

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    obj = Parser('rule.json')
    pp.pprint(obj.validate_data())
