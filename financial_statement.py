from statement import Statement
from IPython.display import display
import numpy as np
import time


class FinancialStatement(Statement):
    def __init__(self, url, soup):
        super().__init__(url, soup)
        self.replace_values()
        self.table.index = self.table[0]
        self.table.index.name = "Category"
        self.table = self.table.drop(0, axis=1)
        self.table = self.table.dropna(axis=1, how="all")
        self.table.columns = self.statement_data["headers"][-1]

    def replace_values(self):
        self.table = self.table.replace(r" \(loss\)", "", regex=True) \
            .replace(r" \(in dollars per share\)", "", regex=True)\
            .replace(r"[$,)]", "", regex=True) \
            .replace(r"[(]", "-", regex=True)\
            .replace(r"\[1\]", np.nan, regex=True)\
            .replace(r"", np.nan, regex=True)\
            .replace(r"net loss", "net income")\
            .replace(r"net earnings", "net income")\
            .replace(r"net wages", "net income")\
            .replace(r"taxable income", "net income")\
            .replace(r"net pay", "net income")\
            .replace(r"real wages", "net income")\
            .replace(r"take-home income", "net income")\
            .replace(r"wages after taxes", "net income")\
            .replace(r"take-home", "net income")\
            .replace(r"(?=.*\bnet\b)(?=.*\bincome\b)(?=.*\bper\b)(?=.*\bshare\b).*", "earnings per "
                                                                                                     "share")\
            .replace(r"(?=.*\bnet\b)(?=.*\bloss\b)(?=.*\bper\b)(?=.*\bshare\b).*", "earnings per "
                                                                                     "share")\
            .replace(r"profit of earnings", "earnings per share")\
            .replace(r'None', "NaN", regex=True)

