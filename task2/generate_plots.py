from typing import List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

CLIENTS_NUMBERS = [1, 2, 6, 16, 32]

# styling of plots
# partially taken from: https://github.com/Mic92/rkt-io (21.11.2021, 18:00 (UTC))
sns.set(rc={'figure.figsize': (3, 5)})
sns.set_style("whitegrid")
sns.set_style("ticks", {"xtick.major.size": 7, "ytick.major.size": 7})
sns.set_context("paper", rc={"font.size": 6, "axes.titlesize": 12, "axes.labelsize": 12})
sns.set_palette(sns.color_palette(palette="gray", n_colors=2))


def get_avr_req_per_sec_from_wrk_file(file_name: str) -> str:
    with open('results/' + file_name) as f:
        lines = f.readlines()
        req_per_sec = ''
        should_start = False
        should_stop = False
        for character in lines[4]:

            # wrk was not able to connect to target
            if lines[0:6] == "unable":
                break

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

def get_max_req_per_sec_from_wrk_file(file_name: str) -> str:
    with open('results/' + file_name) as f:
        lines = f.readlines()
        req_per_sec = ''
        should_start = False
        should_stop = False
        gaps = True
        look_for_non_space_char = True
        number_of_space_gap = 0
        for character in lines[4]:

            # wrk was not able to connect to target
            if lines[0:6] == "unable":
                break

            if should_start == False:

                if look_for_non_space_char == True:
                    if character != ' ':
                        look_for_non_space_char = False
                        gaps += 1
                else:
                    if character == ' ':
                        look_for_non_space_char = True

                if gaps == 5:
                    req_per_sec += character
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

def get_req_per_sec_per_each_clients_number() -> List[float]:
    avg_req_per_sec_values = []
    max_req_per_sec_values = []

    for clients_number in CLIENTS_NUMBERS:
        avg_value = get_avr_req_per_sec_from_wrk_file('clients_nr_' + str(clients_number) + '.txt')
        avg_req_per_sec_values.append(float(avg_value))

        max_value = get_max_req_per_sec_from_wrk_file('clients_nr_' + str(clients_number) + '.txt')
        max_req_per_sec_values.append(float(max_value))

    return {
        'avg_values': avg_req_per_sec_values,
        'max_values': max_req_per_sec_values
    }


def generate_plot() -> None:

    req_per_sec_values_obj = get_req_per_sec_per_each_clients_number()
    print(req_per_sec_values_obj)

    req_per_sec_values = req_per_sec_values_obj['avg_values']
    max_req_per_sec_values = req_per_sec_values_obj['max_values']

    df = pd.DataFrame(data={
        'clients_nr': CLIENTS_NUMBERS,
        'rps_values': req_per_sec_values
    })

    sns.scatterplot(x="clients_nr", y="rps_values", data=df)

    plt.xlabel('Number of Clients')
    plt.ylabel('Requests per Second (RPS)')
    plt.tight_layout()

    plt.savefig('/results/plot_result.svg')

    plt.show()


if __name__ == "__main__":
    generate_plot()
