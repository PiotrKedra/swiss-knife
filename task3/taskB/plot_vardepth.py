import json

import matplotlib.pyplot as plt


def convert_job_name_to_graph_name(js: str):
    js_list = js.split('_')
    job_name = ""
    if js_list[2] == 'direct':
        job_name = js_list[3]
    else:
        job_name = js_list[2]
    return job_name


def read_from_file(file_name_tuple):
    btrfs_read = []
    btrfs_write = []
    ext4_read = []
    ext4_write = []

    result = []

    for file_name in file_name_tuple:
        my_file = open(file_name)
        my_dict = json.load(my_file)



        for jobs in my_dict['jobs']:
            read = jobs['read']
            write = jobs['write']
            if not read['bw'] == 0:
                data_point = (int(jobs['job options']['iodepth']), read['bw'] / 1024,
                          convert_job_name_to_graph_name(jobs['job options']['name']))
                if 'btrfs' in jobs['jobname']:
                    btrfs_read.append(data_point)
                if 'ext4' in jobs['jobname']:
                    ext4_read.append(data_point)

            if not write['bw'] == 0:
                data_point = (int(jobs['job options']['iodepth']), write['bw'] / 1024,
                          convert_job_name_to_graph_name(jobs['job options']['name']))
                if 'btrfs' in jobs['jobname']:
                    btrfs_write.insert(0, data_point) if data_point[0] == 2000 else btrfs_write.append(data_point)
                if 'ext4' in jobs['jobname']:
                    ext4_write.insert(0, data_point) if data_point[0] == 2000 else ext4_write.append(data_point)

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


def generate_plot(files):
    grouped_data = read_from_file(files)

    result_data = grouped_data[0]
    result_data_2 = grouped_data[1]

    print(result_data)


    x_only, y_only, label = zip(*result_data)
    txt = label[0]
    plt.plot(x_only, y_only, label=txt)

    plt.title('Throughput for variable iodepth')
    plt.xlabel('I/O depth')
    plt.ylabel('Throughput in MBit/s')
    plt.legend()
    plt.savefig("results/graphs/throughput_iodepth.png")
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()


if __name__ == "__main__":
    generate_plot(["results/vardepth_btrfs.json", "results/vardepth_ext4.json"])
