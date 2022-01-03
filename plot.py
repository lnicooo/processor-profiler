#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import math

def makeSpider(categories, values, title):

    colors=['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']

    #categories += categories[:1]

    N = max(max(values))
    N = int(math.ceil(N/10))*10

    y_labels = np.arange(0,N+10,10)
    y_labels_str = [str(y) for y in y_labels]

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False)

    angles=np.append(angles,angles[:1])

    # Initialise the spider plot
    ax = plt.subplot(polar=True)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='grey', size=10)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks(y_labels, y_labels_str, color="grey", size=7)
    plt.ylim(0,N)

    for index,value in enumerate(values):
    # Ind1

        value += value[:1]
        ax.plot(angles, value, color=colors[index], linewidth=2, linestyle='solid')
        ax.fill(angles, value, color=colors[index], alpha=0.4)

    # Add a title
    plt.title(title, size=11, color="Grey", y=1.1)
