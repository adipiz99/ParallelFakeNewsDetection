import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np 
import pandas as pd
from matplotlib.lines import Line2D

colorarray=['black','dimgrey','grey','darkgrey','lightgrey','darkslategrey','lightslategrey','slategrey', 'silver', 'gainsboro', 'dimgrey', 'grey', 'darkgrey']

tresholds = [0.270, 0.342, 0.414]
nr = [0.10, 0.20, 0.30]

path = "test/test_sa_5/test_sa_5_graphic_bar/test_1_results/"
df1 = pd.read_csv(path + 'test_1_3.csv')
df2 = pd.read_csv(path + 'test_1_4.csv')
df_no_sa = pd.concat([df1, df2], ignore_index=True)


path = "test/test_sa_5/test_sa_5_1_results_static/"
pathlist1 = Path(path).glob('**/*.csv')
pathlist1 = sorted(pathlist1)
df_array1 = []
for p in pathlist1:
    df_array1.append(pd.read_csv(str(p)))
df_10 = pd.concat(df_array1, ignore_index=True)

path = "test/test_sa_5/test_sa_5_2_results_static/"
pathlist2 = Path(path).glob('**/*.csv')
pathlist2 = sorted(pathlist2)
df_array2 = []
for p in pathlist2:
    df_array2.append(pd.read_csv(str(p)))
df_20 = pd.concat(df_array2, ignore_index=True)

path = "test/test_sa_5/test_sa_5_3_results_static"
pathlist3 = Path(path).glob('**/*.csv')
pathlist3 = sorted(pathlist3)
df_array3 = []
for p in pathlist3:
    df_array3.append(pd.read_csv(str(p)))
df_30 = pd.concat(df_array3, ignore_index=True)

scores_no_sa = []
scores_sa_10 = []
scores_sa_20 = []
scores_sa_30 = []
df = [df_no_sa, df_10, df_20, df_30]

for i in range(len(tresholds)):
    for j in range(len(df)):
        x = df[j].loc[df[j]['Treshold'] == tresholds[i]]
        y = x.loc[:, "Virality"]
        y = np.mean(y)

        if (j == 0):
            scores_no_sa.append(y)
        elif (j == 1):
            scores_sa_10.append(y)
        elif (j == 2):
            scores_sa_20.append(y)
        else:
            scores_sa_30.append(y)

values5 = np.concatenate([scores_sa_10, scores_sa_20, scores_sa_30])
mediatotale = np.mean(values5)
print("{:.2f}".format(mediatotale))

x = np.arange(len(tresholds))  # the label locations
width = 0.2  # the width of the bars

r1 = x
r2 = [x + width+0.03 for x in r1]
r3 = [x + width+0.03 for x in r2]
r4 = [x + width+0.03 for x in r3]

fig, ax = plt.subplots()
plt.rcParams.update({'font.size': 15})

rects1 = ax.bar(r1, scores_no_sa, width, label='No sa, no bias', color='black', hatch='//')
rects2 = ax.bar(r2, scores_sa_10, width, label='sa WI = 0.2, WIN = 0.30', color='green', hatch='x', zorder=0)
rects3 = ax.bar(r3, scores_sa_20, width, label='sa WI = 0.1, WIN = 0.50', color='limegreen', hatch='xx')
rects4 = ax.bar(r4, scores_sa_30, width, label = "sa WI = 0.2, WIN = 0.50", color="yellowgreen", hatch='/'), 

threshold = 0.50
linea=plt.axhline(y=threshold,linewidth=1, color='k',linestyle='--', label = "Virality 0.5")
plt.ylim([0,0.9])
ax.yaxis.set_tick_params(labelsize=15)
# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Average Virality', fontsize = 15)
#ax.set_title('Comparison between the best results', fontweight='bold')
width += (0.15)
ax.set_xticks(x+width)
ax.set_xticklabels(tresholds,rotation=45, fontsize = 15)
ax.set_xlabel("\u03B8 (threshold)", fontsize = 15)
ax.legend()
colors = ['black']
lines = [Line2D([0], [0], color=c, linewidth=1, linestyle='--') for c in colors]
labels = ['Single-view']
#ax.legend([rects1,rects2,rects3,rects4,linea],('No sa','sa nr = 0.10', 'sa nr = 0.20', 'sa nr = 0.30','Virality 0.5'))

fig.set_figheight(6)
fig.set_figwidth(12)
fig.tight_layout()

#filepath = Path('test/test_sa_5/test_sa_5_graphic_bar/test_sa_bias_static_wi_win_difference.png')  
#filepath.parent.mkdir(parents=True, exist_ok=True)  
#fig.savefig(filepath)

plt.show()
