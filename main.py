from IoTWebsite import create_app
import os
import datetime as dt


app = create_app()


def main():
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5500, debug=True)

main()