import os
import json
import logging
logger = logging.getLogger("nosferatu")

from multiprocessing import Process, Queue
from contextlib import contextmanager


from nosferatu.listen.listen import init_listener
from nosferatu.think.think import init_processor
from nosferatu.reply.reply import init_sender


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




@contextmanager
def managed_process(target, *args, **kwargs):
    process = Process(target=target, args=args, kwargs=kwargs)
    process.start()
    try:
        yield process
    finally:
        process.terminate()
        process.join()
        logger.debug("Process terminated")




def main():
    all_bot_settings = load_bot_settings()
    print(type(all_bot_settings))

    que_set = [{'queue': Queue(), 'response_queue': Queue()} for _ in all_bot_settings]

    for bot_settings, que in zip(all_bot_settings, que_set):
        # logger.debug(f"Loaded settings for {bot_settings}")
        # logger.debug("Starting up bot: %s", bot_settings['name'])
        logger.debug("Starting up bot: %s", bot_settings)

        with managed_process(init_listener, bot_settings, que['queue']) as listener_process, \
                managed_process(init_processor, bot_settings, que['queue'], que['response_queue']) as processor_process, \
                managed_process(init_sender, bot_settings, que['response_queue']) as sender_process:

            try:
                logger.debug("bot running")

            # try:
            #     listener_process.start()
            #     processor_process.start()
            #     sender_process.start()

            except KeyboardInterrupt:
                logger.warning("Received keyboard interrupt...")
                # listener_process.terminate()
                # processor_process.terminate()
                # sender_process.terminate()

                # listener_process.join()
                # processor_process.join()
                # sender_process.join()



        # logger.warning("Terminating...")
        # for que in que_set:
        #     que['queue'].close()
        #     que['response_queue'].close()
        #     que['queue'].join_thread()
        #     que['response_queue'].join_thread()
        # listener_process.join()
        # processor_process.join()
        # sender_process.join()









    # all_bot_settings = load_bot_settings()

    # for bot in all_bot_settings:
    #     logger.debug(f"Loaded settings for {bot}")

    # queue = Queue()
    # response_queue = Queue()

    # for bot in all_bot_settings:
    #     # Start the processes
    #     listener_process = Process(target=init_listener, args=(queue,))
    #     processor_process = Process(target=init_processor, args=(queue, response_queue))
    #     sender_process = Process(target=init_sender, args=(response_queue,))

    #     listener_process.start()
    #     processor_process.start()
    #     sender_process.start()

    # try:
    #     listener_process.join()
    #     processor_process.join()
    #     sender_process.join()

    # except KeyboardInterrupt:
    #     logger.warning("Terminating...")
    #     listener_process.terminate()
    #     processor_process.terminate()
    #     sender_process.terminate()
    #     listener_process.join()
    #     processor_process.join()
    #     sender_process.join()
