import os
from Monitor import monitor
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    monitor(os.getenv("url"), os.getenv("email"), os.getenv("password"), interval=1)
    