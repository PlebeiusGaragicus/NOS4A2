if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()

    # import os
    # os.environ["LANGCHAIN_TRACING_V2"] = "true"
    # os.environ["LANGCHAIN_PROJECT"] = "PlebChat"


    from src.login import login_router_page
    login_router_page()
