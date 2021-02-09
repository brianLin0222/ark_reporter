import matplotlib
import matplotlib.pyplot as plt
import squarify as sq



class treemap():
    
    def gr_colors(series):
        #this will not generate a correct treemap when there is an outlier in the portfolio
        #(a stock either greatly outperform or underperform compare to its peers)
        # theme = matplotlib.cm.bwr_r
        
        gtheme = matplotlib.cm.Blues
        rtheme = matplotlib.cm.autumn
        
        g_cmap = matplotlib.colors.Normalize(vmin=0,vmax=max(series))
        r_cmap = matplotlib.colors.Normalize(vmin=min(series),vmax=0)
        rgb_vec = [gtheme(g_cmap(v)) if v>0 else rtheme(r_cmap(v)) for v in series]
        return rgb_vec
    
    
    def draw(size_scale,label,color_scale):
        colors = treemap.gr_colors(color_scale)
        output = sq.plot(sizes=size_scale,label=label,color=colors)
        output.axis('off')
        return output
    
    
    