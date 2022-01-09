import matplotlib.pyplot as plt

def read_from_file(file_name):
    f = open(file_name,)
    core_numbers = []
    calculation_times = []
    for line in f:
        
        stripped_line = line.strip()

        if (stripped_line[:4] == 'real'):
            min = ''
            sec = ''
            if_min = True
            for char in stripped_line[5:]:
                if (if_min == True):
                    if (char != 'm'):
                        min += char
                    else:
                        if_min = False
                        continue
                else:
                    if (char != 's'):
                        sec += char
                    else:
                        return float(sec) + (float(min) * 60)

        
CORES = ['1','2','4','8','16','32','64','128']

def get_data_for_app(app_name, data_type):
    data = []
    for core in CORES:
        data.append(read_from_file('results/' + app_name + '_' + data_type + '_' + core + '.txt'))

    return data


def generate_plot(result_name):
    fig, axes = plt.subplots(1, 3)
    fig.suptitle(result_name +  ' execution time by increasing number of threads for different data size.')
    fig.set_size_inches(15, 4.5, forward=True)


    data_sizes = ["small", "medium", "large"]
    
    axes_num = 0
    for data_size in data_sizes:

        y = get_data_for_app(result_name, data_size)
        x = CORES

        axes[axes_num].bar(x,y)
        axes[axes_num].set_title(data_size)
        if (axes_num == 0):
            axes[axes_num].set(xlabel='Number of threads', ylabel='Execution time (microseconds)')
        else:
            axes[axes_num].set(xlabel='Number of threads')

        axes_num += 1

    # plt.show()
    plt.savefig('results/' +  result_name + '.png', dpi=100)


if __name__ == "__main__":

    APP_TYPES = ["bodytrack", "blacksholes", "ferret"]
    
    for app in APP_TYPES:
        generate_plot(app)
