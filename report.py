import pandas as pd

def generate_statistics(filename):

    df = pd.read_csv(filename)

    print(df.describe())

    df.to_csv(filename,index=False)