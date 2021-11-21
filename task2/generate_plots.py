import numpy as np
import matplotlib.pyplot as plt

CLIENTS_NUMBERS = [1, 2, 4]


def get_req_per_sec_from_wrk_file(file_name):
    with open('wrk_results/' + file_name) as f:
        lines = f.readlines()
        req_per_sec = ''
        should_start = False
        should_stop = False
        for character in lines[4]:

            if should_start == False and character == 'c':
                should_start = True
                continue

            if should_start:
                if character == ' ':
                    if should_stop:
                        break
                    continue
                else:
                    if character.isdigit() or character == '.':
                        req_per_sec = req_per_sec + character
                    elif character == 'k':
                        req_per_sec = req_per_sec.replace('.', '')
                        req_per_sec = req_per_sec + '0'
                        break
                    else:
                        break

                    if character == '.':
                        should_stop = True
        return req_per_sec


def get_req_per_sec_per_each_clients_number():
    req_per_sec_values = []

    for clients_number in CLIENTS_NUMBERS:
        value = get_req_per_sec_from_wrk_file('clients_nr_' + str(clients_number) + '.txt')
        req_per_sec_values.append(float(value))

    return req_per_sec_values


def generate_plot():
    req_per_sec_values = get_req_per_sec_per_each_clients_number()
    x_clients_numbers = np.array(CLIENTS_NUMBERS)
    y_req_per_sec_values = np.array(req_per_sec_values)

    plt.plot(x_clients_numbers, y_req_per_sec_values)

    plt.title('Req/sec for given number of clients.')
    plt.xlabel('Number of clients')
    plt.ylabel('Requests per second')

    plt.savefig('plot_result.png')


if __name__ == "__main__":
    generate_plot()
