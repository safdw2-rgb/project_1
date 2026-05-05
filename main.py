import logging
from src.contact_bot import Operator


logging.basicConfig(
    level=logging.INFO,
    filename="helper_bot_history.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def start_app():
    operator = Operator()
    operator.main()

if __name__ == "__main__":
    start_app()