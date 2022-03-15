import re


class Macros:
    __inputbox = {
        'regex': re.compile(
            r"(?:&lt;{)(?:\[(.*?)\])(?:\[input\])(?:}&gt;)")
    }
    __textbox = {
        'regex': re.compile(
            r"(?:&lt;{)(?:\[(.*?)\])(?:\[text\])(?:}&gt;)")
    }
    __checkbox = {
        'regex': re.compile(
            r"(?:&lt;{)(?:\[(.*?)\])(?:\[checkbox\])(?:\[(.*?)\])(?:}&gt;)"),
        'options': '|'
    }
    __radio = {
        'regex': re.compile(
            r"(?:&lt;{)(?:\[(.*?)\])(?:\[radio\])(?:\[(.*?)\])(?:}&gt;)"),
        'options': '|'
    }
