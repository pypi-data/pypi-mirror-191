import pkgutil
import pandas as pd
from io import StringIO

def _load_dataset(name):
    available = ['a1', 'a2', 'a3', 's1', 's2', 's3', 's4', 'unbalanced']
    if name not in available:
        raise RuntimeError(f'dataset name must be in {{available}}')

    csvstring = pkgutil.get_data(__name__, f'./csv/{name}.csv').decode()
    df = pd.read_csv(StringIO(csvstring))
    return df#.to_numpy()


def DefaultDataset(name):
    """Load a built-in dataset as a pandas DataFrame"""
    return _load_dataset(name)

    
    

    

    
