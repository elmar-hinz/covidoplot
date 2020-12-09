from .lib.Supervisor import Supervisor
from .types.StackedPlotter import StackedPlotter


class StackedSupervisor(Supervisor):

    def __init__(self, dfs, count, type, key):
        self.count = count
        dfs = self.shorten_frames(dfs)
        self.type = type
        self.key = key
        self.df = dfs[type + '-' + key]

    def run(self):
        p = StackedPlotter(data=self.df)
        p.title = Supervisor.title(self.type, self.key)
        p.run()
        self.save('stacked')

