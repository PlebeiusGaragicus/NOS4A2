if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()

    from admin_panel.login import login_router_page
    login_router_page()
