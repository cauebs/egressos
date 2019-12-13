import csv
from sys import argv

import matplotlib.pyplot as plt
import seaborn as sns


def run():
    try:
        program_id = int(argv[1])
    except IndexError:
        program_id = None

    with open(f"{program_id}.csv") as f:
        data = list(csv.reader(f))

    enrollment = [float(row[-2]) for row in data]
    duration = [float(row[-1]) - float(row[-2]) + 0.5 for row in data]
    sns.lineplot(enrollment, duration)
    plt.show()
