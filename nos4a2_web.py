if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()

    from nosferatu.login import login_router_page
    login_router_page()
