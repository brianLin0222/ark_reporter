import requests
from datetime import *
from pandas import DataFrame



BASE_URL = "https://ark-funds.com/wp-content/fundsiteliterature/csv/"
REPORTS = {
            "ARKK":  "ARK_INNOVATION_ETF_ARKK_HOLDINGS",
            "ARKQ":  "ARK_AUTONOMOUS_TECHNOLOGY_&_ROBOTICS_ETF_ARKQ_HOLDINGS",
            "ARKW":  "ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS",
            "ARKG":  "ARK_GENOMIC_REVOLUTION_MULTISECTOR_ETF_ARKG_HOLDINGS",
            "ARKF":  "ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS"
            }
SAVE_PATH = r"./download"




class ARKreport():
    def __init__(self,ark_ticker):
        self.resp = None
        self.raw_data = None
        self.ticker = ark_ticker
        self.report_name = REPORTS[ark_ticker]
        self._run()


    def _fetchData(self):
        url = f"{BASE_URL}{self.report_name}.csv"
        resp = requests.get(url)
        if resp.status_code == 200:
            self.resp = resp
        else:
            raise Exception(f"No data returned, response status{resp.status_code}")


    def _formatData(self):
        data = self.resp.iter_lines()
        try:
            self.raw_data = []
            # col_mode = {}
            for row in data:
                row_data = row.decode().split(',')
                if len(set(row_data))>1:
                    self.raw_data.append(row_data)
                else:                           ##stop parsing data when there is a blank line
                    break
        except Exception as err:
            raise Exception(f"Unable to format data, error:{err}")
    
    
    def _run(self):
        self._fetchData()
        self._formatData()
        try:
            df = DataFrame(self.raw_data[1:],columns=self.raw_data[0])
            df.to_csv(f"{SAVE_PATH}/{self.ticker}/{self.ticker}_{date.today().strftime('%Y%m%d')}.csv",index=False)
        except Exception as err:
            raise Exception(f"Unable to generate CSV file, error:{err}")
            
