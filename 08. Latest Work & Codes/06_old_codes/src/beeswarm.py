"""
The MIT License (MIT)

Copyright (c) 2014 Melissa Gymrek <mgymrek@mit.edu>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import itertools
import math
import matplotlib.pyplot
import numpy
import pandas
import sys

def beeswarm(values, positions=None, method="swarm",
             ax=None, s=20, col="black", xlim=None, ylim=None,
             labels=None, labelrotation="vertical", **kwargs):
    """
    beeswarm(values, positions=None, method="swarm",
         ax=None, s=20, col="black", xlim=None, ylim=None,
         labels=None)

     Inputs:
         * values: an array of a sequence of vectors
         * positions: sets the horizontal positions of the swarms.
            Ticks and labels are set to match the positions.
            If none, set positions to range(len(values))
            Default: None
         * method: how to jitter the x coordinates. Choose from
            "swarm", "hex", "center", "square"
            Default: swarm
         * ax: use this axis for plotting. If none supplied, make a new one
            Default: None
         * s: size of points in points^2 (assuming 72 points/inch).
            Defautt: 20
         * col: color of points. Can be:
            - a single string: color all points that color
            - a vector of strings length len(values): gives color for each group
            - a vector of strings length sum([len(values[i]) for i in range(len(values))])
                 gives color for each point
            - a vector of strings any other length: cycle through the list of colors.
                 (really pretty if not useful)
            Default: "black"
            Note, colors can also be rgb tubples instead of strings.
         * xlim: tuple giving (xmin, xmax). If not specified, either get
             from the supplied ax or recalculate
         * ylim: tuple giving (ymin, ymax). If not specified, eiterh get
             from the supplied as or recalculate
         * labels: list of labels for each group.
             Default: range(len(values))
         * labelrotation: rotation of x label.
             Default: "vertical"

     Returns:
         * bs: pandas.DataFrame with columns: xorig, yorig, xnew, ynew, color
         * ax: the axis used for plotting
    """
    # Check things before we go on
    if method not in ["swarm", "hex", "center", "square"]:
        sys.stderr.write("ERROR: Invalid method.\n")
        return
    if len(values) == 0: return None
    if not hasattr(values[0], "__len__"): values = [values]
    if positions is None:
        positions = range(len(values))
    else:
        if len(positions) != len(values):
            sys.stderr.write("ERROR: number of positions must match number of groups\n")
            return None

    

    yvals = list(itertools.chain.from_iterable(values))
    xvals = list(itertools.chain.from_iterable([[positions[i]]*len(values[i]) for i in range(len(values))]))

    # Get color vector
    if type(col) == str:
        colors = [[col]*len(values[i]) for i in range(len(values))]
    elif type(col) == list:
        if len(col) == len(positions):
            colors = []
            for i in range(len(col)):
                colors.append([col[i]]*len(values[i]))
        elif len(col) == len(yvals):
            colors = []
            sofar = 0
            for i in range(len(values)):
                colors.append(col[sofar:(sofar+len(values[i]))])
                sofar = sofar + len(values[i])
        else:
            cx = col*(len(yvals)/len(col)) # hope for the best
            if len(cx) < len(yvals):
                cx.extend(col[0:(len(yvals)-len(cx))])
            colors = []
            sofar = 0
            for i in range(len(values)):
                colors.append(cx[sofar:(sofar+len(values[i]))])
                sofar = sofar + len(values[i])
    else:
        sys.stderr.write("ERROR: Invalid argument for col\n")
        return

    # Get axis limits
    if ax is None:
        fig = matplotlib.pyplot.figure()
        ax = fig.add_subplot(111)
    if xlim is not None:
        ax.set_xlim(left=xlim[0], right=xlim[1])
    else:
        xx = max(positions) - min(positions) + 1
        xmin = min(positions)-0.1*xx
        xmax = max(positions)+0.1*xx
        ax.set_xlim(left=xmin, right=xmax)
    if ylim is not None:
        ax.set_ylim(bottom=ylim[0], top=ylim[1])
    else:
        yy = max(yvals) - min(yvals)
        ymin = min(yvals)-.05*yy
        ymax = max(yvals)+0.05*yy
        ax.set_ylim(bottom=ymin, top=ymax)

    # Determine dot size
    figw, figh = ax.get_figure().get_size_inches()
    w = (ax.get_position().xmax-ax.get_position().xmin)*figw
    h = (ax.get_position().ymax-ax.get_position().ymin)*figh
    xran = ax.get_xlim()[1]-ax.get_xlim()[0]
    yran = ax.get_ylim()[1]-ax.get_ylim()[0]
    xsize=math.sqrt(s)*1.0/72*xran*1.0/(w*0.8)
    ysize=math.sqrt(s)*1.0/72*yran*1.0/(h*0.8)

    # Get new arrangements
    if method == "swarm":
        bs = _beeswarm(positions, values, xsize=xsize, ysize=ysize, method="swarm", colors=colors)
    else:
        bs = _beeswarm(positions, values, ylim=ax.get_ylim(), xsize=xsize, ysize=ysize, method=method, colors=colors)
    matplotlib.pyplot.close()
    return bs
    # plot
    # ax.scatter(bs["xnew"], bs["ynew"], c=list(bs["color"]), **kwargs)
    # ax.set_xticks(positions)
    # if labels is not None:
    #     ax.set_xticklabels(labels, rotation=labelrotation)
    # return bs, ax

def unsplit(x,f):
    """
    same as R's unsplit function
    Read of the values specified in f from x to a vector

    Inputs:
      x: dictionary of value->[items]
      f: vector specifying values to be read off to the vector
    """
    y = pandas.DataFrame({"y":[None]*len(f)})
    f = pandas.Series(f)
    for item in set(f):
        y.loc[f==item,"y"] = x[item]
    return y["y"]

def grid(x, ylim, xsize=0, ysize=0, method="hex", colors="black"):
    """
    Implement the non-swarm arrangement methods
    """
    size_d = ysize
    if method == "hex": size_d = size_d*math.sqrt(3)/2
    size_g = xsize
    breaks = numpy.arange(ylim[0], ylim[1]+size_d, size_d)
    mids = (pandas.Series(breaks[:-1]) + pandas.Series(breaks[1:]))*1.0/2
    d_index = pandas.Series(pandas.cut(pandas.Series(x), bins=breaks, labels=False))
    d_pos = d_index.apply(lambda x: mids[x])
    v_s = {}
    for item in set(d_index):
        odd_row = (item%2)==1
        vals = range(list(d_index).count(item))
        if method == "center":
            v_s[item] = list(map(lambda a: a - numpy.mean(vals), vals))
        elif method == "square":
            v_s[item] = list(map(lambda a: a - math.floor(numpy.mean(vals)), vals))
        elif method == "hex":
            if odd_row:
                v_s[item] = list(map(lambda a: a - math.floor(numpy.mean(vals)) - 0.25, vals))
            else:
                v_s[item] = list(map(lambda a: a - math.ceil(numpy.mean(vals)) + 0.25, vals))
        else:
            sys.stderr.write("ERROR: this block should never execute.\n")
            return
    x_index = unsplit(v_s, d_index)
    if type(colors) == str: colors = [colors]*len(x_index)
    return x_index.apply(lambda x: x*size_g), d_pos, colors

def swarm(x, xsize=0, ysize=0, colors="black"):
    """
    Implement the swarm arrangement method
    """
    gsize = xsize
    dsize = ysize
    out = pandas.DataFrame({"x": [item*1.0/dsize for item in x], "y": [0]*len(x), "color": colors, "order": range(len(x))})
    out.sort_values(by='x', inplace=True)
    if out.shape[0] > 1:
        for i in range(1, out.shape[0]):
            xi = out["x"].values[i]
            yi = out["y"].values[i]
            pre =  out[0:i] # previous points
            wh = (abs(xi-pre["x"]) < 1) # which are potentially overlapping
            if any(wh):
                pre = pre[wh]
                poty_off = pre["x"].apply(lambda x: math.sqrt(1-(xi-x)**2)) # potential y offset
                poty = pandas.Series([0] + (pre["y"] + poty_off).tolist() + (pre["y"]-poty_off).tolist()) # potential y values
                poty_bad = []
                for y in poty:
                    dists = (xi-pre["x"])**2 + (y-pre["y"])**2
                    if any([item < 0.999 for item in dists]): poty_bad.append(True)
                    else: poty_bad.append(False)
                poty[poty_bad] = numpy.infty
                abs_poty = [abs(item) for item in poty]
                newoffset = poty[abs_poty.index(min(abs_poty))]
                out.loc[i,"y"] = newoffset
            else:
                out.loc[i,"y"] = 0
    out.loc[numpy.isnan(out["x"]), "y"] = numpy.nan
    # Sort to maintain original order
    out.sort_values(by="order", inplace=True)
    return out["y"]*gsize, out["color"]

def _beeswarm(positions, values, xsize=0, ysize=0, ylim=None, method="swarm", colors="black"):
    """
    Call the appropriate arrangement method
    """
    xnew = []
    ynew = []
    xorig = []
    yorig = []
    newcolors = []
    # group y by X
    for i in range(len(positions)):
        xval = positions[i]
        ys = values[i]
        cs = colors[i]
        if method == "swarm":
            g_offset, ncs = swarm(ys, xsize=xsize, ysize=ysize, colors=cs)
            ynew.extend(ys)
        else:
            g_offset, new_values, ncs = grid(ys, xsize=xsize, ysize=ysize, ylim=ylim, method=method, colors=cs)
            ynew.extend(new_values)
        xnew.extend([xval+item for item in g_offset])
        yorig.extend(ys)
        xorig.extend([xval]*len(ys))
        newcolors.extend(ncs)
    out = pandas.DataFrame({"xnew":xnew, "yorig": yorig, "xorig":xorig, "ynew": ynew, "color": newcolors})
    return out