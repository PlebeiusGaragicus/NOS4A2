import os
import json
import atexit
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


# TODO mCoding logging
# https://github.com/mCodingLLC/VideosSampleCode/blob/master/videos/135_modern_logging/main.py
# https://www.youtube.com/watch?v=X7vBbelRXn0
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
    queue_listener.start() # TODO - don't I have to stop this at some point?  I think I do...
    return queue_listener
    # atexit.register(queue_listener.stop)



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
            logger.critical(f"settings.json not valid for {name}")
            return None
    else:
        logger.warning(f"settings.json not found for {name}")
        exit(1)



USAGE = """

nosferatu_cli [-h] [--version] --bot_dir_name=plebbybot (--fetch-only | --reply-only | --fetch-reply | --daemon)

--fetch
    Fetch new messages from relays and save to database.

--reply
    Reply to any messages recieved or stored in database not yet replied to.

--keep-alive
    Run in a loop.

---



--fetch
--reply
--fetch-reply
--daemon

"""



def main():
    from dotenv import load_dotenv
    load_dotenv()

    import argparse
    parser = argparse.ArgumentParser()

    from nosferatu_cli.version import VERSION # avoids a circular import... but I'm not sure why this doesn't work as well as nospy
    parser.add_argument('--version', action='version', version=f'%(prog)s {VERSION}')
    parser.add_argument("--bot_dir_name", help="Name of directory inside `~/bots/` that contains the bot's settings.json file.", required=True)
    exclusive_group = parser.add_mutually_exclusive_group(required=True)
    exclusive_group.add_argument("--fetch", action="store_true", help="Fetch new messages from relays and save to database, then exit.")
    exclusive_group.add_argument("--reply", action="store_true", help="Reply to messages stored in database not yet replied to.")
    exclusive_group.add_argument("--daemon", action="store_true", help="Run in a loop, fetching and replying to messages.")
    args = parser.parse_args()
    print("args:", args) # Namespace(bot_dir_name='nosfatty', fetch=True, reply=False, daemon=False)
    # exit(0)


    from multiprocessing import Process, Queue
    log_queue = Queue()
    # TODO - I need to watch mCoding youtube again and get real-time notifications for exceptions in production!!!
    queue_listener = setup_logging(log_queue)

    settings = load_settings(args.bot_dir_name)
    if settings is None:
        logger.critical(f"settings.json not found for bot `{args.bot_dir_name}`")
        exit(1)


    if args.daemon:
        msg_queue = Queue()
        reply_queue = Queue()
    else:
        msg_queue = None
        reply_queue = None


    if args.fetch or args.daemon:
        from nosferatu_cli.listen.listen import init_listener
        listener_process = Process(target=init_listener, args=(settings, log_queue, msg_queue, reply_queue, args.daemon))
        listener_process.daemon = True
        listener_process.start()

    if args.reply or args.daemon:
        logger.error("Not yet implemented!")
        exit()
        from nosferatu_cli.think.think import init_processor
        processor_process = Process(target=init_processor, args=(settings, log_queue, msg_queue, reply_queue, args.daemon))
        processor_process.daemon = True
        processor_process.start()


    try:
        if args.fetch or args.daemon:
            listener_process.join()

        if args.reply or args.daemon:
            processor_process.join()

    except KeyboardInterrupt:

        # Stop child processes
        if args.fetch or args.daemon:
            listener_process.terminate()
        
        if args.reply or args.daemon:
            processor_process.terminate()

        # then wait for the processes to completely close
        if args.fetch or args.daemon:
            listener_process.join()

        if args.reply or args.daemon:
            processor_process.join()

    queue_listener.stop()















    # try:
    # except KeyboardInterrupt:
    #     logger.warning("Terminating...")
    #     listener_process.terminate()

    #     if keep_alive:
    #         processor_process.terminate()
    #         # sender_process.terminate()

    #     listener_process.join()

    #     if keep_alive:
    #         processor_process.join()
    #         # sender_process.join()

