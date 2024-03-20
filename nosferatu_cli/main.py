import os
import json
import argparse
import logging
from logging.handlers import QueueHandler, QueueListener
logger = None

from multiprocessing import Process, Queue
from contextlib import contextmanager

# from nosferatu_cli.version import VERSION
from nosferatu_cli.listen.listen import init_listener
from nosferatu_cli.think.think import init_processor
from nosferatu_cli.reply.reply import init_sender


from nosferatu_cli.logger import ColoredFormatter, set_color, YELLOW, WHITE, RED


def setup_logging(log_queue):
    debug = os.getenv("DEBUG", False)
    if debug:
        # log_format = f"%(levelname)s | ({set_color(YELLOW)}%(filename)s @ %(lineno)d{set_color(WHITE)}) | %(message)s"
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", help="Specify which bot to use.  Name should be the directory name inside `~/bots/` that holds a valid settings.json file.", required=True)
    exclusive_group = parser.add_mutually_exclusive_group(required=True)
    exclusive_group.add_argument("--fetch", action="store_true", help="Update database with new messages and exit")
    exclusive_group.add_argument("--run", action="store_true", help="Runs fetch in a loop.")

    from nosferatu_cli.version import VERSION # avoids a circular import... but I'm not sure why this doesn't work as well as nospy
    parser.add_argument('--version', action='version', version=f'%(prog)s {VERSION}')

    args = parser.parse_args()



    print(args) # TODO - remove

    # if args.post:
    #     print("Not implemented yet")
    #     exit(0)
    do_the_thing(args.name, args.run)

    # if args.fetch:
    #     # setup_logging(log_queue) # TODO - I need a different logging setup for fetch!!!
    #     # logger.debug(f"Starting Nosferatu with args: {args}")
    #     # logger.warning("Fetching... not implemented yet!!  Quitting.")
    #     print(f"Starting Nosferatu with args: {args}")
    #     print("Fetching... not implemented yet!!  Quitting.")
    #     exit(0)

    # if args.run:
    #     log_queue = Queue()
    #     setup_logging(log_queue) # TODO - I need to watch mCoding youtube again and get real-time notifications for exceptions in production!!!

    #     logger.debug(f"Starting Nosferatu --run with args: {args}")
    #     settings = load_settings(args.name)

    #     queue = Queue()
    #     response_queue = Queue()


    #     listener_process = Process(target=init_listener, args=(settings, queue, log_queue, ))
    #     processor_process = Process(target=init_processor, args=(settings, queue, response_queue, log_queue, ))
    #     sender_process = Process(target=init_sender, args=(settings, response_queue, log_queue, ))

    #     listener_process.start()
    #     processor_process.start()
    #     sender_process.start()

    #     try:
    #         listener_process.join()
    #         processor_process.join()
    #         sender_process.join()

    #     except KeyboardInterrupt:
    #         logger.warning("Terminating...")
    #         listener_process.terminate()
    #         processor_process.terminate()
    #         sender_process.terminate()
    #         listener_process.join()
    #         processor_process.join()
    #         sender_process.join()



def do_the_thing(name, keep_alive):
        log_queue = Queue()
        setup_logging(log_queue) # TODO - I need to watch mCoding youtube again and get real-time notifications for exceptions in production!!!

        # logger.debug(f"Starting Nosferatu --run with args: {args}")
        settings = load_settings(name)

        queue = Queue()
        listener_process = Process(target=init_listener, args=(settings, queue, log_queue, keep_alive, ))
        listener_process.start()

        if keep_alive:
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

