import os
import json
import time
import logging
from logging.handlers import QueueHandler, QueueListener

from multiprocessing import Process, Queue, current_process
from contextlib import contextmanager


logger = None

# from nosferatu.listen.listen import init_listener
# from nosferatu.think.think import init_processor
# from nosferatu.reply.reply import init_sender



def load_bot_settings():
    bot_dir = os.path.join(os.path.expanduser("~"), "bots")
    bot_folders = [d for d in os.listdir(bot_dir) if os.path.isdir(os.path.join(bot_dir, d)) ]

    all_bot_settings = {}
    for bot in bot_folders:
        if bot == "DISABLED_BOTS":
            continue

        settings_file = os.path.join(bot_dir, bot, "settings.json")

        if os.path.exists(settings_file):
            try:
                with open(settings_file, "r") as f:
                    settings = json.load(f)
                    all_bot_settings[bot] = settings
                    logger.debug(f"Loaded settings.json for {bot}")
            except json.JSONDecodeError:
                logger.error(f"settings.json not valid for {bot}")
        else:
            logger.warning(f"settings.json not found for {bot}")
    
    return all_bot_settings


def worker_health_check(bot_processes_dict, bot, que_set, log_queue):
    # Get processes
    listener_process = bot_processes_dict[bot][0]
    processor_process = bot_processes_dict[bot][1]
    sender_process = bot_processes_dict[bot][2]

    # check if alive
    if not (listener_process.is_alive() and processor_process.is_alive() and sender_process.is_alive()):
        # if any have crashed, terminate all and restart
        listener_process.terminate()
        processor_process.terminate()
        sender_process.terminate()

        # restart
        bot_processes_dict[bot] = [
            managed_process(init_listener, bot, que_set['queue'], log_queue),
            managed_process(init_processor, bot, que_set['queue'], que_set['response_queue'], log_queue),
            managed_process(init_sender, bot, que_set['response_queue'], log_queue)
        ]

@contextmanager
def managed_process(target, *args, **kwargs):
    process = Process(target=target, args=args, kwargs=kwargs)
    process.start()
    try:
        yield process
    finally:
        process.terminate()
        process.join()



def main():
    # Create a logging queue and a main logger
    log_queue = Queue()
    main_logger = logging.getLogger()
    main_logger.setLevel(logging.DEBUG)
    global logger
    logger = main_logger

    # These logs will be shown in the console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('[%(levelname)s/%(processName)s] %(message)s'))
    main_logger.addHandler(console_handler)


    # Then create a queue listener with a default console handler and start it
    queue_listener = QueueListener(log_queue, console_handler)
    queue_listener.start()

    all_bot_settings = load_bot_settings()
    que_set = [{'queue': Queue(), 'response_queue': Queue()} for _ in all_bot_settings]


    bot_processes_dict = {}
    for bot, que in zip(all_bot_settings, que_set):
        main_logger.debug(f"Loaded settings for {bot}")

        bot_processes_dict[bot] = [
            managed_process(init_listener, bot, que['queue'], log_queue),
            managed_process(init_processor, bot, que['queue'], que['response_queue'], log_queue),
            managed_process(init_sender, bot, que['response_queue'], log_queue)
        ]

    try: 
        # Simplified health check running every 5 seconds
        while True:
            for bot, que in zip(all_bot_settings, que_set):
                worker_health_check(bot_processes_dict, bot, que, log_queue)
                
            time.sleep(5)  # Sleep for 5 seconds

    except KeyboardInterrupt:
        logger.warning("Terminating...")
    finally:
        queue_listener.stop()




    # try:
    #     for bot, que in zip(all_bot_settings, que_set):
    #         logger.debug(f"Loaded settings for {bot}")

    #         with managed_process(init_listener, bot, que['queue'], log_queue) as listener_process, \
    #                 managed_process(init_processor, bot, que['queue'], que['response_queue'], log_queue) as processor_process, \
    #                 managed_process(init_sender, bot, que['response_queue'], log_queue) as sender_process:
    #             listener_process.join()
    #             processor_process.join()
    #             sender_process.join()

    # except KeyboardInterrupt:
    #     main_logger.warning("Terminating...")

    # finally:
    #     queue_listener.stop()







def init_listener(bot, queue, log_queue):
    # Replace logger with QueueHandler to send logs to main process instead
    queue_handler = QueueHandler(log_queue)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(queue_handler)

    logger.info(f"Listener started for {bot}")
    # listener code here

def init_processor(bot, queue, response_queue, log_queue):
    # Replace logger with QueueHandler to send logs to main process instead
    queue_handler = QueueHandler(log_queue)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(queue_handler)

    logger.info(f"Processor started for {bot}")
    # processor code here

def init_sender(bot, response_queue, log_queue):
    # Replace logger with QueueHandler to send logs to main process instead
    queue_handler = QueueHandler(log_queue)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(queue_handler)

    logger.info(f"Sender started for {bot}")
    # sender code here
