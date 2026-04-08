from app import app as fastapi_app
from app import main as root_main


app = fastapi_app


def main():
    return root_main()


if __name__ == "__main__":
    main()
