import collections
import matplotlib.pyplot as plt
import os
import pdb
import numpy as np
import math



class Diagram(collections.namedtuple("Diagram", ["named_points", "named_lines", "named_circles", "segments", "unnamed_circles", "ndgs", "goals"])):
    def plot(self, show=True, save=False, fname=None, return_fig=False):
        xs = [p.x for p in self.named_points.values()]
        ys = [p.y for p in self.named_points.values()]
        names = [n for n in self.named_points.keys()]

        fig, ax = plt.subplots()

        ax.scatter(xs, ys)
        for i, n in enumerate(names):
            ax.annotate(str(n), (xs[i], ys[i]))

        for p1, p2 in self.segments:
            plt.plot([p1.x, p2.x],[p1.y, p2.y])

        for O, r in self.unnamed_circles:
            circle = plt.Circle((O.x, O.y),
                                radius=r,
                                fill=False
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
        if not names and not self.named_circles:
            plt.xlim(-2, 2)
            plt.ylim(-2, 2)

        for l, L in self.named_lines.items():
            # ax + by = c
            l_name = l.val
            (nx, ny), r = L
            l_angle = math.atan(ny / nx) % math.pi
            if l_angle == 0:
                plt.axvline(x=r, label=l_name) # FIXME: Check if this labrel works
            else:
                slope = -1 / math.tan(l_angle)
                intercept = r / math.sin(l_angle)

                x_vals = np.array(ax.get_xlim())
                y_vals = intercept + slope * x_vals
                # plt.plot(x_vals, y_vals, '--', label=l_name)
                plt.plot(x_vals, y_vals, label=l_name)


            '''
            la, lb, lc, _, _ = L

            if la == 0: # 0x + by = c --> y = c / b
                plt.axhline(x=(lc / lb))
            elif lb == 0: # ax + 0y = c --> x = c / a
                plt.axvline(x=(lc / la))
            else:
                # ax + by = c ---> y = (-ax + c) / b
                slope = -la / lb
                intercept = lc / lb

                x_vals = np.array(ax.get_xlim())
                y_vals = intercept + slope * x_vals
                # plt.plot(x_vals, y_vals, '--', label=l_name)
                plt.plot(x_vals, y_vals, label=l_name)
            '''

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
