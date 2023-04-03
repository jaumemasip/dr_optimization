from typing import List, Optional
import pickle
import pandas as pd
import numpy as np
from pathlib import Path


def fit(
    X: pd.DataFrame,
    y: pd.Series,
    output_dir: str,
    class_order: Optional[List[str]] = None,
    row_weights: Optional[np.ndarray] = None,
    **kwargs,
) -> None:


    output_dir_path = Path(output_dir)
    if output_dir_path.exists() and output_dir_path.is_dir():

        #output all input training data into a csv so it can be downloaded via Artifact download
        X.to_csv("{}/transformed_data.csv".format(output_dir), index = False)

        #create an empty artifact file to satisfy drum requirements
        with open("{}/artifact.pkl".format(output_dir), "wb") as fp:
            pickle.dump(0, fp)


def transform(X: pd.DataFrame, transformer):  
    return X