import sys
from pandas import read_csv
from kmeans import KMeans


CSV_PATH = "src/main/resources/2d-sample.csv"#sys.argv[1]
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

    handler = KMeans(dataset, k=k)
    handler.kmeans()
    while k < max_iter:
        handler.reinitialize(k=k)
        handler.kmeans()
        k += 1

if __name__ == "__main__":
    main()
