import numpy as np
import matplotlib
#matplotlib.use("Agg")
import matplotlib.pyplot as plt

N = 5
menMeans = [20, 35, 30, 35, 27]

ind = np.arange(N)  # the x locations for the groups
width = 0.05       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, menMeans, width, color='r')

womenMeans = (25, 32, 34, 20, 25)
rects2 = ax.bar(ind+width, womenMeans, width, color='y')

# add some text for labels, title and axes ticks
ax.set_ylabel('Scores')
ax.set_title('Scores by group and gender')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('G1', 'G2', 'G3', 'G4', 'G5') )

#ax.legend( rects2[0],'Women')
#ax.legend( rects1[0],'Men')
ax.legend( [rects1[0], rects2[0]], ['Men', 'Women'] )

#ax.legend( (rects2[0]), ('Women') )
def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

#autolabel(rects1)

#plt.show()
plt.savefig("foo.png")
