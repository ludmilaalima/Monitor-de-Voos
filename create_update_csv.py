import pandas as pd
import os
from pathlib import Path



class CreateUpdateCsv:
    def __init__(self, data=None):
        self.data_link = None

    def create_csv(self):
        for file in os.listdir(Path.cwd()):
            if file.endswith(".csv"):
                continue
        
        df = pd.DataFrame(
            {
                "id" : {}, 
                "price": {}, 
                'data' : {}
            }
        )


        df.to_csv("data.csv", index=False)

    def update_csv(self, element):
        for file in os.listdir(Path.cwd()):
            if file.endswith('.csv'):
                self.data_link = file



        new_line = {
            'id' : {1},
            'price' : {element},
            'data' : {1}
        }
        df = pd.read_csv(self.data_link)
        df = pd.concat([df, pd.DataFrame([new_line])], ignore_index=True)
        df.to_csv(self.data_link, index=False)