import matplotlib.pyplot as plt
from matplotlib import container
import numpy as np

errbar=[7,5,1,1,'x']

def plots(figsize=(6,4)):
    fig, ax = plt.subplots(figsize=figsize,dpi=120)
    return ax

def errorbar(ax, x_val,y_val,y_err,x_err=[0],errbar=[7,5,1,1,'x'],color='tab:red',line='',label='Daten'):
    

    # if x_err != '':
    #     ax.errorbar(x_val, y_val,color=color,marker=errbar[4],markersize=errbar[0],linestyle=line,
    #     yerr=y_err, xerr=x_err,label=label,capsize=errbar[1], elinewidth=errbar[2])
    # else:
    #     ax.errorbar(x_val, y_val,color=color,marker=errbar[4],markersize=errbar[0],linestyle=line,
    #     yerr=y_err,label=label,capsize=errbar[1], elinewidth=errbar[2])


    if isinstance(x_err,(list,np.ndarray)) == False:
        x_err = [x_err]*len(x_val)
    ax.errorbar(x_val, y_val,color=color,marker=errbar[4],markersize=errbar[0],linestyle=line,
        yerr=y_err, xerr=x_err,label=label,capsize=errbar[1], elinewidth=errbar[2])
        
    return errbar

def style():
    try:
        plt.style.use(['default','science','grid'])
    except:
        plt.style.use('default')
    plt.rcParams['axes.grid'] = True
    plt.rcParams['font.size'] = 11
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['figure.dpi'] = 120
    plt.rcParams['legend.frameon'] = True
    plt.rcParams['figure.figsize'] = [6.5,4.5]
    
    
def legend(ax,size=10):
    handles, labels = ax.get_legend_handles_labels()
    handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]

    ax.legend(handles, labels,frameon=True,prop={'size': size})

def savefig(name, dpi=300, scale = 0.7):
    plt.savefig(name,dpi = dpi)
    print('Datei gespeichert')

    with open('data.tex','a') as file:
        figure = '\\begin{figure}\n    \\centering\n    \includegraphics'+f'[width={scale}\linewidth]'+'{'+name+'}\n\\end{figure}\n'
        file.write(figure)
