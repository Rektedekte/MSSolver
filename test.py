import keyboard
import mouse

assign_var = None


def key_express(key):
    global assign_var
    assign_var = {"module": "keyboard", "key": key.name}


def mouse_express(button):
    if isinstance(button, mouse.ButtonEvent):
        global assign_var
        assign_var = {"module": "mouse", "key": button.button}


keyboard.on_press(key_express)
mouse.hook(mouse_express)

while not assign_var:
    pass

print(assign_var)

target_module = globals()[assign_var["module"]]
target_module.press(assign_var["key"])
