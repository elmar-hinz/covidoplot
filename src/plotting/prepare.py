from configuration import get as c
import pandas as pd

def concat(dfs):
    cdfs = {}
    for district in c('names.districts'):
        frames = []
        keys = []
        for commune, parent in c('parents.communes').items():
            if parent == district:
                frames.append(dfs['commune-' + commune].transpose())
                keys.append(commune)
        df = pd.concat(frames, keys=keys)
        cdfs['district-' + district] = df
    return cdfs

