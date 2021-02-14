beeminderpy
===========

Python wrapper for Beeminder API.

Example:
```
from beeminderpy.beeminderpy import Beeminder
beeminder = Beeminder("API_KEY_HERE")

args = {
	"username": "my-username",
	"goalname": "my-goal",
	"daystamp": my_timestamp.date(),
	"value": 123,
	"comment": "Added by TU at %s" % datetime.datetime.now()
	}
beeminder.create_datapoint(**args)
print("Beeminder goal %s: committed datapoint %s" % (goal_name, args))
```
