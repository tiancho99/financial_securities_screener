class FinancialStatement:
    def __init__(self, url, soup):
        self.url = url
        self.soup = soup

        def get_