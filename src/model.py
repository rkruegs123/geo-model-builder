import collections
import matplotlib.pyplot as plt

class Model(collections.namedtuple("Model", ["points", "segments", "circles"])):
    def plot(self):
        xs = [p.x for p in self.points.values()]
        ys = [p.y for p in self.points.values()]
        names = [n for n in self.points.keys()]

        fit, ax = plt.subplots()
        ax.scatter(xs, ys)
        for i, n in enumerate(names):
            ax.annotate(n, (xs[i], ys[i]))
        plt.axis('square')
        plt.show()
