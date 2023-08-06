# ConsentiumThingsPy

Under construction! Not ready for use yet! Currently experimenting and planning!

Developed by Debjyoti Chowdhury from ConsentiumInc

## Examples of How To Use (Buggy Alpha Version)

Creating A Server

```python
from ConsentiumThingsPy import ThingsUpdate
import time

api_key = "Your send API key"

board = ThingsUpdate(key=api_key)


# When You Are Done create sensor and info bucket
sensor_val = [1, 2, 3, 4, 5, 6, 7]
info_buff = ["a", "b", "c", "d", "e", "f", "g"]

while True:
    r = board.sendREST(sensor_val=sensor_val, info_buff=info_buff)
    print(r)
    time.sleep(5)
```
