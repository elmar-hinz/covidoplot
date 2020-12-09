from .lib.Supervisor import Supervisor
from .types.IncidencePlotter import IncidencePlotter


class IncidenceSupervisor(Supervisor):

    def __init__(self, dfs, type, key):
        self.type = type
        self.key = key
        self.df = dfs[type + '-' + key]

    def run(self):
        p = IncidencePlotter(data=self.df)
        p.title = '7-Tage-Inzidenz ' + Supervisor.title(self.type, self.key)
        p.run()
        self.save('last_weeks_incidence')

