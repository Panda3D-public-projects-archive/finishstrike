import os
from matplotlib import pylab

def generateGraph(path = '.', name='defaultName', data=[], ponto = ([0],[0]), extension='png'):
    """
        This method creates and saves a graph. In this project, this
        method is used to represent, in graphic, a projection of an image.
       
        Parameters:
        
        extensions: There are several extensions allowed in this method, 
                    such as emf, eps, pdf, png, ps, raw, rgba, svg, svgz. 
                    Nevertheless, the default extension is png. 
    """
    
    figure = pylab.figure()
    graph = figure.add_subplot(111)
    graph.plot(data)
    pylab.scatter(ponto[0], ponto[1], c=[60]*len(ponto[0]), s=12, alpha = 0.75)
    try:
        figure.savefig(os.path.join(path, name))
    except Exception, e:
        print e
