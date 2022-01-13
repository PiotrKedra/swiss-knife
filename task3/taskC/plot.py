import json
import matplotlib.pyplot as plt


WINDOWS_SIZES = [2,4,8,16,64,128,256,512]
UDP_DATA = [500,750,1000,2000,5000,10000]
PARALLEL_CONN = [1,2,4,8,16,32,64]

def read_bitepersec_from_file(file_name):
    f = open(file_name)

    data = json.load(f)

    return float(data['end']['sum_sent']['bits_per_second'])
    


def get_bandwidth_data(file_type):

    result = []
    for window_size in WINDOWS_SIZES:
        result.append(read_bitepersec_from_file('iperf_results/result_' + file_type + '_' + str(window_size) + 'k.json')/1000000.)

    return result


def dict_raise_on_duplicates(ordered_pairs):
    """Convert duplicate keys to JSON array."""
    d = {}
    for k, v in ordered_pairs:
        if k in d:
            if type(d[k]) is list:
                d[k].append(v)
            else:
                d[k] = [d[k],v]
        else:
           d[k] = v
    return d

def get_bandwidth_data_for_bdir():
    result_tx = []
    result_rx = []
    for window_size in WINDOWS_SIZES:
        file_name = 'iperf_results/result_bdir_' + str(window_size) + 'k.json'
        f = open(file_name)
        data = json.load(f, object_pairs_hook=dict_raise_on_duplicates) 

        result_tx.append(float(data['end']['sum_sent'][0]['bits_per_second'])/1000000.)
        result_rx.append(float(data['end']['sum_sent'][1]['bits_per_second'])/1000000.)

    return {
         'tx-c': result_tx,
         'rx-c': result_rx
     }

   # return result_tx_sum_rx


def generate_bandwidth_by_windows_size_figure():

    TYPES = ['basic','reverse']

    plt.figure()
    for type_ in TYPES:
        y_axis = get_bandwidth_data(type_)
        plt.plot(WINDOWS_SIZES, y_axis, label=type_)

    
    bdir_data = get_bandwidth_data_for_bdir()
    #plt.plot(WINDOWS_SIZES, bdir_data, label='bdir sum(TX-C, RX-C)')
    plt.plot(WINDOWS_SIZES, bdir_data['rx-c'], label='bdir RX-C')
    plt.plot(WINDOWS_SIZES, bdir_data['tx-c'], label='bdir TX-C')


    plt.legend(loc="lower right")
    plt.xlabel('window size') 
    plt.ylabel('bandwidth (Mbit/s)') 
    plt.title('window size by bandwidth figure') 
    plt.savefig('iperf_results/fig_window_size_by_bandwidth.png', dpi=100)


def get_data_for_udp():
    bandwidth = []
    lost_percent = []
    for udp_data in UDP_DATA:
        file_name = 'iperf_results/result_udp_' + str(udp_data) + '.json'
        f = open(file_name)
        data = json.load(f) 
        bandwidth.append(float(udp_data))
        lost_percent.append(int(data['end']['sum']['lost_percent']))
    
    return {
        'bandwidth': bandwidth,
        'lost_percent': lost_percent 
    }


def generate_udp_plot():
    data = get_data_for_udp()

    plt.figure()

    plt.plot(data['bandwidth'], data['lost_percent'])
    plt.ylabel('loss percentage') 
    plt.xlabel('bandwidth (Mbit/s)') 
    plt.title('UDP - bandwidth by loss percentage figure') 
    plt.savefig('iperf_results/fig_udp.png', dpi=100)


def get_data_for_parallel():
    bandwidth = []
    retransmits = []
    for parallel_conn in PARALLEL_CONN:
        file_name = 'iperf_results/result_parallel_' + str(parallel_conn) + '.json'
        f = open(file_name)
        data = json.load(f)
        
        bandwidth.append(float(data['end']['sum_sent']['bits_per_second'])/1000000.)
        retransmits.append(int(data['end']['sum_sent']['retransmits']))
    
    return {
        'bandwidth': bandwidth,
        'retransmits': retransmits 
    }

def generate_parallel_plot():
    data = get_data_for_parallel()

    plt.figure()

    xs = list(map(str, PARALLEL_CONN))
    ys = data['bandwidth']
    plt.bar(xs, ys)

    for x,y,z in zip(xs,ys,data['retransmits']):

        plt.annotate(z, # this is the text
                    (x,y), # these are the coordinates to position the label
                    textcoords="offset points", # how to position the text
                    xytext=(0,10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center
                    
    plt.xlabel('parallel connections') 
    plt.ylabel('bandwidth (Mbit/s)') 
    plt.title('parallel connections by bandwidth figure (annotated by retransmits)') 
    
    plt.savefig('iperf_results/fig_parallel.png', dpi=100)



if __name__ == "__main__":

    generate_bandwidth_by_windows_size_figure()
    generate_udp_plot()
    generate_parallel_plot()
