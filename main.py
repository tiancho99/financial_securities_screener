from argparse import ArgumentParser
import requests
import bs4 import BeautifulSoup



def get_arguments():
    # TODO: add help argument to date
    parser = ArgumentParser(description="Get financial information of a given company")
    parser.add_argument("cik", type=ascii, help="Central Index Key")
    parser.add_argument("form_type", type=ascii, help="10K, 10Q")
    parser.add_argument("date", default=today, type=ascii, help="pending")

    return parser.parse_args()


def main():
    args = get_arguments()
    print(args)


if __name__ == '__main__':
    main()
