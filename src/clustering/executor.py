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
    k = 2
    max_iter = 10

    handler = K_Means(dataset, k=k, visualizeSteps=False)
    handler.kmeans()
    while k < max_iter:
    	handler.reinitialize(k=k, visualizeSteps=False)
    	handler.kmeans()
    	k += 1

if __name__ == "__main__":
    main()