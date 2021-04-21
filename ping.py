#!/usr/bin/env python3

import subprocess
import platform
from itertools import count
import matplotlib
import matplotlib.pyplot as plt
import texttable as tt
# import sys
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.ticker import ScalarFormatter




def ping_target(target):

        try:
            output = subprocess.check_output("ping -{} 2 {}".format('n' if platform.system().lower(
            ) == "windows" else 'c', target ), shell=True, universal_newlines=True)


            if 'unreachable' in output:
                return False

            else:
                return output.split('\n')[-3:]

        except Exception:
                return False
 



if __name__ == '__main__':

    tab = tt.Texttable()

    rtt_of_targets = list()

    targets = ['tu.berlin', 'ruhr-uni-bochum.de', 'uni-hamburg.de',
            'lmu.de','kuleuven.be','port.ac.uk','kth.se','uw.edu.pl',\
            'ccsf.edu','nitt.edu','kyoto-u.ac.jp','aut.ac.nz']

    for _ in targets:

        out = ping_target(_)

        if out:
            rtt_of_targets.append(out[1].split("=")[1].split("/")[1])
        else:
            print("Unreachable Target")

    distance = [609.78,229.98,482.06,314.63,270.59,648.94, \
    1282.54,978.40,9152.22,7721.70,9314.80,18267.36]

    distance = [i * 100 for i in distance]

    distance = list(map(int,distance))


    result = sorted(zip(targets,rtt_of_targets,distance), key = lambda t: t[2])

    print(f'{"Nr.":<4} {"Target":<20} {"RTT(ms)":<10} {"Distance(m)":<10}\n')

    for i,(t,r,d) in enumerate(result,1):
        print(f'{i:<4} {t:<20} {r:<10} {d:<10}')


    ''' 
    
    Uncomment for table-like output of value

    '''

    # headings = ['Target','RTT(ms)','Distance(m)']
    # tab.header(headings)
    # for i,row in enumerate(result,1):
    #     tab.add_row(row)

    # s = tab.draw()
    # print(s)

        
    plot_target, plot_rtt, plot_d = zip(*result)

    plot_rtt = list(map(float,plot_rtt))
    

    # print(sys.version)
    fig = plt.figure()
    fig.suptitle('XXXXXXXXX', fontsize=20)

    y_formatter = ScalarFormatter(useOffset=False)
    
    categories = np.array([0, 1, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2])
    one = mpatches.Patch(facecolor='red', label='In Germany', linewidth = 0.5, edgecolor = 'black')
    two = mpatches.Patch(facecolor='green', label = 'In Europe(excl. DE)', linewidth = 0.5, edgecolor = 'black')
    three = mpatches.Patch(facecolor='blue', label = 'Rest of the World', linewidth = 0.5, edgecolor = 'black')
    legend = plt.legend(handles=[one, two, three], title="Targets",
                    loc=4, fontsize='medium', fancybox=True)
    frame = legend.get_frame() #sets up for color, edge, and transparency
    frame.set_facecolor('#b4aeae') #color of legend
    frame.set_edgecolor('black') #edge color of legend
    frame.set_alpha(1)
    colormap = np.array(['r', 'g', 'b'])

    plt.scatter(plot_d,plot_rtt,s=27, c=colormap[categories])
    plt.ylabel("RTT(ms)")
    plt.xlabel("Distance(m)")
    
    plt.grid(True)
    ax = plt.gca()
    ax.get_xaxis().get_major_formatter().set_scientific(False)
    plt.show()