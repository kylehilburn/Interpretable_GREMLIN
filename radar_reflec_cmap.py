from matplotlib.pyplot import get_cmap
from matplotlib.pyplot import cm
from matplotlib.colors import ListedColormap
from matplotlib.colors import BoundaryNorm

rgb_colors = []

# original: not CVD accessible
#rgb_colors.append((227,227,227))  #0
#rgb_colors.append((76,235,230))   #5
#rgb_colors.append((63,155,242))   #10
#rgb_colors.append((49,0,241))     #15
#rgb_colors.append((66,255,35))     #20
#rgb_colors.append((50,202,25))     #25
#rgb_colors.append((33,146,14))     #30
#rgb_colors.append((249,252,45))     #35
#rgb_colors.append((224,191,35))     #40
#rgb_colors.append((247,148,32))     #45
#rgb_colors.append((243,0,25))     #50
#rgb_colors.append((203,0,19))     #55
#rgb_colors.append((180,0,15))     #60

# new: CVD accessible
rgb_colors.append((231, 231, 231))  #0
rgb_colors.append((111, 239, 255))  #5
rgb_colors.append(( 95, 207, 239))  #10
rgb_colors.append(( 79, 175, 223))  #15
rgb_colors.append(( 47,  95, 191))  #20
rgb_colors.append(( 31,  63, 175))  #25
rgb_colors.append(( 15,  31, 159))  #30
rgb_colors.append((247, 239,  63))  #35
rgb_colors.append((239, 191,  55))  #40
rgb_colors.append((231, 143,  47))  #45
rgb_colors.append((207,  15,  23))  #50
rgb_colors.append((183,   7,  15))  #55
rgb_colors.append((159,   0,   8))  #60

colors = []
for atup in rgb_colors:
    colors.append('#%02x%02x%02x'%atup)

cm.register_cmap(cmap=ListedColormap(colors,'radar'))

cmap = get_cmap('radar')
cmap.set_over(colors[-1])
cmap.set_under(colors[0])

bounds = [0,5,10,15,20,25,30,35,40,45,50,55,60]

ticklabels = [str(a) for a in bounds]

norm = BoundaryNorm(bounds,cmap.N)
