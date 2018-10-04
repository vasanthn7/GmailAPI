
# Instructions

* Initial Predicate contains either 'all' or 'any'
* 'all' indicates that all the given conditions must match in order to run the actions.
* 'any' indicates that at least one of the conditions must match in order to run the conditions.

## Rules:
* `rules` have a list of sub_rules.
* Each sub_rule is a dictionary with three "key": "value" pair
* fields include `from`,`to`,`subject`,`message`,`labels` and `date`
* predicates for `date` are `after` and `before`
* predicates for other fields include `contains`, `does_not_contain`, `equal_to`, and `not_equal_to`
* value for `date` is in the format `%Y/%m/%d`
* value for other fields is a string
### Example
```
"rules": [
    {
        "field":"date",
        "predicate": "before",
        "value":"2018/10/03"
    },
    {
        "field":"message",
        "predicate": "does_not_contain",
        "value":"Test"
    }
]
```

## Actions:
* `actions` has a list of actions that will occur on the order of declaration
* actions include `mark_read`, `mark_unread`, `add_label`, `delete`, `starred`, `archive_message` and `restore_message`
###Example
```
"actions":["mark_read","starred", "restore_message"]
```

**Refer rule.json for sample**
