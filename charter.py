import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from enum import Enum

class DarkTheme(Enum):
    BAR_COLOR = 'steelblue'
    LINE_COLOR = 'steelblue'

    TEXT_COLOR = 'white'
    AXES_LABELCOLOR = 'white'
    XTICK_COLOR = 'white'
    YTICK_COLOR = 'white'
    AXES_TITLECOLOR = 'white'

class LightTheme(Enum):
    BAR_COLOR = 'steelblue'
    LINE_COLOR = 'steelblue'

    TEXT_COLOR = 'black'
    AXES_LABELCOLOR = 'black'
    XTICK_COLOR = 'black'
    YTICK_COLOR = 'black'
    AXES_TITLECOLOR = 'black'

THEMES = {
    'dark': DarkTheme,
    'light': LightTheme
    }

theme = 'dark'

c = THEMES[theme]

print(c.BAR_COLOR.value)


class Charter:
    def __init__(self):
        pass
    
    def set_minx_maxx(self,minx,maxx):
        if minx is not None or maxx is not None:
            minx_input, maxx_input = plt.xlim()
            minx_wrong = False
            maxx_wrong = False
            if minx is not None:
                if type(minx) in [int,float]:
                    minx_input = minx
                else: 
                    minx_wrong = True
                    print('Chartert WARNING: Passed "minx" not used because not a number!')
            if maxx is not None:
                if type(maxx) in [int,float]:
                    maxx_input = maxx 
                else: 
                    maxx_wrong = True
                    print('Chartert WARNING: Passed "maxx" not used because not a number!')
            if not minx_wrong and not maxx_wrong:
                if minx_input < maxx_input:
                    plt.xlim((minx_input,maxx_input))
                else:
                    print('Chartert WARNING: Passed minx and/or maxx is not used beacuse minx > maxx !')   

    def set_miny_maxy(self,miny,maxy):
        if miny is not None or maxy is not None:
            miny_input, maxy_input = plt.ylim()
            miny_wrong = False
            maxy_wrong = False
            if miny is not None:
                if type(miny) in [int,float]:
                    miny_input = miny
                else: 
                    miny_wrong = True
                    print('Chartert WARNING: Passed "miny" not used because not a number!')
            if maxy is not None:
                if type(maxy) in [int,float]:
                    maxy_input = maxy 
                else: 
                    maxy_wrong = True
                    print('Chartert WARNING: Passed "maxy" not used because not a number!')
            if not miny_wrong and not maxy_wrong:
                if miny_input < maxy_input:
                    plt.ylim((miny_input,maxy_input))
                else:
                    print('Chartert WARNING: Passed miny and/or maxy is not used beacuse miny > maxy !')   

    def hist(self,
            x: int | list = [],
            w: int | float = 6.0,
            h: int | float = 2.0,
            bins: int = 50,
            color: str | list | dict = None,
            minx: float = None, maxx: float = None,
            miny: float = None, maxy: float = None,
            title: str = None,
            **kwargs):

        plt.rcParams.update({
            'text.color': '#000000',
            'axes.labelcolor': '#000000',
            'xtick.color': '#000000',
            'ytick.color': '#000000',
            'axes.titlecolor': '#000000'
        })

        processed_args = {}  

        if color is None:
            processed_args['color'] = default_bar_color
        else:
            try:
                color = plt.get_cmap(color).colors
            except:
                processed_args['color'] = color

        fig=plt.figure(figsize=(w,h))
        plt.hist(x=x.dropna().values,bins=bins, **processed_args, **kwargs);

        self.set_minx_maxx(minx,maxx)
        self.set_miny_maxy(miny,maxy)
    
        plt.ylabel('count')
        
        try: xname = x.name
        except: xname=None
        if xname is not None: plt.xlabel(x.name)

        if title is None:
            if type(x) == pd.Series:
                title = f'Histogram of "{x.name}"'
        plt.title(title)
   

    def bar(self,
            x: int | list = [],
            y: int | list = [],
            w: int | float = 6.0,
            h: int | float = 2.0,
            x_labels_angle: int | float = 0,
            bar_width: int | float = 0.85,            
            color: str | list | dict = None,
            miny: float = None, maxy: float = None,
            title: str = None,
            **kwargs):

        processed_args = {}      

        if color is None: 
            processed_args['color'] = default_bar_color
        else:
            if type(color) == dict: # color mapping dict by name
                x_colors = []
                for name in x:
                    if name in color: x_colors.append(color[name])
                    else: x_colors.append(default_bar_color)
                processed_args['color'] = x_colors
            else:
                try:
                    color = plt.get_cmap(color).colors # check if a palette name
                    processed_args['color']
                except:
                    processed_args['color'] = color # pass as is, could be a simple color for all element or a custom list of colors


        plt.rcParams.update({
            'text.color': 'white',
            'axes.labelcolor': 'white',
            'xtick.color': 'white',
            'ytick.color': 'white',
            'axes.titlecolor': 'white'
        })

        fig=plt.figure(figsize=(w,h),facecolor='#282828')
        plt.bar(x=x, height=y, width=bar_width, **processed_args, **kwargs);        

        self.set_miny_maxy(miny,maxy)

        plt.xticks(rotation=x_labels_angle)

        try: xname = x.name
        except: xname=None
        if xname is not None: plt.xlabel(x.name)

        try: yname = y.name
        except: yname=None
        if yname is not None: plt.xlabel(x.name)
 
        if title is None:
            if xname is not None and yname is not None:
                title = f'"{y.name}" by "{x.name}"'
        plt.title(title)

        ax = plt.gca()

        # Set the background color of the plot area
        ax.set_facecolor('#252525')

        ax.grid(color='#252525') 

        # Set the border color of the plot area
        ax.spines['top'].set_color('#444444')
        ax.spines['right'].set_color('#444444')
        ax.spines['bottom'].set_color('#444444')
        ax.spines['left'].set_color('#444444')

        # Set the color of the ticks
        ax.tick_params(axis='x', colors='#888888')
        ax.tick_params(axis='y', colors='#888888')

        # Set the color of the tick labels separately
        for label in ax.get_xticklabels():
            label.set_color('white')  # Change x-axis tick label color to yellow

        for label in ax.get_yticklabels():
            label.set_color('white')  # Change y-axis tick label color to yellow

        # Set the color of the tick labels
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')

        # Set the color of the title
        ax.title.set_color('white')

        # Set the color of the grid lines
        # ax.grid(color='#252525') 
        ax.grid(False) 

        plt.rcParams.update({
            'text.color': 'white',
            'axes.labelcolor': 'white',
            'xtick.color': 'white',
            'ytick.color': 'white',
            'axes.titlecolor': 'white'
        })

