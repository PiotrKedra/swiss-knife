import json
import matplotlib.pyplot as plt
import numpy as np

def read_avarage(name):
    f = open(name,)
    data = json.load(f)
    throughput = data['throughput']
    return [
        throughput['p1'],
        throughput['p10'],
        throughput['p25'],
        throughput['p50'],
        throughput['p75'],
        throughput['p90'],
        throughput['p99']]


def make_figures(method, request_nums, fig_nr):

    fig_num = fig_nr

    percentils = [1, 10, 25, 50, 75, 90, 99]
    workers_nums = [1, 5, 10, 20, 50, 100]

    x_request = np.array(request_nums)
    x_workers = np.array(workers_nums)

    for req in request_nums:
        fig = plt.figure(fig_num)
        fig.suptitle(method + ' throughput (Requests nr: ' + str(req) + ')')
        for wor in workers_nums:
            plot_arr = []
            work_arr = []
            file_name = 'optimized/' + method + '_performance_w_' + str(wor) + '_a_' + str(req) + '.json'
            value = read_avarage(file_name)
            plot_arr = list(plot_arr + value)
            for i in range(0, 8):
                work_arr.append(wor)

            y_plot_arr = np.array(plot_arr)
            x_new_work = np.array(percentils)
            label = 'Workers: ' + str(wor)
            plt.plot(x_new_work, y_plot_arr, label=label)


        fig_num = fig_num + 1
        plt.legend(loc="lower right")
        plt.xlabel("Percentile value of histogram")
        plt.ylabel("Response data throughput")




request_nums_post = [5000, 15000, 25000]
request_nums_get = [50, 150, 250]

make_figures('get', request_nums_post, 1)
make_figures('post', request_nums_get, 4)

plt.show()