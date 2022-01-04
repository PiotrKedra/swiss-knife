import matplotlib.pyplot as plt

def read_from_file(file_name):
    f = open(file_name,)
    core_numbers = []
    calculation_times = []
    for line in f:
        stripped_line = line.strip()

        tmp = ""
        for char in stripped_line:
            if char == ' ':
                core_numbers.append(tmp)
                tmp = ""
                continue
            
            tmp += char
        
        calculation_times.append(int(tmp))
    
    return {
        'core_numbers': core_numbers,
        'calculation_times': calculation_times
    }



def generate_plot(result_name):
    fig, axes = plt.subplots(1, 3)
    fig.suptitle('Word count execution time by increasing number of threads for different data size.')
    fig.set_size_inches(15, 4.5, forward=True)


    data_sizes = ["small", "medium", "large"]
    
    axes_num = 0
    for data_size in data_sizes:
        data = read_from_file("results/" + result_name + "-" + data_size + ".txt")

        y = data['calculation_times']
        x = data['core_numbers']

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

    APP_TYPES = ["matrix", "word_count"]
    
    for app in APP_TYPES:
        generate_plot(app)