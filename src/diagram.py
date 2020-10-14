import collections
import matplotlib.pyplot as plt
import os
import pdb
import numpy as np
import math



class Diagram(collections.namedtuple("Diagram", ["named_points", "named_lines", "named_circles", "segments", "unnamed_points", "unnamed_lines", "unnamed_circles", "ndgs", "goals"])):
    def plot(self, show=True, save=False, fname=None, return_fig=False):

        # Plot named points
        xs = [p.x for p in self.named_points.values()]
        ys = [p.y for p in self.named_points.values()]
        names = [n for n in self.named_points.keys()]

        fig, ax = plt.subplots()

        ax.scatter(xs, ys)
        for i, n in enumerate(names):
            ax.annotate(str(n), (xs[i], ys[i]))

        # Plot unnamed points
        u_xs = [p.x for p in self.unnamed_points]
        u_ys = [p.y for p in self.unnamed_points]
        ax.scatter(u_xs, u_ys, c="black", alpha=0.5)

        # Plot segments (never named)
        for p1, p2 in self.segments:
            plt.plot([p1.x, p2.x],[p1.y, p2.y])

        for O, r in self.unnamed_circles:
            circle = plt.Circle((O.x, O.y),
                                radius=r,
                                fill=False,
                                color="black"
            )
            ax.add_patch(circle)

        for (c_name, (O, r)) in self.named_circles.items():
            circle = plt.Circle((O.x, O.y),
                                radius=r,
                                fill=False,
                                label=c_name,
                                color=np.random.rand(3)
            )
            ax.add_patch(circle)

        plt.axis('scaled')
        plt.axis('square')

        # Plot lines AFTER all bounds are set

        have_points = self.named_points or self.unnamed_points
        have_circles = self.named_circles or self.unnamed_circles

        if not (have_points or have_circles):
            plt.xlim(-2, 2)
            plt.ylim(-2, 2)


        def plot_line(L, name=None):
            (nx, ny), r = L
            l_angle = math.atan(ny / nx) % math.pi
            if l_angle == 0:
                if name is not None:
                    plt.axvline(x=r, label=name) # FIXME: Check if this labrel works
                else:
                    plt.axvline(x=r)
            else:
                slope = -1 / math.tan(l_angle)
                intercept = r / math.sin(l_angle)

                eps = 0.2
                (lo_x_lim, hi_x_lim) = ax.get_xlim()
                x_vals = np.array((lo_x_lim - 0.2, hi_x_lim + 0.2))
                y_vals = intercept + slope * x_vals
                if name is not None:
                    # plt.plot(x_vals, y_vals, '--', label=l_name)
                    plt.plot(x_vals, y_vals, label=name)
                else:
                    # plt.plot(x_vals, y_vals, '--', c="black")
                    plt.plot(x_vals, y_vals, c="black", alpha=0.5)

        # Plot named lines
        for l, L in self.named_lines.items():
            # ax + by = c
            l_name = l.val
            plot_line(L, l_name)

        # Plot unnamed lines
        for L in self.unnamed_lines:
            plot_line(L)

        if self.named_lines or self.named_circles:
            plt.legend()

        if return_fig:
            return plt

        if show:
            plt.show()
        if save:
            if fname is None:
                raise RuntimeError("Must supply filename if saving plot")
            if os.path.isfile(fname):
                os.remove(fname)
            plt.savefig(fname)
