import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
# Okabe-Ito: colour-vision-deficiency safe by construction, fixed order, never cycled
BLUE='#0072B2'; VERM='#D55E00'; GREEN='#009E73'; PURPLE='#CC79A7'; ORANGE='#E69F00'; SKY='#56B4E9'
INK='#1A1A1A'; MUTED='#5A5A5A'; GRID='#D9D9D9'
ORDER=[BLUE,VERM,GREEN,PURPLE,ORANGE,SKY]
plt.rcParams.update({
 'font.family':'DejaVu Sans','font.size':8,'axes.labelsize':8,'axes.titlesize':8.5,
 'xtick.labelsize':7.5,'ytick.labelsize':7.5,'legend.fontsize':7.5,
 'axes.edgecolor':MUTED,'axes.linewidth':0.7,'axes.labelcolor':INK,
 'xtick.color':MUTED,'ytick.color':MUTED,'text.color':INK,
 'axes.grid':True,'grid.color':GRID,'grid.linewidth':0.5,'grid.alpha':0.9,
 'axes.axisbelow':True,'figure.dpi':160,'savefig.dpi':600,'savefig.bbox':'tight',
 'legend.frameon':False,'axes.spines.top':False,'axes.spines.right':False})
def panel(ax,letter):
    ax.text(-0.14,1.06,f'({letter})',transform=ax.transAxes,fontsize=9,fontweight='bold',va='bottom',ha='left')
def save(fig,name):
    for ext in ('png','pdf'): fig.savefig(f'{name}.{ext}')
    plt.close(fig); print('saved',name)
