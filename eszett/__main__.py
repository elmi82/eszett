import asyncio
import logging

from eszett import eszett


def main(args=None):
    logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(eszett.start())
    except KeyboardInterrupt:
        logging.info("Receieved abort signal")
        pass
    finally:
        logging.info("Thank you and goodbye")


if __name__ == "__main__":
    main()
