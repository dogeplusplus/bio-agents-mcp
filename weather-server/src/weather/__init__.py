from . import server
import asyncio


def main():
    asyncio.run(server.main())


if __name__ == "__main__":
    main()