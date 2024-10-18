from src.app import create_app, create_tables


create_tables()
app = create_app()


if __name__ == "__main__":
    app.run()
