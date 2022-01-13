import json

import matplotlib.pyplot as plt


def split(word):
    return [char for char in word]


def convert_bs_to_number(bs: str):
    bs_list = split(bs)
    bs_text = bs_list[0]
    if not bs_list[1] == 'k':
        bs_text += bs_list[1]

    return int(bs_text) * 1000 if bs_list[1] == "k" or bs_list[2]== "k" else int(bs_text)


def convert_job_name_to_graph_name(js: str):
    js_list = js.split('_')
    job_name = ""
    if js_list[2] == 'direct':
        job_name = js_list[3]
    else:
        job_name = js_list[2]
    return js_list[0] + ' ' + js_list[1] + ' ' + job_name


def read_from_file(file_name: str):
    my_file = open(file_name)
    my_dict = json.load(my_file)

    btrfs_read = []
    btrfs_write = []
    ext4_read = []
    ext4_write = []

    result = []

    for jobs in my_dict['jobs']:
        read = jobs['read']
        write = jobs['write']
        if not read['bw'] == 0:
            data_point = (convert_bs_to_number(jobs['job options']['bs']), read['bw_bytes'] / pow(2,20),
                          convert_job_name_to_graph_name(jobs['job options']['name']))
            if 'btrfs' in jobs['jobname']:
                btrfs_read.append(data_point)
            if 'ext4' in jobs['jobname']:
                ext4_read.append(data_point)

        if not write['bw'] == 0:
            data_point = (convert_bs_to_number(jobs['job options']['bs']), write['bw_bytes'] / pow(2,20),
                          convert_job_name_to_graph_name(jobs['job options']['name']))
            if 'btrfs' in jobs['jobname']:
                btrfs_write.append(data_point)
            if 'ext4' in jobs['jobname']:
                ext4_write.append(data_point)
    if ext4_read:
        result.append(ext4_read)
    if ext4_write and not ext4_read:
        result.append(ext4_write)
    if btrfs_read:
        result.append(btrfs_read)
    if btrfs_write and not btrfs_read:
        result.append(btrfs_write)

    return result


def get_data_for_app(files):
    data = []
    for file_name in files:
        data.append(read_from_file("results/" + file_name))

    return data


def generate_plot(files, operation):
    file_counter = 0
    grouped_data = get_data_for_app(files)

    for file_data in grouped_data:
        for result_data in file_data:
            x_only, y_only, label = zip(*result_data)
            txt = label[0]
            plt.plot(x_only, y_only, label=txt)
        file_counter += 1

    plt.title('Throughput using ' + operation)
    plt.xlabel('Block sizes')
    plt.ylabel('Throughput in MBit/s')
    plt.legend()
    plt.savefig("results/graphs/throughput_" + operation + ".png")
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()


def generate_plot_for_each_graph(plot_type: str):
    files = ['rand' + plot_type + '.json', 'seq' + plot_type + '.json']

    generate_plot(files, plot_type)


if __name__ == "__main__":
    plot_types = ["read", "write", "readwrite"]

    for plot_type in plot_types:
        generate_plot_for_each_graph(plot_type)
