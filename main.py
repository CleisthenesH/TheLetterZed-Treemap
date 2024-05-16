# Copyright 2024 Kieran Harvie.
# All rights reserved.
# Use of this source code is governed by an Apache-style
# license that can be found in the LICENSE file.

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import squarify 
import pandas as pd
import seaborn as sb
from textwrap import wrap

excel = pd.read_excel('Expected Value of Mann vs. Machine.xlsx',sheet_name = None)

def make_treeplot(sheet):
    df = excel[sheet]
    df.sort_values(by=["Expected Value (Keys)"],ascending=False)

    rects = squarify.squarify(
           squarify.normalize_sizes(df["Expected Value (Keys)"],1,1)
           ,0,0,1,1)

    transpose = ({
            'p':(a['x'],a['y']),
            'dx':a['dx'],
            'dy':a['dy'],
            'text':'\n'.join(wrap(b,15)),
            'color':c
            }for a,b,c in zip(rects,df["Item"],sb.color_palette("tab20",len(rects))))

    plt.figure(figsize=(15,15))
    ax = plt.gca()

    for rect in transpose:
        ax.add_patch(Rectangle(rect['p'],rect['dx'],rect['dy'],linewidth=1,edgecolor='black',facecolor=rect['color']))#,label=rect["text"]))
        ax.annotate(rect["text"],rect['p'])

    plt.title(sheet)
    plt.axis('off')
    plt.savefig(sheet + '.png')

for sheet in {"OilSpill","SteelTrap","MechaEngine","TwoCities","GearGrinder","Australium"}:
    make_treeplot(sheet)
