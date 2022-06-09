from statement import Statement


class BalanceSheet(Statement):
    def __init__(self, url, soup):
        super().__init__(url, soup)
