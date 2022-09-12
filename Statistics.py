import pickle
import csv
import matplotlib.pyplot as plt


def percentage(part: int, whole: int) -> float:
    return 100 * float(part) / float(whole)


class Statistics:
    def __init__(self, inputDataset: str,
                 outputDatasetSex: str,
                 outputDatasetRelations: str,
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
        figure, ax = plt.subplots(2, 1)

        ax[0].ticklabel_format(useOffset=False, style='plain')
        ax[0].scatter(self.selections, self.relations)
        ax[0].set_title("Процент женщин от общего количества")

        ax[1].ticklabel_format(useOffset=False, style='plain')
        ax[1].scatter(self.selections[:100], self.relations[:100])
        ax[1].set_title("Процент женщин от общего количества (Размеры выборок от 100 до 10000)")

        for a in ax:
            a.set_xlabel("Размер выборки")
            a.set_ylabel("Процент женщин")

        figure.set_figwidth(sizeByWidth)
        figure.set_figheight(sizeByHeight)

        plt.draw()
        plt.savefig(outputImage)
        plt.show()

        print("Количесто точек: " + str(len(self.relations)))
        print("Процент мужчин от общего количества: " + str(100 - self.relations[-1]))
        print("Процент женщин от общего количества: " + str(self.relations[-1]))
        print("Шаг выборки: " + str(self.samplingStep))
        print("Среднее значение: " + str(sum(self.relations) / len(self.relations)))
