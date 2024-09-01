#  Copyright (c) <2020>, <George Stavrinos>
#  All rights reserved.

#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#  * Redistributions of source code must retain the above copyright
#  notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#  notice, this list of conditions and the following disclaimer in the
#  documentation and/or other materials provided with the distribution.
#  * Neither the name of the <organization> nor the
#  names of its contributors may be used to endorse or promote products
#  derived from this software without specific prior written permission.

#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import random
import platform
from time import sleep
import pyautogui as pag

if platform.system() == "Windows":
    import pydirectinput as pdi

result = None
controller = pag
path = os.path.dirname(os.path.realpath(__file__))

class command:
    fn = None
    sz = 0
    args = []
    add = []
    def __init__(self, f,s,a,aa):
        self.fn = f
        self.sz = s
        self.args = a
        self.add = aa

def direct_input(en):
    global controller
    controller = pdi if en else pag

def press(key):
    controller.press(key)

def click(x,y,button):
    controller.click(x,y, button=button)

def mouseDown(x,y,button):
    controller.mouseDown(x,y, button=button)

def mouseUp(x,y,button):
    controller.mouseUp(x,y, button=button)

def mouseTo(x,y):
    controller.moveTo(x,y)

def select(s, confidence, once=False):
    while(True):
        target = None
        try:
            target = pag.locateOnScreen(s, confidence=confidence)
        except:
            pass
        if target:
            return pag.center(target)
        if once:
            return target

def selectThenClick(s, confidence, button):
    try:
        target = select(s, confidence)
        print(target)
        click(target[0],target[1],button=button)
    except Exception as e:
        print(e)
        print("Could not find:"+str(s))

def selectThenMouseDown(s, confidence, button):
    try:
        target = select(s, confidence)
        print(target)
        mouseDown(target[0],target[1],button=button)
    except Exception as e:
        print(e)
        print("Could not find:"+str(s))

def selectThenMouseUp(s, confidence, button):
    try:
        target = select(s, confidence)
        mouseUp(target[0],target[1],button=button)
    except:
        print("Could not find:"+str(s))

def selectThenPress(s, confidence, button):
    try:
        target = select(s, confidence)
        mouseTo(target[0], target[1])
        press(button)
    except:
        print("Could not find:"+str(s))

def checkFor(s, confidence):
    try:
        return select(s, confidence, True) is not None
    except:
        return False

commands = {
    "windows_mode": command(direct_input,1,[],[]),
    "keyboard_press": command(press,1,[],[]),
    "left_click": command(click,2,[],["left"]),
    "right_click": command(click,2,[],["right"]),
    "middle_click": command(click,2,[],["middle"]),
    "left_mouse_down": command(mouseDown,2,[],["left"]),
    "right_mouse_down": command(mouseDown,2,[],["right"]),
    "middle_mouse_down": command(mouseDown,2,[],["middle"]),
    "left_mouse_up": command(mouseUp,2,[],["left"]),
    "right_mouse_up": command(mouseUp,2,[],["right"]),
    "middle_mouse_up": command(mouseUp,2,[],["middle"]),
    "mouse_move": command(mouseTo,2,[],[]),
    "wait_for_this": command(select,2,[],[]),
    "find_and_left_click": command(selectThenClick,2,[],["left"]),
    "find_and_right_click": command(selectThenClick,2,[],["right"]),
    "find_and_middle_click": command(selectThenClick,2,[],["middle"]),
    "find_and_left_mouse_down": command(selectThenClick,2,[],["left"]),
    "find_and_right_mouse_down": command(selectThenClick,2,[],["right"]),
    "find_and_middle_mouse_down": command(selectThenClick,2,[],["middle"]),
    "find_and_left_mouse_up": command(selectThenClick,2,[],["left"]),
    "find_and_right_mouse_up": command(selectThenClick,2,[],["right"]),
    "find_and_middle_mouse_up": command(selectThenClick,2,[],["middle"]),
    "find_and_press": command(selectThenPress,3,[],[]), # Moves mouse and then presses the keyboard button
    "wait": command(sleep, 1, [], []),
    "check_for": command(checkFor, 2, [], [])
}

def commandTranslation(com, condition=None):
    c = commands[com[0]]
    print(com[0])
    print(c)
    if c:
        c.sz = len(com)-1
        if len(com) >= 2:
            c.args = com[1:]
        else:
            print("Not enough arguments for command: "+str(com))
            exit()
        if len(c.args) != c.sz:
            print("Command arguments do not match the required number: "+str(com))
            exit()
    if c.fn == commands["keyboard_press"].fn:
        c.fn(c.args[0])
        print("Pressing "+c.args[0])
    elif c.fn == commands["left_click"].fn or c.fn == commands["right_click"].fn or c.fn == commands["middle_click"].fn or c.fn == commands["left_mouse_down"].fn or c.fn == commands["right_mouse_down"].fn or c.fn == commands["middle_mouse_down"].fn or c.fn == commands["left_mouse_up"].fn or c.fn == commands["right_mouse_up"].fn or c.fn == commands["middle_mouse_up"].fn:
        c.fn(int(c.args[0]),int(c.args[1]),c.add[0])
        print("Clicking at: "+str(c.args))
    elif c.fn == commands["mouse_move"].fn:
        c.fn(int(c.args[0]),int(c.args[1]))
        print("Moving mouse at: "+str(c.args))
    elif c.fn == commands["find_and_left_click"].fn or c.fn == commands["find_and_right_click"].fn or c.fn == commands["find_and_middle_click"].fn or c.fn == commands["find_and_left_mouse_down"].fn or c.fn == commands["find_and_right_mouse_down"].fn or c.fn == commands["find_and_middle_mouse_down"].fn or c.fn == commands["find_and_left_mouse_up"].fn or c.fn == commands["find_and_right_mouse_up"].fn or c.fn == commands["find_and_middle_mouse_up"].fn:
        print(c.args)
        print(c.add)
        c.fn(os.path.join(path,c.args[0]),float(c.args[1]),c.add[0])
    elif c.fn == commands["find_and_press"].fn:
        c.fn(os.path.join(path,c.args[0]),float(c.args[1]),c.args[2])
    elif c.fn == commands["wait"].fn:
        print("Waiting...")
        c.fn(float(c.args[0]))
    elif c.fn == commands["windows_mode"].fn:
        c.fn(c.args[0]=="1")
    elif c.fn == commands["wait_for_this"].fn:
        c.fn(os.path.join(path,c.args[0]),float(c.args[1]))
    elif c.fn == commands["check_for"].fn:
        if condition is not None:
            return c.fn(os.path.join(path,c.args[0]),float(c.args[1])) == condition
        else:
            print("check_for needs a conditional symbol (! or =). Exiting...")
            exit()

def commandMux(com_):
    global result
    condition = None
    com = com_[:]
    if com[0].startswith("!"):
        com[0] = com[0][1:]
        condition = False
        result = commandTranslation(com,condition)
    elif com[0].startswith("="):
        com[0] = com[0][1:]
        condition = True
        result = commandTranslation(com,condition)
    elif com[0].startswith("+"):
        com[0] = com[0][1:]
        if result:
            commandTranslation(com)
    elif com[0].startswith("-"):
        com[0] = com[0][1:]
        if not result:
            commandTranslation(com)
    else:
        commandTranslation(com)

if len(sys.argv) >= 2:
    with open(os.path.join(path,sys.argv[1])) as f:
        one_time = []
        loop = []
        looping = False
        for com in f:
            com = com.strip()
            if com.startswith("#"):
                continue
            if com == "---":
                looping = True
                continue
            if looping:
                loop.append(com.split(","))
            else:
                one_time.append(com.split(","))

        for com in one_time:
            commandMux(com)
        del(one_time)
        while True:
            for com in loop:
                commandMux(com)
else:
    print("A config file argument is needed")
