with open('/Users/djchoi81/Desktop/church-schedule-app/app.js', 'r') as f:
    js = f.read()

config_old = """const firebaseConfig = {
  apiKey: "AIzaSyDSyk8SUIMDGM9OHh6EciapPp3I7tyOH6o",
  authDomain: "nambooch-c4a73.firebaseapp.com","""

config_new = """const firebaseConfig = {
  apiKey: "AIzaSyDSyk8SUIMDGM9OHh6EciapPp3I7tyOH6o",
  authDomain: "nambooch-c4a73.firebaseapp.com",
  databaseURL: "https://nambooch-c4a73-default-rtdb.firebaseio.com", """

js = js.replace(config_old, config_new)

with open('/Users/djchoi81/Desktop/church-schedule-app/app.js', 'w') as f:
    f.write(js)
