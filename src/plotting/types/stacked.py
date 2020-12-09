from .lib.commons import title
from .lib.commons import save
from .StackedPlotter import StackedPlotter

def plot(df, type, key):
    p = StackedPlotter(data=df)
    p.title = title(type, key)
    p.run()
    save(type, key, 'stacked')
