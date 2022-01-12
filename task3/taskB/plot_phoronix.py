import json

import matplotlib.pyplot as plt
import numpy as np


def read_from_file(file_name: str):
    my_file = open(file_name)
    my_dict = json.load(my_file)

    results_dict = my_dict['results']

    results = []

    for experiment in results_dict:
        for identifier in results_dict[experiment]["results"]:
            results.append(results_dict[experiment]["results"][identifier]["value"])

    return results


def get_data_for_app(files):
    data = []
    for file_name in files:
        data.append(read_from_file("results/" + file_name))

    return data


def generate_plot(files):
    data = get_data_for_app(files)
    N = 4
    ind = np.arange(N)  # the x locations for the groups
    width = 0.27  # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(111)

    yvals = data[0]
    rects1 = ax.bar(ind, yvals, width, color='r')
    zvals = data[1]
    rects2 = ax.bar(ind + width, zvals, width, color='g')

    ax.set_ylabel('Files/s')
    ax.set_xlabel('Amount of 1MB Files')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(('1K', '5K', '4K, 32 subdirs', '1K No FS sync'))
    ax.legend((rects1[0], rects2[0]), ('ext4', 'btrfs'))

    def autolabel(rects):
        for rect in rects:
            h = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * h, '%d' % int(h),
                    ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    plt.title('Throughput for variable iodepth')
    plt.savefig("results/graphs/throughput_phoronix.png")


if __name__ == "__main__":
    generate_plot(["phoronix_ext4.json", "phoronix_btrfs.json"])
