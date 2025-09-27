import pandas as pd
import os
from pathlib import Path
from datetime import datetime
import shortuuid



class CreateUpdateCsv:
    def __init__(self, data='data.csv'):
        self.data_link = Path(data)

    def create_csv(self):
        if "data.csv" not in os.listdir(Path.cwd()):
    
            df = pd.DataFrame(columns=['id', 'price', "date"])
            df.to_csv("data.csv", index=False)
           

    def update_csv(self, element):
        
        date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        id = shortuuid.uuid()[:8]

        new_line = {
            'id' : id,
            'price' : element,
            'date' : date
        }

        pd.DataFrame([new_line], columns = ['id', 'price', 'date']).to_csv(
            self.data_link, mode='a', header=False, index=False
        )
        