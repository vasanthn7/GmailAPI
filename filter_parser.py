import json
import pprint

class Parser:
    def __init__(self,filename):
        with open(filename) as json_file:
            self.data = json.load(json_file)

    def filter_mail(self):
        pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(self.data)
        action_dict = { "mark_read": ["removeLabelIds", ['UNREAD']],
                        "mark_unread":["addLabelIds", ['UNREAD']],
                        "add_label":["addLabelIds"],
                        "delete":["addLabelIds", ['TRASH']],
                        "starred":["addLabelIds", ['STARRED']],
                        "archive_message":["removeLabelIds", ['INBOX']]
                    }
        filter_list = ["from","to","subject","label","date","message"]
        filter = {}
        filter['criteria'] = {}
        if(self.data['predicate'] == 'all'):
            for rule in self.data['rules']:
                filter_rule = self.data['rules'][rule]
                if filter_rule['field'] in filter_list:
                    if filter_rule['field'] != 'date':
                        filter['criteria'][filter_rule['field']] = filter_rule['value']
                    else:
                        filter['criteria'][filter_rule['predicate']] = filter_rule['value']
            if 'actions' in self.data:
                filter['action'] = {}
                for action in self.data['actions']:
                    filter_action = self.data['actions'][action]
                    if(filter_action[:9] != 'add_label'):
                        filter['action'][action_dict[filter_action][0]] = action_dict[filter_action][1]
        return filter

if __name__ == '__main__':
    obj = Parser('rule.json')
    filter = obj.filter_mail()
