import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np 
import pandas as pd
from matplotlib.lines import Line2D

colorarray=['black','dimgrey','grey','darkgrey','lightgrey','darkslategrey','lightslategrey','slategrey', 'silver', 'gainsboro', 'dimgrey', 'grey', 'darkgrey']

tresholds = [0.270, 0.342, 0.414]

path = "test/test_sa_1/test_sa_1_3_results_static/"
pathlist1 = Path(path).glob('**/*.csv')
pathlist1 = sorted(pathlist1)
df_array1 = []
for p in pathlist1:
    df_array1.append(pd.read_csv(str(p)))
df_0 = pd.concat(df_array1, ignore_index=True)

path = "test/test_sa_2/test_sa_2_1_results_static/"
pathlist2 = Path(path).glob('**/*.csv')
pathlist2 = sorted(pathlist2)
df_array2 = []
for p in pathlist2:
    df_array2.append(pd.read_csv(str(p)))
df_15 = pd.concat(df_array2, ignore_index=True)

path = "test/test_sa_2/test_sa_2_2_results_static/"
pathlist3 = Path(path).glob('**/*.csv')
pathlist3 = sorted(pathlist3)
df_array3 = []
for p in pathlist3:
    df_array3.append(pd.read_csv(str(p)))
df_27 = pd.concat(df_array3, ignore_index=True)

scores_sa_0 = []
scores_sa_15 = []
scores_sa_27 = []
df = [df_0, df_15, df_27]


for i in range(len(tresholds)):
    for j in range(len(df)):
        x = df[j].loc[df[j]['Treshold'] == tresholds[i]]
        y = x.loc[:, "Virality"]
        y = np.mean(y)

        if (j == 0):
            scores_sa_0.append(y)
        elif(j == 1):
            scores_sa_15.append(y)
        else:
            scores_sa_27.append(y)

values2 = np.concatenate([scores_sa_0, scores_sa_15, scores_sa_27])
mediatotale = np.mean(values2)
print("{:.2f}".format(mediatotale))

x = np.arange(len(tresholds))  # the label locations
width = 0.2  # the width of the bars

r1 = x
r2 = [x + width+0.03 for x in r1]
r3 = [x + width+0.03 for x in r2]

fig, ax = plt.subplots()
plt.rcParams.update({'font.size': 10})

rects1 = ax.bar(r1, scores_sa_0, width, label='sa PO = 0', color='green', hatch='x', zorder=0)
rects2 = ax.bar(r2, scores_sa_15, width, label = "sa PO = 0.15", color="limegreen", hatch='/'), 
rects3 = ax.bar(r3, scores_sa_27, width, label = "sa PO = 0.27", color='yellowgreen', hatch='+'), 

threshold = 0.50
linea=plt.axhline(y=threshold,linewidth=1, color='k',linestyle='--', label = "Virality 0.5")
plt.ylim([0,0.9])
ax.yaxis.set_tick_params(labelsize=15)
# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Average Virality', fontsize = 15)
#ax.set_title('Comparison between the best results', fontweight='bold')
width += (0.14)
ax.set_xticks(x+width)
ax.set_xticklabels(tresholds,rotation=45, fontsize = 15)
ax.set_xlabel("\u03B8 (threshold)", fontsize = 15)

colors = ['black']
lines = [Line2D([0], [0], color=c, linewidth=1, linestyle='--') for c in colors]
labels = ['Single-view']
ax.legend()
#ax.legend([rects1, rects2, rects3, rects4, rects5, rects6, linea],('No sa PO = 0.27','sa PO = 0.27', 'Virality 0.5'))

fig.set_figheight(7)
fig.set_figwidth(14)
fig.tight_layout()

# filepath = Path('test/test_sa_2/test_sa_2_graphic_bar/test_sa_confbias_static_po_difference.png')  
# filepath.parent.mkdir(parents=True, exist_ok=True)  
# fig.savefig(filepath)

plt.show()