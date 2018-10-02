
Instructions

Initial Predicate contains either 'all' or 'any'
'all' indicates that all the given conditions must match in order to run the actions.
'any' indicates that at least one of the conditions must match in order to run the
conditions.
Rules:
rules have a list of sub_rules.
fields include `from`,`to`,`subject`,`message`,`labels` and `date`
predicates for `date` are `after` and `before`
predicates for other fields include contains, does_not_contain
value for `date` is in the format `%Y/%m/%d`
value for other fields is a string

Actions:
action has a list of actions that will occur on the order of declaration
actions include `mark_read`, `mark_unread`, `add_label`, `delete`, `starred` and `archive_message`
the add_label action is followed by a string, which will be added to the labels(e.g. `"action_1" :"add_label Important"`)
