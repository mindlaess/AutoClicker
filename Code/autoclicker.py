# Author: Synctic
# License: MIT | Copyright (c) 2022 Synctic
# Version: 1.05

from PIL import Image, ImageTk
from pynput.keyboard import *
from pynput.keyboard import Key, Listener
from pynput import keyboard
from time import sleep
import tkinter as tk
import sys
import os
import pydirectinput
import customtkinter
import threading
import spinbox as spinbox

autoclick_key = Key.f5
holdm_key = Key.f6

button1 = "Left"
clicktype = "Single"
repeattype = 1


class App(customtkinter.CTk):

    WIDTH = 315
    HEIGHT = 452

    auto1 = False
    auto = False

    global resource

    def resource(relative_path):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(
            os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")

    def start(self):
        self.mainloop()

    def setupAutoclicker(self):
        title = customtkinter.CTkLabel(master=self.tab1, text="AutoClicker", font=("Roboto Medium", -16))
        title.pack(pady=5)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.start_auto_button = customtkinter.CTkButton(
            master=self.tab1,
            text="Start",
            fg_color=("black"),
            font=("Roboto Medium", -16),
            command=self.start_button,
        )
        self.start_auto_button.pack(pady=(200,0))

        self.stop_auto_button = customtkinter.CTkButton(
            master=self.tab1,
            text="Stop",
            fg_color=("black"),
            font=("Roboto Medium", -16),
            state="disabled",
            command=self.stop_button,
        )
        self.stop_auto_button.pack(pady=(10,10))

        self.buttonmenu_var = customtkinter.StringVar(value="Left")

        self.buttonmenu = customtkinter.CTkComboBox(
            master=self.tab1,
            font=("Roboto Medium", -14),
            width=115,
            fg_color="black",
            button_color="black",
            variable=self.buttonmenu_var,
            command=self.buttonmenu_event,
            values=["Left", "Middle", "Right"],
        )
        self.buttonmenu.place(x=20, y=70)

        self.buttonmenu.bind("<Return>", lambda e: self.custombutton())

        self.buttontxt = customtkinter.CTkLabel(
            master=self.tab1, text="Button:", font=("Roboto Medium", -15)
        )
        self.buttontxt.place(x=46, y=40)

        self.clicktype_var = customtkinter.StringVar(value="Single")

        self.clicktypemenu = customtkinter.CTkOptionMenu(
            master=self.tab1,
            font=("Roboto Medium", -14),
            width=115,
            fg_color="black",
            button_color="black",
            variable=self.clicktype_var,
            command=self.clicktype_event,
            values=["Single", "Double", "Triple", "Hold"],
        )
        self.clicktypemenu.place(x=160, y=70)

        self.clicktypetxt = customtkinter.CTkLabel(
            master=self.tab1, text="Click Type:", font=("Roboto Medium", -15)
        )
        self.clicktypetxt.place(x=180, y=40)

        self.clickinterval_var = customtkinter.StringVar(
            master=self.tab1, value=str(0.01)
        )

        self.clickintervaltxt = customtkinter.CTkLabel(
            master=self.tab1, text="Click interval", font=("Roboto Medium", -14)
        )
        self.clickintervaltxt.pack(pady=(10,0))

        self.clickinterval = customtkinter.CTkEntry(
            master=self.tab1,
            font=("Roboto Medium", -14),
            width=80,
            textvariable=self.clickinterval_var,
        )
        self.clickinterval.pack(pady=(5,0))

        self.secondstxt = customtkinter.CTkLabel(
            master=self.tab1, text="secs", font=("Roboto Medium", -13), width=10
        )
        self.secondstxt.place(x=195, y=385)

        self.repeat_var = customtkinter.IntVar()
        self.repeat_var.set(value=1)

        self.repeat = customtkinter.CTkRadioButton(
            master=self.tab1,
            text="Repeat",
            value=0,
            variable=self.repeat_var,
            command=self.repeat_event,
            font=("Roboto Medium", -13),
            width=20,
            height=20,
        )
        self.repeat.place(x=20, y=140)

        self.repeatstopped = customtkinter.CTkRadioButton(
            master=self.tab1,
            text="Repeat until stopped",
            value=1,
            variable=self.repeat_var,
            command=self.repeat_event,
            font=("Roboto Medium", -13),
            width=20,
            height=20,
        )
        self.repeatstopped.place(x=20, y=170)

        self.repeattimes = spinbox.FloatSpinbox(
            master=self.tab1, width=105, height=25, step_size=1
        )
        self.repeattimes.place(x=160, y=135)

        self.lis2 = keyboard.Listener(on_press=self.on_press1)
        self.lis2.start()

        self.repeattimes.set(1)
        self.repeatstopped.select()

    def setupMoveit(self):
        self.sliderVar = customtkinter.IntVar(master=self.tab2, value=50)
        self.slider = customtkinter.CTkSlider(master=self.tab2, from_=0, to=100, variable=self.sliderVar)
        self.slider.pack(pady=(10,0))
        customtkinter.CTkLabel(master=self.tab2, textvariable=self.sliderVar).pack()

        self.start_move = customtkinter.CTkButton(
            master=self.tab2,
            text="Start",
            fg_color=("black"),
            font=("Roboto Medium", -16),
            command=self.start_move_fn,
        )
        self.start_move.pack(pady=(150,0))

        self.stop_move = customtkinter.CTkButton(
            master=self.tab2,
            text="Stop",
            fg_color=("black"),
            font=("Roboto Medium", -16),
            state="disabled",
            command=self.stop_move_fn,
        )
        self.stop_move.pack(pady=(10,10))

        # self.lismove = keyboard.Listener(on_press=self.on_press1)
        # self.lismove.start()

    def start_move_fn(self):

        return

    def stop_move_fn(self):
        return

    def __init__(self):
        super().__init__()

        self.title("AutoClicker")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        self.p1 = ImageTk.PhotoImage(file=resource("../Assets/icon.ico"))
        self.wm_iconbitmap()
        self.iconphoto(False, self.p1)

        self.tabview = customtkinter.CTkTabview(master=self)
        self.tab1 = self.tabview.add("AutoClicker")
        self.tab2 = self.tabview.add("MoveIt")
        self.tabview.pack(pady=10)

        #
        #   Setting AutoClicker Tab
        #

        self.setupAutoclicker()

        #
        #   Setting MoveIt Tab
        #

        self.setupMoveit()

    def buttonmenu_event(self, choice5):
        global button1
        self.choice5 = choice5

        if self.choice5 == "Left":
            button1 = "Left"
        elif self.choice5 == "Middle":
            button1 = "Middle"
        elif self.choice5 == "Right":
            button1 = "Right"

    def custombutton(self):
        global button1
        button1 = self.buttonmenu_var.get()
        self.frame.focus_set()

    def clicktype_event(self, choice):
        global clicktype

        if choice == "Single":
            clicktype = "Single"
        elif choice == "Double":
            clicktype = "Double"
        elif choice == "Triple":
            clicktype = "Triple"
        elif choice == "Hold":
            clicktype = "Hold"

    def repeat_event(self):
        global repeattype

        if self.repeat_var.get() == 0:
            repeattype = 0
        if self.repeat_var.get() == 1:
            repeattype = 1

    def start_button(self):
        if self.tabview.get() == "AutoClicker":
            if (
                clicktype == "Single"
                or clicktype == "Double"
                or clicktype == "Triple"
                and not self.pause
            ):
                self.lis2.stop()
                self.pause = False

                self.autoclc = threading.Thread(target=self.autoClick)
                self.autoclc.start()

                self.buttonmenu.configure(state="normal")
                self.buttonmenu.configure(state="disabled")
                self.start_auto_button.configure(state="disabled")
                self.stop_auto_button.configure(state="enabled")
            else:
                if not self.pause:
                    self.lis2.stop()
                    self.pause = False

                    self.autohol = threading.Thread(target=self.autoHold)
                    self.autohol.start()

                    self.buttonmenu.configure(state="normal")
                    self.buttonmenu.configure(state="disabled")
                    self.start_auto_button.configure(state="disabled")
                    self.stop_auto_button.configure(state="enabled")
        elif self.tabview.get() == "MoveIt":
            if not self.pause:
                self.autoMove = threading.Thread(target=self.autoMove_fn)
                self.autoMove.start()

                self.slider.configure(state="disabled")
                self.start_move.configure(state="disabled")
                self.stop_move.configure(state="enabled")

    def on_press1(self, key):
        if self.tabview.get() == "AutoClicker":
            if not self.auto1 and key == autoclick_key:
                self.pause = False
                self.auto1 = True
                self.auto = False
                self.lis2.stop()
                self.start_button()

            if not self.auto and key == holdm_key:
                self.pause = False
                self.lis2.stop()
                self.start_button()
                self.auto1 = True
        elif self.tabview.get() == "MoveIt":
            if key == autoclick_key:
                self.pause = False
                self.lis2.stop()
                self.start_button()

    def on_press(self, key):
        if self.tabview.get() == "AutoClicker":
            if self.auto1 and key == autoclick_key:
                self.pause = True
                self.auto1 = False
                self.stop_button()
                self.lis2 = keyboard.Listener(on_press=self.on_press1)
                self.lis2.start()

            if self.auto and key == holdm_key:
                self.pause = True
                self.auto = False
                self.stop_button()
                self.lis2 = keyboard.Listener(on_press=self.on_press1)
                self.lis2.start()
        elif self.tabview.get() == "MoveIt":
            if key == autoclick_key:
                self.pause = True
                self.stop_button()
                self.lis2 = keyboard.Listener(on_press=self.on_press1)
                self.lis2.start()

    def autoHold(self):
        self.auto = True
        self.auto1 = False
        self.pause = False

        lis = Listener(on_press=self.on_press)
        lis.start()

        while self.auto:
            if not self.pause:
                if button1 == "Left":
                    pydirectinput.mouseDown(button="left")
                elif button1 == "Middle":
                    pydirectinput.mouseDown(button="middle")
                elif button1 == "Right":
                    pydirectinput.mouseDown(button="right")
                else:
                    pydirectinput.keyDown(keys=self.buttonmenu.get().lower())
                    pydirectinput.PAUSE = self.interval

            if self.pause:
                self.autohol.join()
                break
        lis.stop()

    def autoClick(self):
        self.auto = False
        self.auto1 = True
        self.pause = False

        lis1 = Listener(on_press=self.on_press)
        lis1.start()

        self.interval = float(self.clickinterval.get())
        if repeattype == 1:
            while self.auto1:
                if not self.pause:
                    if clicktype == "Single":
                        if self.buttonmenu.get() == "Left":
                            pydirectinput.click(button="left")
                            pydirectinput.PAUSE = self.interval
                        elif self.buttonmenu.get() == "Middle":
                            pydirectinput.click(button="middle")
                            pydirectinput.PAUSE = self.interval
                        elif self.buttonmenu.get() == "Right":
                            pydirectinput.click(button="right")
                            pydirectinput.PAUSE = self.interval
                        else:
                            pydirectinput.press(
                                keys=self.buttonmenu.get().lower())
                            pydirectinput.PAUSE = self.interval

                    if clicktype == "Double":
                        if button1 == "Left":
                            pydirectinput.doubleClick(button="left")
                            pydirectinput.PAUSE = self.interval
                        elif button1 == "Middle":
                            pydirectinput.doubleClick(button="middle")
                            pydirectinput.PAUSE = self.interval
                        elif button1 == "Right":
                            pydirectinput.doubleClick(button="right")
                            pydirectinput.PAUSE = self.interval
                        else:
                            pydirectinput.press(
                                keys=self.buttonmenu.get().lower())
                            pydirectinput.PAUSE = self.interval

                    if clicktype == "Triple":
                        if button1 == "Left":
                            pydirectinput.tripleClick(button="left")
                            pydirectinput.PAUSE = self.interval
                        elif button1 == "Middle":
                            pydirectinput.tripleClick(button="middle")
                            pydirectinput.PAUSE = self.interval
                        elif button1 == "Right":
                            pydirectinput.tripleClick(button="right")
                            pydirectinput.PAUSE = self.interval
                        else:
                            pydirectinput.press(
                                keys=self.buttonmenu.get().lower())
                            pydirectinput.PAUSE = self.interval
                if self.pause:
                    break
        else:
            for i in range(int(self.repeattimes.get()) + 1):
                if not self.pause:
                    if clicktype == "Single":
                        if self.buttonmenu.get() == "Left":
                            pydirectinput.click(button="left")
                            pydirectinput.PAUSE = self.interval
                        elif self.buttonmenu.get() == "Middle":
                            pydirectinput.click(button="middle")
                            pydirectinput.PAUSE = self.interval
                        elif self.buttonmenu.get() == "Right":
                            pydirectinput.click(button="right")
                            pydirectinput.PAUSE = self.interval
                        else:
                            pydirectinput.press(keys=self.buttonmenu.get())
                            pydirectinput.PAUSE = self.interval

                    if clicktype == "Double":
                        if button1 == "Left":
                            pydirectinput.doubleClick(button="left")
                            pydirectinput.PAUSE = self.interval
                        elif button1 == "Middle":
                            pydirectinput.doubleClick(button="middle")
                            pydirectinput.PAUSE = self.interval
                        elif button1 == "Right":
                            pydirectinput.doubleClick(button="right")
                            pydirectinput.PAUSE = self.interval
                        else:
                            pydirectinput.press(
                                keys=self.buttonmenu.get().lower())
                            pydirectinput.PAUSE = self.interval

                    if clicktype == "Triple":
                        if button1 == "Left":
                            pydirectinput.tripleClick(button="left")
                            pydirectinput.PAUSE = self.interval
                        elif button1 == "Middle":
                            pydirectinput.tripleClick(button="middle")
                            pydirectinput.PAUSE = self.interval
                        elif button1 == "Right":
                            pydirectinput.tripleClick(button="right")
                            pydirectinput.PAUSE = self.interval
                        else:
                            pydirectinput.press(
                                keys=self.buttonmenu.get().lower())
                            pydirectinput.PAUSE = self.interval

                    if i == int(self.repeattimes.get()):
                        self.pause = True

                if self.pause:
                    self.auto1 = False
                    self.stop_button()
                    self.autoclc.join()
                    break
                lis1.stop()

    def autoMove_fnR(self, steps, step_x, step_y):
        current_x, current_y = pydirectinput.position()
        for _ in range(steps):
            if not self.pause:
                current_x += step_x
                current_y += step_y
                pydirectinput.moveTo(int(current_x), int(current_y))
                sleep(0.1)
            else:
                return

    def autoMove_fn(self):
        i = 0
        self.lis1 = Listener(on_press=self.on_press)
        self.lis1.start()

        while not self.pause:
            i = (i+1)%2
            if not self.pause:
                moveby = self.sliderVar.get()
                current_x, current_y = pydirectinput.position()
                target_x, target_y = current_x + ((-1)**i)*moveby, current_y + ((-1)**i)*moveby
                pydirectinput.moveTo(int(target_x), int(target_y))
            else:
                break
        if self.pause:
            self.stop_button()
            self.lis1.stop()
        return
        
    def stop_button(self):
        self.pause = True
        if self.tabview.get() == "AutoClicker":
            if clicktype == "Single":
                if button1 == "Left":
                    self.auto1 = False
                    pydirectinput.mouseUp(button="left")
                elif button1 == "Middle":
                    self.auto1 = False
                    pydirectinput.mouseUp(button="middle")
                elif button1 == "Right":
                    self.auto1 = False
                    pydirectinput.mouseUp(button="right")

            if clicktype == "Double":
                if button1 == "Left":
                    self.auto1 = False
                    pydirectinput.mouseUp(button="left")
                elif button1 == "Middle":
                    self.auto1 = False
                    pydirectinput.mouseUp(button="middle")
                elif button1 == "Right":
                    self.auto1 = False
                    pydirectinput.mouseUp(button="right")

            if clicktype == "Triple":
                if button1 == "Left":
                    self.auto1 = False
                    pydirectinput.mouseUp(button="left")
                elif button1 == "Middle":
                    self.auto1 = False
                    pydirectinput.mouseUp(button="middle")
                elif button1 == "Right":
                    self.auto1 = False
                    pydirectinput.mouseUp(button="right")

            if clicktype == "Hold":
                if button1 == "Left":
                    self.auto = False
                    pydirectinput.mouseUp(button="left")
                elif button1 == "Middle":
                    self.auto = False
                    pydirectinput.mouseUp(button="middle")
                elif button1 == "Right":
                    self.auto = False
                    pydirectinput.mouseUp(button="right")
                else:
                    pydirectinput.keyUp(button=self.buttonmenu.get().lower())

            self.buttonmenu.configure(state="normal")
            self.start_auto_button.configure(state="enabled")
            self.stop_auto_button.configure(state="disabled")

        elif self.tabview.get() == "MoveIt":
            self.slider.configure(state="normal")
            self.start_move.configure(state="normal")
            self.stop_move.configure(state="disabled")

    def on_close(self, event=0):
        self.destroy()



if __name__ == "__main__":
    app = App()
    app.attributes("-topmost", True)
    app.resizable(False, False)
    app.update()
    app.start()
