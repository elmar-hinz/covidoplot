from .lib.Supervisor import Supervisor
from .types.ComparisonPlotter import ComparisonPlotter
from .types.lib.colors import colors
from configuration import plural as p
from configuration import get as c

class VerticalComparisonSupervisor(Supervisor):

    def __init__(self,
                 dfs,
                 count,
                 field,
                 type,
                 key,
                 title_prefix,
                 ylabel,
                 file_name_suffix
                 ):
        self.count = count
        dfs = self.shorten_frames(dfs)
        self.field = field
        self.type = type
        self.key = key
        self.title_prefix = title_prefix
        self.ylabel = ylabel
        self.file_name_suffix = file_name_suffix
        self.colors = [colors[i] for i in [0, 3, 5, 9]]
        self.dfs = [
            dfs['country-germany'],
            dfs['country-italy'],
        ]
        self.labels = [
            'Deutschland', 'Italien',
#            'Deutschlandtrend ohne Lockerungen'
        ]
        if type in ['commune', 'district']:
            # Hack TODO improve
            self.dfs.insert(0, dfs['district-hoexter'])
            self.labels.insert(0, 'Kreis Höxter')
        if type in ['commune']:
            self.dfs.insert(0, dfs['commune-' + key])
            self.labels.insert(0, c('names.communes')[self.key])

    def run(self):
        p = ComparisonPlotter(data=self.dfs, start=0)
        p.field = self.field
        p.labels = self.labels
        p.colors = self.colors
        p.title = self.title_prefix + ' ' + \
                  Supervisor.title(self.type, self.key)
        p.ylabel = self.ylabel
        p.run()
        self.save(self.file_name_suffix)



