import Statistics

if __name__ == '__main__':
    statistics = Statistics.Statistics("Datasets/WholeYear.csv", "Datasets/DatasetSex.pkl",
                                       "Datasets/DatasetRelations.pkl", 100, 100)
    statistics.GetDatasetSex(False)
    statistics.GetDatasetRelations(False)
    statistics.Plotting(10, 10, "image.png")

