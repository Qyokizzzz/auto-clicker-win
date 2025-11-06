import keyboard
import threading
import argparse
from src.Button import KeyboardButton, MouseButton
from src.Utils import sleep

class AutoClicker:
    def __init__(self, repeat_key, click_type, interval, duration, hotkey, x = None, y = None, times = None):
        self.interval = interval
        self.hotkey = hotkey
        self.times = times
        self.thread = None
        self.trigger = False
        self.button = KeyboardButton(repeat_key, click_type, duration)
        if repeat_key in ['mouseLeft', 'mouseRight']:
            self.button = MouseButton(repeat_key[5:], click_type, duration, x, y)

    def start(self):
        self.thread = threading.Thread(target=self._loop)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.trigger = False
        if self.thread is not None:
            self.thread.join(timeout=1)
            self.thread = None

    def _loop(self):
        counter = 0
        while self.trigger:
            self.button.perform()
            sleep(self.interval)

            counter += 1
            if self.times and counter >= self.times:
                self.trigger = False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repeat_key', type=str, default='mouseLeft')
    parser.add_argument('--click_type', type=int, default=2)
    parser.add_argument('--interval', type=int, default=1)
    parser.add_argument('--duration', type=int, default=1)
    parser.add_argument('--hotkey', type=str, default='f2')

    parser.add_argument('--x', type=int, default=None)
    parser.add_argument('--y', type=int, default=None)
    parser.add_argument('--times', type=int, default=None)

    args = parser.parse_args()
    print(args)
    clicker = AutoClicker(args.repeat_key, args.click_type, args.interval, args.duration, args.hotkey, args.x, args.y, args.times)

    while 1:
        if keyboard.is_pressed(clicker.hotkey):
            clicker.trigger = not clicker.trigger

            if clicker.trigger:
                clicker.start()
            else:
                clicker.stop()

            sleep(1)
