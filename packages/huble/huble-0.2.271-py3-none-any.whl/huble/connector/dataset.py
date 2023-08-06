import pandas as pd
import requests
from pydantic import BaseModel
#import woodwork as ww
from ..util.data_types import get_dataframe_types

class Dataset:
    def __init__(self, url) -> None:
        self.url = url
        self.dataframe = self.__load_dataset(url)

    def __load_dataset(self, url: str) -> pd.DataFrame:
        local_filename = url.split("/")[-1]
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return pd.read_csv(local_filename)


    def parse_dataset(self):
        data_dict = get_dataframe_types(self.dataframe)
        data_dict['rows'] = len(self.dataframe.axes[0])
        return data_dict


