import matplotlib.pyplot as plt
from pathlib import Path 
import pandas as pd

colorarray=['black','dimgrey','grey','darkgrey','lightgrey','darkslategrey','lightslategrey','slategrey', 'silver', 'gainsboro', 'dimgrey', 'grey', 'darkgrey']

node_range = [0.10, 0.20, 0.30]

markers = ['o-', 's--', 'D:', "^-", "v--", "o--", "s-", "D--", "^:", "v-", "o--", "s:"]

path = "test/test_sa_4/test_sa_4_1_results_dynamic/"
#get number of files in path
pathlist = Path(path).glob('**/*.csv')
pathlist = sorted(pathlist)
df_array = []

for p in pathlist:
    df_array.append(pd.read_csv(str(p)))

df = pd.concat(df_array, ignore_index=True)

x_values = []
y_values = []

for i in range(len(node_range)):
    x = df.loc[df['Node Range'] == node_range[i]]
    x_values.append(x.loc[:, "Network Polarization"])
    y_values.append(x.loc[:, "Virality"])

fig=plt.figure(figsize=(10, 5))
plt.rcParams.update({'font.size': 13})
ax=plt.subplot(111)

for i in range (len(node_range)):
    if (i > 4 and i < 10):
        ax.plot(x_values[i], y_values[i], markers[i], fillstyle = "none" , label=node_range[i], color = colorarray[i])
    else:
        ax.plot(x_values[i], y_values[i], markers[i], label=node_range[i], color = colorarray[i])


plt.ylabel("Virality (Global Cascade fraction)")
plt.xlabel("Pn (Network Polarization)")

# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Node Range")
plt.grid(visible=True,linewidth=0.2)

filepath = Path(path + 'test_sa_4_T270.png')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
fig.savefig(filepath)




