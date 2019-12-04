#!/usr/bin/env python


# Code from http://www.mit.edu/~iancross/python/kdestats.html,
# written by Ian J. M. Crossfield


from scipy.stats import gaussian_kde
import numpy as np
def confmap(map, frac, **kw):
    """Return the confidence level of a 2D histogram or array that
    encloses the specified fraction of the total sum.

    :INPUTS:
      map : 1D or 2D numpy array
        Probability map (from hist2d or kde)

      frac : float, 0 <= frac <= 1
        desired fraction of enclosed energy of map

    :OPTIONS:
      ordinate : None or 1D array
        If 1D map, interpolates onto the desired value.  This could
        cause problems when you aren't just setting upper/lower
        limits....
    """
    # 2010-07-26 12:54 IJC: Created
    # 2011-11-05 14:29 IJMC: Fixed so it actually does what it's supposed to!
    from scipy.optimize import bisect

    def diffsum(level, map, ndesired):
        return ((1.0*map[map >= level].sum()/map.sum() - ndesired))

    if hasattr(frac,'__iter__'):
        return [confmap(map,thisfrac, **kw) for thisfrac in frac]

    #nx, ny = map.shape
    #ntot = map.size
    #n = int(ntot*frac)

    #guess = map.max()
    #dx = 10.*float((guess-map.min())/ntot)
    #thisn = map[map<=guess].sum()

    ret = bisect(diffsum, map.min(), map.max(), args=(map, frac))
    if kw.has_key('ordinate') and kw['ordinate'] is not None:
        sortind = np.argsort(map)
        ret = np.interp(ret, map[sortind], kw['ordinate'][sortind])

    return ret


def kdehist2(x, y, npts, xrange=None, yrange=None):
    """Generate a 2D histogram map from data, using Gaussian KDEs

    :INPUTS:
      x : seq
        X data

      y : seq
        Y data

      npts : int or 2-seq
        number of points across final histogram, or [nx, ny]

    :OPTIONAL_INPUTS:
      xrange : 2-seq
        [x_min, x_max] values for final histogram

      yrange : 2-seq
        [y_min, y_max] values for final histogram
        
    :RETURNS:
      [kdehist, xbins, ybins]

    :EXAMPLE:
      ::
 
        import kdestats as kde
        import numpy as np
        import pylab as py

        covmat = [[1., 1.5], [1.5, 4.]]
        xy = np.random.multivariate_normal([0, 0], covmat, [1e4])
        kdehist = kde.kdehist2(xy[:,0], xy[:,1], [30, 30])
        clevels = kde.confmap(kdehist[0], [.6827,.9545,.9973])

        py.figure()  # Plot 1-, 2-, and 3-sigma contours
        c = py.contour(kdehist[1], kdehist[2], kdehist[0], clevels)
    """
    # 2012-02-11 19:45 IJMC: Created

    if hasattr(npts, '__iter__'):
        if len(npts)==1:
            npts = [npts[0], npts[1]]
    else:
        npts = [npts, npts]

    # Generate KDE:
    thiskde = gaussian_kde([x, y])

    # Generate coordinates for KDE evaluation:
    if xrange is None:
        thisx0 = np.median(thiskde.dataset[0])
        thisdx0 = np.std(thiskde.dataset[0])
        thisx = np.linspace(-5*thisdx0,5*thisdx0,npts[0])+thisx0
    else:
        thisx = np.linspace(xrange[0], xrange[1], npts[0])

    if yrange is None:
        thisy0 = np.median(thiskde.dataset[1])
        thisdy0 = np.std(thiskde.dataset[1])
        thisy = np.linspace(-5*thisdy0,5*thisdy0,npts[1])+thisy0
    else:
        thisy = np.linspace(yrange[0], yrange[1], npts[1])

    thisxx,thisyy = np.meshgrid(thisx,thisy)
    
    thishist = thiskde([thisxx.ravel(),thisyy.ravel()]).reshape(npts[0],npts[0])

    return thishist, thisx, thisy