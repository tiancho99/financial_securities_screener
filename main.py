from argparse import ArgumentParser
# import pandas as pd
import requests
from bs4 import BeautifulSoup

# from financial_statement import FinancialStatement
from filing import Filing


def get_arguments():
    # TODO: add help and default arguments to date
    parser = ArgumentParser(description="Get financial information of a given company")
    parser.add_argument("cik", help="Central Index Key")
    parser.add_argument("form_type", help="10K, 10Q")
    # parser.add_argument("dateb", default="", type=ascii, required=False, help="pending")

    return parser.parse_args()


def main():
    args = get_arguments()
    base_url = r"https://www.sec.gov"

    # Establish URL where 10-k filings are
    filings_url = base_url + "/cgi-bin/browse-edgar"

    # request to filings_url
    headers = {
        'User-Agent': 'My User Agent 1.0'
    }
    params = {
        "action": "getcompany",
        "CIK": args.cik,
        'type': args.form_type,
        # 'dateb': args.dateb,
        'owner': 'exclude',
        'start': '',
        'output': 'atom',
        'count': 12,
    }
    response = requests.get(url=filings_url, params=params, headers=headers)
    soup = BeautifulSoup(response.content, "lxml-xml")
    print(response.url)
    # Obtain every filing
    entries = soup.find_all("entry")
    filings = []

    # Get 10k every 3 filings because of repeated information
    for i in range(0, len(entries), 3):
        filing_type = entries[i].find("filing-type").text.lower()
        if entries[i] is not None and filing_type == args.form_type:
            filing_date = entries[i].find("filing-date").text
            # Get filing accession number to construct the url for the filing
            accession_number = entries[i].find("accession-number")
            accession_number = accession_number.text.replace('-', '')
            statement_url = base_url + f"/Archives/edgar/data/{args.cik}/{accession_number}"
            # Construct Filing object
            filing = Filing(accession_number, statement_url, filing_date)

            try:
                print(f"Financial statement {filing.financial_statement.url}")
            except AttributeError:
                print("There  was an error retrieving the Financial Statement")
                break

            try:
                print(f"Balance sheet {filing.balance_sheet.url}")
            except AttributeError:
                print("There  was an error retrieving the Balance Sheet")
                break

            try:
                print(f"Cash Flow{filing.cash_flow_statement.url}")
            except AttributeError:
                print("There  was an error retrieving the Cash Flow")
                break


if __name__ == '__main__':
    main()
