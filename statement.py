import pandas as pd


class Statement:
    def __init__(self, url, soup):
        self.url = url
        self.soup = soup.find("table")
        self.statement_data = {
            "headers": [],
            "sections": [],
            "data": [],
        }
        self.table = self.get_table()

    def get_table(self):
        rows = self.soup.find_all('tr')
        for row in rows:
            cols = row.find_all("td")

            if len(row.find_all("th")) == 0:
                reg_row = [ele.text.strip().lower() for ele in cols]
                self.statement_data["data"].append(reg_row)

            # if len(row.find_all("th")) == 0 and len(row.find_all("strong")) != 0:
            #     sec_row = cols[0].text.strip()
            #     self.statement_data["sections"].append(sec_row)

            elif (r := row.find_all("th")) != 0:
                th_row = [ele.text.strip() for ele in r]
                self.statement_data["headers"].append(th_row)

        table = pd.DataFrame(self.statement_data["data"])
        # print(self.statement_data["headers"])
        # display(table.iloc[1])

        return table
