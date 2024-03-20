# import os
# import logging


# # http://jafrog.com/2013/11/23/colors-in-terminal.html
# # https://github.com/fidian/ansi
# # https://gist.github.com/JBlond/2fea43a3049b38287e5e9cefc87b2124
# # https://docs.python.org/3/library/logging.html#formatter-objects


# logger = None

# # Define the color codes
# BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# def set_color(color):
#     return f'\033[0;3{color}m'

# # Custom log level colors
# LOG_COLORS = {
#     logging.DEBUG: set_color(BLUE),
#     logging.INFO: set_color(GREEN),
#     logging.WARNING: set_color(YELLOW),
#     logging.ERROR: set_color(RED),
#     logging.CRITICAL: set_color(MAGENTA),
# }

# class ColoredFormatter(logging.Formatter):
#     def format(self, record):
#         level_color = LOG_COLORS[record.levelno]
#         record.levelname = f"{level_color}{record.levelname}\033[0m"
#         return super().format(record)


# def setup_logging(log_queue):
#     from nosferatu_cli.logger import ColoredFormatter, set_color, YELLOW, WHITE, RED
#     # import logging
#     from logging.handlers import QueueHandler, QueueListener

#     debug = os.getenv("DEBUG", False)
#     if debug:
#         log_format = f"%(levelname)s | {set_color(YELLOW)}%(name)s:{set_color(RED)}%(funcName)s{set_color(WHITE)} | %(message)s"
#     else:
#         log_format = "%(levelname)s | %(message)s"

#     global logger
#     logger = logging.getLogger("nosferatu")
#     logger.setLevel(logging.DEBUG) # TODO

#     # These logs will be shown in the console
#     console_handler = logging.StreamHandler()
#     formatter = ColoredFormatter(log_format, datefmt="%Y/%m/%d %H:%M.%S")
#     console_handler.setFormatter(formatter)
#     logger.addHandler(console_handler)

#     # Then create a queue listener with a default console handler and start it
#     queue_listener = QueueListener(log_queue, console_handler)
#     queue_listener.start()
