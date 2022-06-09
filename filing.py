import requests
from bs4 import BeautifulSoup
from financial_statement import FinancialStatement
from balance_sheet import BalanceSheet
from cash_flow_statement import Cash_Flow


def get_statement_soup(report, base_url):
    html_file_name = report.find("HtmlFileName").text
    statement_url = base_url + "/" + html_file_name
    response = requests.get(statement_url, headers={'User-Agent': 'My User Agent 1.0'}).content
    soup = BeautifulSoup(response, "lxml")
    return statement_url, soup



def request_reports(base_url):
    response = requests.get(base_url + "/FilingSummary.xml", headers={'User-Agent': 'My User Agent 1.0'}).content
    # print(base_url + "/FilingSummary.xml")
    return BeautifulSoup(response, "lxml-xml")


class Filing:
    def __init__(self, accession_number, base_url, date):
        self.url = base_url
        self.date = date
        self.reports = request_reports(base_url).find_all("Report")
        self.accession_number = accession_number
        self.financial_statement = None
        self.balance_sheet = None
        self.cash_flow_statement = None

        self.request_statements(base_url)

    def request_statements(self, base_url):
        for report in self.reports:
            short_name = report.find("ShortName").text.upper()
            if (short_name == "CONSOLIDATED STATEMENT OF OPERATIONS" or
                    short_name == "CONSOLIDATED STATEMENTS OF OPERATIONS" or
                    short_name == "INCOME STATEMENTS" or
                    short_name == "INCOME STATEMENT" or
                    short_name == "CONSOLIDATED STATEMENT OF EARNINGS" or
                    short_name == "CONSOLIDATED STATEMENTS OF EARNINGS" or
                    short_name == "CONSOLIDATED STATEMENT OF INCOME" or
                    short_name == "CONSOLIDATED STATEMENTS OF INCOME"):
                fs_url, soup = get_statement_soup(report, base_url)
                self.financial_statement = FinancialStatement(fs_url, soup)

            elif (short_name == "CONSOLIDATED BALANCE SHEETS" or
                    short_name == "CONSOLIDATED BALANCE SHEET" or
                    short_name == "BALANCE SHEET" or
                    short_name == "BALANCE SHEETS"):
                bs_url, soup = get_statement_soup(report, base_url)
                self.balance_sheet = BalanceSheet(bs_url, soup)

            elif (short_name == "CONSOLIDATED STATEMENTS OF CASH FLOWS" or short_name == "CASH FLOWS STATEMENTS" or
                    short_name == "CONSOLIDATED STATEMENT OF CASH FLOWS" or
                    short_name == "CONSOLIDATED STATEMENT OF CASH FLOW" or
                    short_name == "CONSOLIDATED STATEMENTS OF CASH FLOW"):
                cf_url, soup = get_statement_soup(report, base_url)
                self.cash_flow_statement = Cash_Flow(cf_url, soup)


