# TimeExtral_advanced

### Purpose
The purpose of this module is to provide users with convenient commands and more precise time measurements, as well as the ability to set specific values for variables such as x and y. Some examples of these commands include waitms, waitns, sleep, calctime, set-x, and set-y.


## How To Install

You can install the module TimeExtral_advanced by typing `pip install TimeExtral_advanced` or if you're using pip3: `pip3 install yourmodulenamehere`

## Examples
```py
import TimeExtral_advanced
import requests

print("The Word 'Hi' will appear in 5 seconds.")
TimeExtral_advanced.waitms(5000)
print("Hi!")
TimeExtral_advanced.sleep(5)
HTML = requests.post("https://youtube.com/").text
print("The html code of youtube.com at this moment is:\n\n\n" + HTML)
```