from __future__ import annotations
import pickle
import csv
import matplotlib.pyplot as plt


def percentage(part: int, whole: int) -> float:
    return 100 * float(part) / float(whole)


class Statistics:
    def __init__(self, inputDataset: str,
                 outputDatasetSex: str,
                 outputDatasetRelations: str | bytes,
                 firstNumberSampling: int,
                 samplingStep: int,
                 gender: str):

        self.relations = []
        self.datasetSex = []
        self.selections = []
        self.inputDataset = inputDataset
        self.outputDatasetSex = outputDatasetSex
        self.outputDatasetRelations = outputDatasetRelations
        self.firstNumberSampling = firstNumberSampling
        self.samplingStep = samplingStep
        self.gender = gender

    def GetDatasetSex(self, overwrite: bool):
        with open(self.inputDataset, newline='') as f:
            reader = csv.DictReader(f)
            self.datasetSex = [row['SEX'] for row in reader]

        if overwrite:
            with open(self.outputDatasetSex, 'wb') as f:
                pickle.dump(self.datasetSex, f)

    def GetDatasetRelations(self, overwrite: bool):
        self.selections = [s for s in range(self.firstNumberSampling,
                                            len(self.datasetSex), self.samplingStep)]
        if overwrite:
            for i in self.selections:
                sel = self.datasetSex[0:i]
                genderCount = 0
                for s in sel:
                    if s == self.gender: genderCount += 1
                self.relations.append(percentage(genderCount, len(sel)))

            with open(self.outputDatasetRelations, 'wb') as f:
                pickle.dump(self.relations, f)
        else:
            with open(self.outputDatasetRelations, 'rb') as f:
                self.relations = pickle.load(f)

    def Plotting(self, sizeByWidth: int, sizeByHeight: int, outputImage: str):
        fig, ax = plt.subplots()

        ax.ticklabel_format(useOffset=False, style='plain')

        self.relations = [100 - i for i in self.relations]
        ax.scatter(self.selections, self.relations)

        plt.title('Процент женщин от мужчин')
        plt.xlabel("Количество выборки")
        plt.ylabel("Процент женщин")

        fig.set_figwidth(sizeByWidth)
        fig.set_figheight(sizeByHeight)

        plt.draw()
        plt.savefig(outputImage)
        plt.show()
        print("Количесто точек: " + str(len(self.relations)))
        print("Среднее значение: " + str(sum(self.relations) / len(self.relations)))
