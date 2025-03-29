import matplotlib
import matplotlib.pyplot as plt
import colorsys
import pandas as pd
from enum import Enum

class Charter:
    def __init__(self):
        pass

    class DarkTheme(Enum):
        CHART_BACKGROUND_COLOR = '#292929'
        PLOT_AREA_BACKGROUND_COLOR = '#222222'
        PLOT_AREA_BORDER_COLOR = '#353535'
        GRID_COLOR = False
        
        TICK_COLOR = '#555555'
        TICK_LABEL_COLOR = '#bbbbbb'
        
        BAR_COLOR = 'steelblue'
        # BAR_BORDER_COLOR = '#353535'
        LINE_COLOR = 'steelblue'

        TITLE_COLOR = 'white'
        TEXT_COLOR = 'white'
        AXES_LABEL_COLOR = 'white'
        AXES_TITLE_COLOR = 'white'

    class LightTheme(Enum):
        CHART_BACKGROUND_COLOR = '#dddddd'
        PLOT_AREA_BACKGROUND_COLOR = '#bcbcbc'
        PLOT_AREA_BORDER_COLOR = '#9a9a9a'
        GRID_COLOR = False

        TICK_COLOR = '#cccccc'
        TICK_LABEL_COLOR = '#262626'

        BAR_COLOR = 'steelblue'
        # BAR_BORDER_COLOR = '#666666'
        LINE_COLOR = 'steelblue'

        TITLE_COLOR = 'black'
        TEXT_COLOR = 'black'
        AXES_LABEL_COLOR = 'black'
        AXES_TITLE_COLOR = 'black'

    THEMES = {
        'dark': DarkTheme,
        'light': LightTheme
        }


    # -----------------------------------------------------------------------------------------------

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


    # -----------------------------------------------------------------------------------------------

    def shift_color_lightness(self,color,lightness_multiplier):
        rgb = matplotlib.colors.ColorConverter.to_rgb(color)
        h, l, s = colorsys.rgb_to_hls(*rgb)
        r, g, b = colorsys.hls_to_rgb(h, min(1, l * lightness_multiplier), s)
        return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"

    def set_theme(self,fig,theme_config):

        cf = theme_config
        ax = plt.gca()

        fig.patch.set_facecolor(cf.CHART_BACKGROUND_COLOR.value)
        ax.set_facecolor(cf.PLOT_AREA_BACKGROUND_COLOR.value)

        ax.spines['top'].set_color(cf.PLOT_AREA_BORDER_COLOR.value)
        ax.spines['right'].set_color(cf.PLOT_AREA_BORDER_COLOR.value)
        ax.spines['bottom'].set_color(cf.PLOT_AREA_BORDER_COLOR.value)
        ax.spines['left'].set_color(cf.PLOT_AREA_BORDER_COLOR.value)

        ax.grid(False) 

        ax.tick_params(axis='x', colors=cf.TICK_COLOR.value)
        ax.tick_params(axis='y', colors=cf.TICK_COLOR.value)

        for label in ax.get_xticklabels():
            label.set_color(cf.TICK_LABEL_COLOR.value)

        for label in ax.get_yticklabels():
            label.set_color(cf.TICK_LABEL_COLOR.value)

        ax.title.set_color(cf.TITLE_COLOR.value)

        ax.xaxis.label.set_color(cf.AXES_LABEL_COLOR.value)
        ax.yaxis.label.set_color(cf.AXES_LABEL_COLOR.value)

    # -----------------------------------------------------------------------------------------------

    def hist(self,
            x: int | list | pd.Series,
            w: int | float = 6.0,
            h: int | float = 2.0,
            orientation: str = 'vertical',
            bins: int = 50,
            theme: str = 'dark',
            color: str | list | dict = None,
            edgecolor: str = None,
            minx: float = None,
            maxx: float = None,
            miny: float = None,
            maxy: float = None,
            title: str = None,
            **kwargs):

        cf = self.THEMES[theme]
        processed_args = {}  

        if color is None:
            processed_args['color'] = cf.BAR_COLOR.value
        else:
            try:
                color = plt.get_cmap(color).colors
            except:
                processed_args['color'] = color

        if edgecolor is None: processed_args['edgecolor'] = self.shift_color_lightness(cf.BAR_COLOR.value,0.75)
        else: processed_args['edgecolor'] = edgecolor

        fig=plt.figure(figsize=(w,h))
        plt.hist(x=x.dropna().values,
                 bins=bins,
                 orientation=orientation,
                 **processed_args,
                 **kwargs);

        self.set_minx_maxx(minx,maxx)
        self.set_miny_maxy(miny,maxy)
        
        if orientation == 'horizontal':
            plt.xlabel('count')
            try: xname = x.name
            except: xname=None
            if xname is not None: plt.ylabel(x.name)
        else:
            plt.ylabel('count')
            try: xname = x.name
            except: xname=None
            if xname is not None: plt.xlabel(x.name)
        
        if title is None:
            if type(x) == pd.Series:
                title = f'Histogram of "{x.name}"'
        plt.title(title)

        self.set_theme(fig,cf)

        plt.show()


    # -----------------------------------------------------------------------------------------------

    def bar(self,
            x: int | list | pd.Series,
            y: int | list | pd.Series,
            w: int | float = 6.0,
            h: int | float = 2.0,
            orientation: str = 'vertical',
            theme: str = 'dark',
            color: str | list | dict = None,
            other_color: str = None,
            edgecolor: str = None,   
            bar_width: int | float = 0.85,    
            order: str | list = None,
            x_labels_angle: int | float = 0,
            y_labels_angle: int | float = 0,
            miny: float = None,
            maxy: float = None,
            title: str = None,
            **kwargs):

        cf = self.THEMES[theme]
        processed_args = {}     

        if color is None: 
            processed_args['color'] = cf.BAR_COLOR.value
        else:
            if type(color) == dict: # color mapping dict by name
                x_colors = []
                for name in x:
                    if name in color: x_colors.append(color[name])
                    else: 
                        if other_color is None: x_colors.append(cf.BAR_COLOR.value)
                        else: x_colors.append(other_color)
                processed_args['color'] = x_colors
            else:
                try:
                    color = plt.get_cmap(color).colors # check if a palette name
                    processed_args['color']
                except:
                    processed_args['color'] = color # pass as is, could be a simple color for all element or a custom list of colors

        if edgecolor is None: processed_args['edgecolor'] = None
        else: processed_args['edgecolor'] = edgecolor

        fig=plt.figure(figsize=(w,h))
        plt.bar(x=x,
                height=y, 
                width=bar_width,
                **processed_args, 
                **kwargs);        
        
        self.set_miny_maxy(miny,maxy)

        plt.xticks(rotation=x_labels_angle)
        plt.yticks(rotation=y_labels_angle)

        try: xname = x.name
        except: xname=None
        if xname is not None: plt.xlabel(x.name)
        
        try: yname = y.name
        except: yname=None
        if yname is not None: plt.ylabel(y.name)            

        if title is None:
            if xname is not None and yname is not None:
                title = f'{y.name} by "{x.name}"'
        plt.title(title)

        self.set_theme(fig,cf)

        plt.show()

   # -----------------------------------------------------------------------------------------------

    def barh(self,
            x: int | list | pd.Series,
            y: int | list | pd.Series,
            w: int | float = 6.0,
            h: int | float = 2.0,
            theme: str = 'dark',
            color: str | list | dict = None,
            edgecolor: str = None,   
            bar_width: int | float = 0.85,    
            x_labels_angle: int | float = 0,
            y_labels_angle: int | float = 0,
            miny: float = None,
            maxy: float = None,
            title: str = None,
            **kwargs):

        cf = self.THEMES[theme]
        processed_args = {}     

        if color is None: 
            processed_args['color'] = cf.BAR_COLOR.value
        else:
            if type(color) == dict: # color mapping dict by name
                x_colors = []
                for name in x:
                    if name in color: x_colors.append(color[name])
                    else: x_colors.append(cf.BAR_COLOR.value)
                processed_args['color'] = x_colors
            else:
                try:
                    color = plt.get_cmap(color).colors # check if a palette name
                    processed_args['color']
                except:
                    processed_args['color'] = color # pass as is, could be a simple color for all element or a custom list of colors

        if edgecolor is None: processed_args['edgecolor'] = None
        else: processed_args['edgecolor'] = edgecolor

        fig=plt.figure(figsize=(w,h))
        plt.barh(y=y,
                width=x, 
                height=bar_width,
                **processed_args, 
                **kwargs);        
        
        self.set_minx_maxx(miny,maxy)

        plt.xticks(rotation=x_labels_angle)
        plt.yticks(rotation=y_labels_angle)

        try: xname = x.name
        except: xname=None
        if xname is not None: plt.xlabel(x.name)
        
        try: yname = y.name
        except: yname=None
        if yname is not None: plt.ylabel(y.name)            

        if title is None:
            if xname is not None and yname is not None:
                title = f'{x.name} by "{y.name}"'
        plt.title(title)

        self.set_theme(fig,cf)     

        plt.show()
           