from pandas import read_csv
from kmeans import K_Means

CSV_PATH = "../../data/2d-sample.csv"
CSV_COLUMN_DELIMITER = ","

def _load_csv_data(path, delim):
    engine = "python"
    dataset = read_csv(path, "r", delimiter=delim, engine=engine, header=None)

    return dataset

"""Apply kmeans to dataset"""
def main():
    dataset = _load_csv_data(CSV_PATH, CSV_COLUMN_DELIMITER)
    handler = K_Means(dataset)

    handler.kmeans(k=4, visualizeSteps=False)

if __name__ == "__main__":
    main()