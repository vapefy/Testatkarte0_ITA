from gpiozero import LED, Button
import time
import sqlite3
import datetime

class Entry:

    def __init__(self, timestamp: datetime.datetime, led_state: bool) -> None:
        self.timestamp = timestamp
        self.led_state = led_state

class ORM:

    def __init__(self, filename) -> None:
        self.filename = filename
        self.conn = sqlite3.connect(self.filename, check_same_thread=False)
        self.c = self.conn.cursor()

        self.init_database()

    def save_entry(self, entry: Entry):
        self.c.execute("INSERT INTO taster (time_stamp, led_status) VALUES ('" + entry.timestamp.strftime("%d-%m-%Y %H:%M:%S") + "',  " + str(entry.led_state) + ");")
        self.conn.commit()

    def init_database(self):

        sql_code = "" 

        with open("./setup.sql", "r+") as file:
            lines = file.readlines()
        
        for line in lines:
            sql_code = sql_code + line

        self.c.execute(sql_code)
        self.conn.commit()




class Diode:

    def __init__(self) -> None:
        self.led = LED(11)
        self.running = False


    def switch(self, on: bool):
        if(on):
            self.led.on()
            self.running = True
        else:
            self.led.off()
            self.running = False


class Main:

    def __init__(self) -> None:
        self.button = Button(8, pull_up=False)
        self.diode = Diode()
        self.orm = ORM("taster.db")

        self.button.when_released = self.button_pressed

    def button_pressed(self):
        if(self.diode.running):
            self.diode.switch(False)

            entry = Entry(datetime.datetime.now(), False)
            self.orm.save_entry(entry)
            print("saved", str(entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')), entry.led_state)
        else:
            self.diode.switch(True)

            entry = Entry(datetime.datetime.now(), True)
            self.orm.save_entry(entry)
            print("saved", str(entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')), entry.led_state)



Main()
input()