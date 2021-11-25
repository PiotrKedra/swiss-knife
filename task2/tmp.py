from typing import List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


with open('clients_nr_1.txt') as f:
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

    print(req_per_sec)