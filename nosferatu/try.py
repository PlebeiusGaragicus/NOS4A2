# from enum import Enum

# class Color(Enum):
#     BLACK = 0
#     RED = 1
#     GREEN = 2
#     YELLOW = 3
#     BLUE = 4
#     MAGENTA = 5
#     CYAN = 6
#     WHITE = 7
#     RESET = 9

# def colored(text, fg=Color.RESET, bg=Color.RESET, bold=False, underline=False):
#     style = ';'.join([
#         '1' if bold else '0',
#         '4' if underline else '0',
#         str(30 + fg.value),
#         str(40 + bg.value)
#     ])
#     return f'\x1b[{style}m{text}\x1b[0m'


# print(colored('(venv) satoshi@Jupiter NOS4A2 %', fg=Color.RED, bg=Color.BLACK, bold=True, underline=False))
# # print(colored('Hello, World!', fg=Color.GREEN, bg=Color.BLUE, bold=False, underline=False))



from enum import Enum

class Style(Enum):
    RESET   = 0
    BOLD    = 1
    UNDERLINE = 4

class Color(Enum):
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7
    RESET = 9

def colored(text, fg=None, bg=None, style=None):
    escape_seq = "\033["
    codes = []
    if style:
        codes.append(str(Style[style].value))
    if fg:
        codes.append(str(30 + Color[fg].value))
    if bg:
        codes.append(str(40 + Color[bg].value))
    escape_seq += ';'.join(codes) + 'm' + text + "\033[0m"
    return escape_seq

# print(colored('Hello, World!', fg='RED', bg='YELLOW', style='BOLD'))
# print(colored('Hello, World!', fg='RED', style='BOLD'))
# print(colored('Hello, World!', fg='RED', style='RESET'))
print(colored('Hello, World!', fg='RED', style='UNDERLINE'))


print(colored('(venv) satoshi@Jupiter NOS4A2 %', fg='RED', bg='BLACK', style='BOLD'))
