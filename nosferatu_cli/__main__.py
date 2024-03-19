if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    # import logging
    # from nosferatu_cli.logger import setup_logging
    # setup_logging()
    # logger = logging.getLogger("nosferatu")
    # logger.debug("Starting Nosferatu!")

    from nosferatu_cli.main import main
    main()



#################
#TODO
# ERROR | (_logging.py @ 77) | Connection to remote host was lost. - goodbye
