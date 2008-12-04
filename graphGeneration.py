import matplotlib
import matplotlib.pylab as plt

def generate_projection_graph(name='defaultName', data=[], extension='png'):
    """
         	
        This method creates and saves a graph. In this project, this method is used to represent, in graphic, a projection of an image.
       
        Parameters:
        
        extensions: There are several extensions allowed in this method, 
                    such as emf, eps, pdf, png, ps, raw, rgba, svg, svgz. 
                    Nevertheless, the default extension is png. 
    """
    
    matplotlib.use('Agg')
    figure = plt.figure()
    graph = figure.add_subplot(111)
    graph.plot(data)
    try:
        figure.savefig("%s.%s"%(name,extension))
    except Exception, e:
        print e
        

    
