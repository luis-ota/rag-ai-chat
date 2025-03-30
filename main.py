from dotenv import load_dotenv

from frontend import AIChatApp

if __name__ == "__main__":
    load_dotenv()
    app = AIChatApp()
    app.run()