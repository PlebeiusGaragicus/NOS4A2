import os
import json
import logging
logger = None

# http://jafrog.com/2013/11/23/colors-in-terminal.html
# https://github.com/fidian/ansi
# https://gist.github.com/JBlond/2fea43a3049b38287e5e9cefc87b2124
# https://docs.python.org/3/library/logging.html#formatter-objects


# Define the color codes
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

def set_color(color):
    return f'\033[0;3{color}m'

# Custom log level colors
LOG_COLORS = {
    logging.DEBUG: set_color(BLUE),
    logging.INFO: set_color(GREEN),
    logging.WARNING: set_color(YELLOW),
    logging.ERROR: set_color(RED),
    logging.CRITICAL: set_color(MAGENTA),
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        level_color = LOG_COLORS[record.levelno]
        record.levelname = f"{level_color}{record.levelname}\033[0m"
        return super().format(record)


def setup_logging(log_queue):
    # from nosferatu_cli.logger import ColoredFormatter, set_color, YELLOW, WHITE, RED
    from logging.handlers import QueueHandler, QueueListener

    debug = os.getenv("DEBUG", False)
    if debug:
        log_format = f"%(levelname)s | {set_color(YELLOW)}%(name)s:{set_color(RED)}%(funcName)s{set_color(WHITE)} | %(message)s"
    else:
        log_format = "%(levelname)s | %(message)s"

    global logger
    logger = logging.getLogger("nosferatu")
    logger.setLevel(logging.DEBUG) # TODO

    # These logs will be shown in the console
    console_handler = logging.StreamHandler()
    formatter = ColoredFormatter(log_format, datefmt="%Y/%m/%d %H:%M.%S")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Then create a queue listener with a default console handler and start it
    queue_listener = QueueListener(log_queue, console_handler)
    queue_listener.start()



def load_settings(name):
    bot_dir = os.path.join(os.path.expanduser("~"), "bots")

    settings_file = os.path.join(bot_dir, name, "settings.json")
    if os.path.exists(settings_file):
        try:
            with open(settings_file, "r") as f:
                settings = json.load(f)
                logger.debug(f"Loaded settings.json for {name}")
                return settings
        except json.JSONDecodeError:
            logger.error(f"settings.json not valid for {name}")
    else:
        logger.warning(f"settings.json not found for {name}")
        exit(1)




def main():
    from dotenv import load_dotenv
    load_dotenv()

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", help="Specify which bot to use.  Name should be the directory name inside `~/bots/` that holds a valid settings.json file.", required=True)
    exclusive_group = parser.add_mutually_exclusive_group(required=True)
    exclusive_group.add_argument("--fetch", action="store_true", help="Update database with new messages and exit")
    exclusive_group.add_argument("--run", action="store_true", help="Runs fetch in a loop.")

    from nosferatu_cli.version import VERSION # avoids a circular import... but I'm not sure why this doesn't work as well as nospy
    parser.add_argument('--version', action='version', version=f'%(prog)s {VERSION}')
    args = parser.parse_args()
    # Namespace(name='nosfatty', fetch=True, run=False)

    do_the_thing(args.name, args.run, args.name) # NOTE: the directory of the bot files is the mongodb collection name of the bot's messages, etc



def do_the_thing(name, keep_alive, collection_name):
    from multiprocessing import Process, Queue
    from nosferatu_cli.listen.listen import init_listener

    log_queue = Queue()
    # from nosferatu_cli.logger import setup_logging
    setup_logging(log_queue) # TODO - I need to watch mCoding youtube again and get real-time notifications for exceptions in production!!!

    settings = load_settings(name)

    queue = Queue()
    listener_process = Process(target=init_listener, args=(settings, queue, log_queue, keep_alive, collection_name))
    listener_process.start()

    if keep_alive:
        from nosferatu_cli.think.think import init_processor
        from nosferatu_cli.reply.reply import init_sender

        response_queue = Queue()
        processor_process = Process(target=init_processor, args=(settings, queue, response_queue, log_queue, ))
        sender_process = Process(target=init_sender, args=(settings, response_queue, log_queue, ))

        processor_process.start()
        sender_process.start()

    try:
        listener_process.join()

        if keep_alive:
            processor_process.join()
            sender_process.join()

    except KeyboardInterrupt:
        logger.warning("Terminating...")
        listener_process.terminate()

        if keep_alive:
            processor_process.terminate()
            sender_process.terminate()

        listener_process.join()

        if keep_alive:
            processor_process.join()
            sender_process.join()
