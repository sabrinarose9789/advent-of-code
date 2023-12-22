# Pulse Propagation

# flip_flop = off & lp = hp; on & lp = lp 
# conjunction =  if all(inputs) = lp else hp 
# broadcaster = gets pulse -> all dest 
# processed in order they are sent 
import queue
import argparse
import pprint

def create_button_graph(filename):
    buttons = {}
    with open(filename) as f:
        for line in f.readlines():
            button, mods = line.strip().split(" -> ")
            letters = button.strip("%&")
            if letters not in buttons:
                buttons[letters] = {}
            buttons[letters]["type"] = "broadcast"
            if button[0] in "&%":
                buttons[letters]["type"] = button[0]
            buttons[letters]["out"] = mods.split(", ")
            for o in buttons[letters]["out"]:
                if o not in buttons:
                    buttons[o] = {}
                if "input" not in buttons[o]:
                    buttons[o]["input"] = {}
                buttons[o]["input"][letters] = "low"
            if button[0] == "%":
                buttons[letters]["on"] = False 
    pulses = {"low": 0, "high": 0}
    for i in range(10000):
        press_button(buttons, pulses, i)
        if i == 999:
            print(pulses["low"] * pulses["high"])
    m = 1
    for p, val in pulses.items():
        if p not in ('low', 'high'):
            m *= val[0] 
    print(m)



def press_button(buttons, pulses, i):
    pressed_buttons = queue.Queue()
    pressed_buttons.put(("low", "broadcaster", "input"))

    while pressed_buttons:
        if pressed_buttons.empty():
            break
        pulse, button, input = pressed_buttons.get()
        pulses[pulse] += 1 
        b = buttons[button]
        if button == "rx" and pulse == "low":
            print(i)
        if "type" not in b:
            continue
        if b["type"] == "%":
            if pulse == "low":
                if b["on"]:
                    new_pulse = "low"
                else:
                    new_pulse = "high"
                b["on"] = not b["on"]
                for next_mod in b["out"]:
                    pressed_buttons.put((new_pulse, next_mod, button))
        elif b["type"] == "&":
            b["input"][input] = pulse
            if button == "dd" and pulse == "high":
                if input not in pulses:
                    pulses[input] =  (i, True)
                elif pulses[input][0]:
                    pulses[input] = (i - pulses[input][0], False)
            new_pulse = "high"
            if  all(x == "high" for x in b["input"].values()):
                new_pulse = "low"
            for next_mod in b["out"]:
                pressed_buttons.put((new_pulse, next_mod, button))
        else:
            for next_mod in b["out"]:
                pressed_buttons.put((pulse, next_mod, button))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "Pulse Propagation",
                description = 'Follow the buttons'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    create_button_graph(args.filename)
                        

