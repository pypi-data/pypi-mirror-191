from __future__ import print_function, division

from ... import Integer
from ...core.compatibility import is_sequence

from threading import RLock

# it is sufficient to import "pyglet" here once
try:
    from pyglet.gl import *
except ImportError:
    raise ImportError("pyglet is required for plotting.\n "
                      "visit http://www.pyglet.org/")

from plot_object import PlotObject
from plot_axes import PlotAxes
from plot_window import PlotWindow
from plot_mode import PlotMode

from time import sleep
from os import getcwd, listdir
from util import parse_option_string

from ...geometry.entity import GeometryEntity

from ...utilities.decorator import doctest_depends_on

@doctest_depends_on(modules=('pyglet',))
class PygletPlot(object):
    """
    Plot Examples
    =============

    See examples/advaned/pyglet_plotting.py for many more examples.


    >>> from ..pygletplot import PygletPlot as Plot
    >>> from ...abc import x, y, z

    >>> Plot(x*y**3-y*x**3)
    [0]: -x**3*y + x*y**3, 'mode=cartesian'

    >>> p = Plot()
    >>> p[1] = x*y
    >>> p[1].color = z, (0.4,0.4,0.9), (0.9,0.4,0.4)

    >>> p = Plot()
    >>> p[1] =  x**2+y**2
    >>> p[2] = -x**2-y**2


    Variable Intervals
    ==================

    The basic format is [var, min, max, steps], but the
    syntax is flexible and arguments left out are taken
    from the defaults for the current coordinate mode:

    >>> Plot(x**2) # implies [x,-5,5,100]
    [0]: x**2, 'mode=cartesian'
    >>> Plot(x**2, [], []) # [x,-1,1,40], [y,-1,1,40]
    [0]: x**2, 'mode=cartesian'
    >>> Plot(x**2-y**2, [100], [100]) # [x,-1,1,100], [y,-1,1,100]
    [0]: x**2 - y**2, 'mode=cartesian'
    >>> Plot(x**2, [x,-13,13,100])
    [0]: x**2, 'mode=cartesian'
    >>> Plot(x**2, [-13,13]) # [x,-13,13,100]
    [0]: x**2, 'mode=cartesian'
    >>> Plot(x**2, [x,-13,13]) # [x,-13,13,10]
    [0]: x**2, 'mode=cartesian'
    >>> Plot(1*x, [], [x], mode='cylindrical')
    ... # [unbound_theta,0,2*Pi,40], [x,-1,1,20]
    [0]: x, 'mode=cartesian'


    Coordinate Modes
    ================

    Plot supports several curvilinear coordinate modes, and
    they independent for each plotted function. You can specify
    a coordinate mode explicitly with the 'mode' named argument,
    but it can be automatically determined for Cartesian or
    parametric plots, and therefore must only be specified for
    polar, cylindrical, and spherical modes.

    Specifically, Plot(function arguments) and Plot[n] =
    (function arguments) will interpret your arguments as a
    Cartesian plot if you provide one function and a parametric
    plot if you provide two or three functions. Similarly, the
    arguments will be interpreted as a curve if one variable is
    used, and a surface if two are used.

    Supported mode names by number of variables:

    1: parametric, cartesian, polar
    2: parametric, cartesian, cylindrical = polar, spherical

    >>> Plot(1, mode='spherical') # doctest: +SKIP


    Calculator-like Interface
    =========================

    >>> p = Plot(visible=False)
    >>> f = x**2
    >>> p[1] = f
    >>> p[2] = f.diff(x)
    >>> p[3] = f.diff(x).diff(x) # doctest: +SKIP
    >>> p # doctest: +SKIP
    [1]: x**2, 'mode=cartesian'
    [2]: 2*x, 'mode=cartesian'
    [3]: 2, 'mode=cartesian'
    >>> p.show()
    >>> p.clear()
    >>> p
    <blank plot>
    >>> p[1] =  x**2+y**2
    >>> p[1].style = 'solid'
    >>> p[2] = -x**2-y**2
    >>> p[2].style = 'wireframe'
    >>> p[1].color = z, (0.4,0.4,0.9), (0.9,0.4,0.4)
    >>> p[1].style = 'both'
    >>> p[2].style = 'both'
    >>> p.close()


    Plot Window Keyboard Controls
    =============================

    Screen Rotation:
        X,Y axis      Arrow Keys, A,S,D,W, Numpad 4,6,8,2
        Z axis        Q,E, Numpad 7,9

    Model Rotation:
        Z axis        Z,C, Numpad 1,3

    Zoom:             R,F, PgUp,PgDn, Numpad +,-

    Reset Camera:     X, Numpad 5

    Camera Presets:
        XY            F1
        XZ            F2
        YZ            F3
        Perspective   F4

    Sensitivity Modifier: SHIFT

    Axes Toggle:
        Visible       F5
        Colors        F6

    Close Window:     ESCAPE

    =============================

    """

    @doctest_depends_on(modules=('pyglet',))
    def __init__(self, *fargs, **win_args):
        """
        Positional Arguments
        ====================

        Any given positional arguments are used to
        initialize a plot function at index 1. In
        other words...

        >>> from ..pygletplot import PygletPlot as Plot
        >>> from ...core import Symbol
        >>> from ...abc import x
        >>> p = Plot(x**2, visible=False)

        ...is equivalent to...

        >>> p = Plot(visible=False)
        >>> p[1] = x**2

        Note that in earlier versions of the plotting
        module, you were able to specify multiple
        functions in the initializer. This functionality
        has been dropped in favor of better automatic
        plot plot_mode detection.


        Named Arguments
        ===============

        axes
            An option string of the form
            "key1=value1; key2 = value2" which
            can use the following options:

            style = ordinate
                none OR frame OR box OR ordinate

            stride = 0.25
                val OR (val_x, val_y, val_z)

            overlay = True (draw on top of plot)
                True OR False

            colored = False (False uses Black,
                             True uses colors
                             R,G,B = X,Y,Z)
                True OR False

            label_axes = False (display axis names
                                at endpoints)
                True OR False

        visible = True (show immediately
            True OR False


        The following named arguments are passed as
        arguments to window initialization:

        antialiasing = True
            True OR False

        ortho = False
            True OR False

        invert_mouse_zoom = False
            True OR False

        """
        self._win_args = win_args
        self._window = None

        self._render_lock = RLock()

        self._functions = {}
        self._pobjects = []
        self._screenshot = ScreenShot(self)

        axe_options = parse_option_string(win_args.pop('axes', ''))
        self.axes = PlotAxes(**axe_options)
        self._pobjects.append(self.axes)

        self[0] = fargs
        if win_args.get('visible', True):
            self.show()

    ## Window Interfaces

    def show(self):
        """
        Creates and displays a plot window, or activates it
        (gives it focus) if it has already been created.
        """
        if self._window and not self._window.has_exit:
            self._window.activate()
        else:
            self._win_args['visible'] = True
            self.axes.reset_resources()

            if hasattr(self, '_doctest_depends_on'):
                self._win_args['runfromdoctester'] = True

            self._window = PlotWindow(self, **self._win_args)

    def close(self):
        """
        Closes the plot window.
        """
        if self._window:
            self._window.close()

    def saveimage(self, outfile=None, format='', size=(600, 500)):
        """
        Saves a screen capture of the plot window to an
        image file.

        If outfile is given, it can either be a path
        or a file object. Otherwise a png image will
        be saved to the current working directory.
        If the format is omitted, it is determined from
        the filename extension.
        """
        self._screenshot.save(outfile, format, size)

    ## Function List Interfaces

    def clear(self):
        """
        Clears the function list of this plot.
        """
        self._render_lock.acquire()
        self._functions = {}
        self.adjust_all_bounds()
        self._render_lock.release()

    def __getitem__(self, i):
        """
        Returns the function at position i in the
        function list.
        """
        return self._functions[i]

    def __setitem__(self, i, args):
        """
        Parses and adds a PlotMode to the function
        list.
        """
        if not (isinstance(i, (int, Integer)) and i >= 0):
            raise ValueError("Function index must "
                             "be an integer >= 0.")

        if isinstance(args, PlotObject):
            f = args
        else:
            if (not is_sequence(args)) or isinstance(args, GeometryEntity):
                args = [args]
            if len(args) == 0:
                return  # no arguments given
            kwargs = dict(bounds_callback=self.adjust_all_bounds)
            f = PlotMode(*args, **kwargs)

        if f:
            self._render_lock.acquire()
            self._functions[i] = f
            self._render_lock.release()
        else:
            raise ValueError("Failed to parse '%s'."
                    % ', '.join(str(a) for a in args))

    def __delitem__(self, i):
        """
        Removes the function in the function list at
        position i.
        """
        self._render_lock.acquire()
        del self._functions[i]
        self.adjust_all_bounds()
        self._render_lock.release()

    def firstavailableindex(self):
        """
        Returns the first unused index in the function list.
        """
        i = 0
        self._render_lock.acquire()
        while i in self._functions:
            i += 1
        self._render_lock.release()
        return i

    def append(self, *args):
        """
        Parses and adds a PlotMode to the function
        list at the first available index.
        """
        self.__setitem__(self.firstavailableindex(), args)

    def __len__(self):
        """
        Returns the number of functions in the function list.
        """
        return len(self._functions)

    def __iter__(self):
        """
        Allows iteration of the function list.
        """
        return self._functions.itervalues()

    def __repr__(self):
        return str(self)

    def __str__(self):
        """
        Returns a string containing a new-line separated
        list of the functions in the function list.
        """
        s = ""
        if len(self._functions) == 0:
            s += "<blank plot>"
        else:
            self._render_lock.acquire()
            s += "\n".join(["%s[%i]: %s" % ("", i, str(self._functions[i]))
                            for i in self._functions])
            self._render_lock.release()
        return s

    def adjust_all_bounds(self):
        self._render_lock.acquire()
        self.axes.reset_bounding_box()
        for f in self._functions:
            self.axes.adjust_bounds(self._functions[f].bounds)
        self._render_lock.release()

    def wait_for_calculations(self):
        sleep(0)
        self._render_lock.acquire()
        for f in self._functions:
            a = self._functions[f]._get_calculating_verts
            b = self._functions[f]._get_calculating_cverts
            while a() or b():
                sleep(0)
        self._render_lock.release()

class ScreenShot:
    def __init__(self, plot):
        self._plot = plot
        self.screenshot_requested = False
        self.outfile = None
        self.format = ''
        self.invisibleMode = False
        self.flag = 0

    def __nonzero__(self):
        if self.screenshot_requested:
            return 1
        return 0

    __bool__ = __nonzero__

    def _execute_saving(self):
        if self.flag < 3:
            self.flag += 1
            return

        size_x, size_y = self._plot._window.get_size()
        size = size_x*size_y*4*sizeof(c_ubyte)
        image = create_string_buffer(size)
        glReadPixels(0, 0, size_x, size_y, GL_RGBA, GL_UNSIGNED_BYTE, image)
        from PIL import Image
        im = Image.frombuffer('RGBA', (size_x, size_y),
                              image.raw, 'raw', 'RGBA', 0, 1)
        im.transpose(Image.FLIP_TOP_BOTTOM).save(self.outfile, self.format)

        self.flag = 0
        self.screenshot_requested = False
        if self.invisibleMode:
            self._plot._window.close()

    def save(self, outfile=None, format='', size=(600, 500)):
        self.outfile = outfile
        self.format = format
        self.size = size
        self.screenshot_requested = True

        if not self._plot._window or self._plot._window.has_exit:
            self._plot._win_args['visible'] = False

            self._plot._win_args['width'] = size[0]
            self._plot._win_args['height'] = size[1]

            self._plot.axes.reset_resources()
            self._plot._window = PlotWindow(self._plot, **self._plot._win_args)
            self.invisibleMode = True

        if self.outfile is None:
            self.outfile = self._create_unique_path()
            print(self.outfile)

    def _create_unique_path(self):
        cwd = getcwd()
        l = listdir(cwd)
        path = ''
        i = 0
        while True:
            if not 'plot_%s.png' % i in l:
                path = cwd + '/plot_%s.png' % i
                break
            i += 1
        return path
