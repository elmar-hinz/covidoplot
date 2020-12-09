from .lib.Supervisor import Supervisor
from .types.ComparisonPlotter import ComparisonPlotter
from .types.lib.colors import colors
from configuration import plural as p
from configuration import get as c


class ComparisonSupervisor(Supervisor):

    def __init__(self,
                 cdfs,
                 count,
                 field,
                 type,
                 child_type,
                 key,
                 title_prefix,
                 file_name_suffix,
                 ):
        self.count = count
        cdfs = self.shorten_frames(cdfs, horizontal=True)
        self.field = field
        self.type = type
        self.child_type = child_type
        self.key = key
        self.title_prefix = title_prefix
        self.file_name_suffix = file_name_suffix
        self.df = cdfs[type + '-' + key]
        self.dfs = []
        self.keys = []
        self.labels = []
        self.colors = colors
        self.read_children()
        self.create_list_of_dataframes()


    def read_children(self):
        for k, v in c('names')[p(self.child_type)].items():
            self.keys.append(k)
            self.labels.append(v)

    def create_list_of_dataframes(self):
        for key in self.keys:
            frame = self.df.loc[key].transpose()
            self.dfs.append(frame)

    def run(self):
        p = ComparisonPlotter(data=self.dfs, start=0)
        p.field = self.field
        p.labels = self.labels
        p.colors = self.colors
        p.title = self.title_prefix + ' ' + \
                  Supervisor.title(self.type, self.key)
        p.run()
        self.save(self.file_name_suffix)

