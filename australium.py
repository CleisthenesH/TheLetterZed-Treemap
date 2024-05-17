# Copyright 2024 Kieran Harvie.
# All rights reserved.
# Use of this source code is governed by an Apache-style
# license that can be found in the LICENSE file.

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import squarify 
import pandas as pd
from textwrap import wrap

df = pd.read_excel('Expected Value of Mann vs. Machine.xlsx',sheet_name = 'Australium')

df.sort_values(by=["Expected Value (Keys)"],ascending=False)

rects = squarify.squarify(
       squarify.normalize_sizes(df["Expected Value (Keys)"],1,1)
       ,0,0,1,1)

transpose = ({
        'p':(a['x'],a['y']),
        'dx':a['dx'],
        'dy':a['dy'],
        'text':b,
        }for a,b in zip(rects,df["Item"]))

plt.figure(figsize=(15,15),facecolor = 'black')
ax = plt.gca()

for rect in transpose:
    image = plt.imread('australium\\' + rect['text'] + '.png')

    d = 0.5*max(rect['dx'],rect['dy'])
    x = rect['p'][0]+0.5*rect['dx']
    y = rect['p'][1]+0.5*rect['dy']

    patch = Rectangle(rect['p'],rect['dx'],rect['dy'],linewidth=1,edgecolor='white',facecolor='none',transform = ax.transData)

    ax.add_patch(patch)
    ax.imshow(image,extent = (x-d,x+d,y-d,y+d)).set_clip_path(patch)
    ax.annotate('\n'.join(wrap(rect["text"],15)),(rect['p'][0]+0.01,rect['p'][1]+0.01),color='white')

plt.xlim([-0.01,1.01])
plt.ylim([-0.01,1.01])
plt.axis('off')

plt.title('Australium',color='white')
plt.savefig('australium_image.png',bbox_inches='tight')
