from os import get_terminal_size
from time import sleep
from typing import Any

from noiftimer import Timer


def clear():
    """Erase the current line from the terminal."""
    print(" " * (get_terminal_size().columns - 1), flush=True, end="\r")


def print_in_place(string: str, animate: bool = False, animate_refresh: float = 0.01):
    """Calls to print_in_place will overwrite
    the previous line of text in the terminal
    with the 'string' param.

    :param animate: Will cause the string
    to be printed to the terminal
    one character at a time.

    :param animate_refresh: Number of seconds
    between the addition of characters
    when 'animate' is True."""
    clear()
    string = str(string)
    width = get_terminal_size().columns
    string = string[: width - 2]
    if animate:
        for i in range(len(string)):
            print(f"{string[:i+1]}", flush=True, end=" \r")
            sleep(animate_refresh)
    else:
        print(string, flush=True, end="\r")


def ticker(info: list[str]):
    """Prints info to terminal with
    top and bottom padding so that repeated
    calls print info without showing previous
    outputs from ticker calls.

    Similar visually to print_in_place,
    but for multiple lines."""
    width = get_terminal_size().columns
    info = [str(line)[: width - 1] for line in info]
    height = get_terminal_size().lines - len(info)
    print("\n" * (height * 2), end="")
    print(*info, sep="\n", end="")
    print("\n" * (int((height) / 2)), end="")


class ProgBar:
    """Self incrementing, dynamically sized progress bar.

    Includes a Timer object from noiftimer that starts timing
    on the first call to display and stops timing once
    self.counter >= self.total.
    It can be easily added to the progress bar display by calling
    Timer's checkTime function and passing the value to the 'prefix' or 'suffix'
    param of self.display():

    bar = ProgBar(total=someTotal)
    bar.display(prefix=f"Run time: {bar.timer.checkTime()}")"""

    def __init__(
        self,
        total: float,
        fill_ch: str = "_",
        unfill_ch: str = "/",
        width_ratio: float = 0.75,
        new_line_after_completion: bool = True,
        clear_after_completion: bool = False,
    ):
        """:param total: The number of calls to reach 100% completion.

        :param fill_ch: The character used to represent the completed part of the bar.

        :param unfill_ch: The character used to represent the uncompleted part of the bar.

        :param width_ratio: The width of the progress bar relative to the width of the terminal window.

        :param new_line_after_completion: Make a call to print() once self.counter >= self.total.

        :param clear_after_completion: Make a call to printbuddies.clear() once self.counter >= self.total.

        Note: if new_line_after_completion and clear_after_completion are both True, the line will be cleared
        then a call to print() will be made."""
        self.total = total
        self.fill_ch = fill_ch[0]
        self.unfill_ch = unfill_ch[0]
        self.width_ratio = width_ratio
        self.new_line_after_completion = new_line_after_completion
        self.clear_after_completion = clear_after_completion
        self.timer = Timer()
        self.reset()

    def reset(self):
        self.counter = 0
        self.percent = ""
        self.prefix = ""
        self.suffix = ""
        self.filled = ""
        self.unfilled = ""
        self.bar = ""

    def get_percent(self) -> str:
        """Returns the percentage complete to two decimal places
        as a string without the %."""
        percent = str(round(100.0 * self.counter / self.total, 2))
        if len(percent.split(".")[1]) == 1:
            percent = percent + "0"
        if len(percent.split(".")[0]) == 1:
            percent = "0" + percent
        return percent

    def _prepare_bar(self):
        self.terminal_width = get_terminal_size().columns - 1
        bar_length = int(self.terminal_width * self.width_ratio)
        progress = int(bar_length * self.counter / self.total)
        self.filled = self.fill_ch * progress
        self.unfilled = self.unfill_ch * (bar_length - progress)
        self.percent = self.get_percent()
        self.bar = self.get_bar()

    def _trim_bar(self):
        original_width = self.width_ratio
        while len(self.bar) > self.terminal_width and self.width_ratio > 0:
            self.width_ratio -= 0.01
            self._prepare_bar()
        self.width_ratio = original_width

    def get_bar(self):
        return f"{self.prefix} [{self.filled}{self.unfilled}]-{self.percent}% {self.suffix}"

    def display(
        self,
        prefix: str = "",
        suffix: str = "",
        counter_override: float = None,
        total_override: float = None,
        return_object: Any = None,
    ) -> Any:
        """Writes the progress bar to the terminal.

        :param prefix: String affixed to the front of the progress bar.

        :param suffix: String appended to the end of the progress bar.

        :param counter_override: When an externally incremented completion counter is needed.

        :param total_override: When an externally controlled bar total is needed.

        :param return_object: An object to be returned by display().

        Allows display() to be called within a comprehension:

        e.g.

        bar = ProgBar(9)

        myList = [bar.display(return_object=i) for i in range(10)]"""
        if not self.timer.started:
            self.timer.start()
        if counter_override is not None:
            self.counter = counter_override
        if total_override:
            self.total = total_override
        # Don't wanna divide by 0 there, pal
        while self.total <= 0:
            self.total += 1
        self.prefix = prefix
        self.suffix = suffix
        self._prepare_bar()
        self._trim_bar()
        pad = " " * (self.terminal_width - len(self.bar))
        width = get_terminal_size().columns
        print(f"{self.bar}{pad}"[: width - 2], flush=True, end="\r")
        if self.counter >= self.total:
            self.timer.stop()
            if self.clear_after_completion:
                clear()
            if self.new_line_after_completion:
                print()
        self.counter += 1
        return return_object
