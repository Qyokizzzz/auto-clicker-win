from abc import ABC, abstractmethod
import pyautogui as pg
from src.Utils import sleep

class Button(ABC):
    def __init__(self, button, click_type, duration, x = None, y = None):
        self.button = button
        self.click_type = click_type
        self.duration = duration
        self.x = x
        self.y = y

    @abstractmethod
    def single_click(self):
        pass

    @abstractmethod
    def double_click(self):
        pass

    @abstractmethod
    def press(self):
        pass

    def perform(self):
        action = [
            self.single_click,
            self.double_click,
            self.press
        ]
        return action[self.click_type]()

class MouseButton(Button):
    def __init__(self, button, click_type, duration, x, y):
        super().__init__(button, click_type, duration, x, y)

    def single_click(self):
        pg.click(self.x, self.y, button=self.button)

    def double_click(self):
        pg.doubleClick(self.x, self.y, button=self.button)

    def press(self):
        pg.mouseDown(self.x, self.y, button=self.button)
        sleep(self.duration)
        pg.mouseUp(self.x, self.y, button=self.button)

class KeyboardButton(Button):
    def __init__(self, button, click_type, duration):
        super().__init__(button, click_type, duration)

    def single_click(self):
        pg.press(self.button)

    def double_click(self):
        pg.press(self.button, presses=2, interval=0.1)

    def press(self):
        pg.keyDown(self.button)
        sleep(self.duration)
        pg.keyUp(self.button)
