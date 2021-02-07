import matplotlib
import matplotlib.pyplot as plt
import squarify as sq



class treemap():
    
    def gr_colors(series):
        theme = matplotlib.cm.bwr_r
        cmap = matplotlib.colors.Normalize(vmin=min(series),vmax=max(series))
        return [theme(cmap(v)) for v in series]
    
    
    def draw(size_scale,label,color_scale):
        colors = treemap.gr_colors(color_scale)
        output = sq.plot(sizes=size_scale,label=label,color=colors)
        output.axis('off')
        return output
    
    
    