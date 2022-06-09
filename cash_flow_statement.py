from statement import Statement


class Cash_Flow(Statement):
    def __init__(self, url, soup):
        super().__init__(url, soup)
