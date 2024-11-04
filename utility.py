# Copyright 2024 Kieran Harvie.
# All rights reserved.
# Use of this source code is governed by an Apache-style
# license that can be found in the LICENSE file.

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
import squarify 
import pandas as pd
from textwrap import wrap

excel = pd.read_excel('Expected Value of Mann vs. Machine.xlsx', sheet_name = None)

for df in excel:
    excel[df] = excel[df].loc[excel[df]["Expected Value (Keys)"] != 0]
    excel[df].sort_values(by=["Expected Value (Keys)"],ascending=False)

df = excel['TwoCities']

rects = squarify.squarify(
       squarify.normalize_sizes(df["Expected Value (Keys)"],1,1)
       ,0,0,1,1)

top_sheet = {b:{
        'p':(a['x'],a['y']),
        'dx':a['dx'],
        'dy':a['dy'],
        'color':'white',
        'weight':c
        }
        for a,b,c in zip(rects,df["Item"],df["Likelihood"])}

top_sheet['Australium'].update({
    'sheet':'Australium',
    'color':'gold',
    'dir':'australium'
    })

top_sheet['Two Cities Mission Completion'].update({
    'sheet':'TwoCitiesMission',
    'color':'red'
    })

top_sheet['Random Killstreak Kit'].update({
    'sheet':'Killstreak',
    'color':'powderblue'
    })

top_sheet['Random Specialized Killstreak Kit Fabricator'].update({
    'sheet':'SpecKillstreakFab',
    'color':'green'
    })

top_sheet['Random Professional Killstreak Kit Fabricator'].update({
    'sheet':'ProfKillstreakFab',
    'color':'darkorange'
    })

plt.figure(figsize=(15,15),facecolor = 'black')
plt.figure(facecolor = 'black')
ax = plt.gca()

def plot_nested_square(key,use_images):
    df = excel[top_sheet[key]['sheet']]

    if not use_images:
        patch = Rectangle(top_sheet[key]['p'],top_sheet[key]['dx'],top_sheet[key]['dy'],color='none') 
        ax.add_patch(patch)
        image = plt.imread('misc_images\\' + top_sheet[key]['sheet'] + '.png')

        d = 0.5*max(top_sheet[key]['dx'],top_sheet[key]['dy'])
        x = top_sheet[key]['p'][0] + 0.5*top_sheet[key]['dx']
        y = top_sheet[key]['p'][1] + 0.5*top_sheet[key]['dy']

        ax.imshow(image,extent = (x-d,x+d,y-d,y+d)).set_clip_path(patch)


    rects = squarify.squarify(
           squarify.normalize_sizes(
               df["Expected Value (Keys)"],
               top_sheet[key]['dx'],
               top_sheet[key]['dy']
            ),
               *top_sheet[key]['p'],
               top_sheet[key]['dx'],
               top_sheet[key]['dy']
            )

    transpose = ({
        'p':(a['x'],a['y']),
        'dx':a['dx'],
        'dy':a['dy'],
        'text':b,
        'value':c*top_sheet[key]['weight'],
        }for a,b,c in zip(rects,df["Item"],df["Expected Value (Keys)"]))


    for rect in transpose:
        patch = Rectangle(
                rect['p'],rect['dx'],rect['dy'],
                linewidth=1,
                edgecolor=top_sheet[key]['color'],
                facecolor='none',
                transform = ax.transData)
        ax.add_patch(patch)

        if use_images:
            image = plt.imread(top_sheet[key]['dir'] + '\\' + rect['text'] + '.png')

            d = 0.5*max(rect['dx'],rect['dy'])
            x = rect['p'][0]+0.5*rect['dx']
            y = rect['p'][1]+0.5*rect['dy']

            ax.imshow(image,extent = (x-d,x+d,y-d,y+d)).set_clip_path(patch)

        if rect['value'] > 0.02:
            ax.annotate('\n'.join(wrap(rect["text"],15)),(rect['p'][0]+0.01,rect['p'][1]+0.01),color='white')

for key in top_sheet:
    plot_nested_square(key,use_images = (key == 'Australium'))

plt.title('Two Cities',color='white')
plt.xlim([-0.01,1.01])
plt.ylim([-0.01,1.01])
plt.axis('off')
plt.legend(handles = [Patch(color=top_sheet[x]['color'],label = '\n'.join(wrap(x,15))) for x in top_sheet],loc='center left',bbox_to_anchor=(1,0.5))

plt.savefig('utility.png')
