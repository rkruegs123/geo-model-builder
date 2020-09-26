import collections
import matplotlib.pyplot as plt
import os

class Diagram(collections.namedtuple("Diagram", ["points", "segments", "circles", "ndgs", "goals"])):
    def plot(self, show=True, save=False, fname=None):
        xs = [p.x for p in self.points.values()]
        ys = [p.y for p in self.points.values()]
        names = [n for n in self.points.keys()]

        fit, ax = plt.subplots()
        ax.scatter(xs, ys)
        for i, n in enumerate(names):
            ax.annotate(n, (xs[i], ys[i]))

        for p1, p2 in self.segments:
            plt.plot([p1.x, p2.x],[p1.y, p2.y])

        for O, r in self.circles:
            circle = plt.Circle((O.x, O.y),
                                radius=r,
                                fill=False)
            ax.add_artist(circle)

        plt.axis('square')
        if show:
            plt.show()
        if save:
            if fname is None:
                raise RuntimeError("Must supply filename if saving plot")
            if os.path.isfile(fname):
                os.remove(fname)
            plt.savefig(fname)
