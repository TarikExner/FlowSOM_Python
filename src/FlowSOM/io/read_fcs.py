from __future__ import annotations

import re

import pytometry as pm


def read_FCS(filepath):
    """Reads in an FCS file

    :param filepath: An array containing a full path to the FCS file
    :type filepath: str
    """
    try:
        f = pm.io.read_fcs(filepath)
        f.var.n = f.var.n.astype(int)
        f.var = f.var.sort_values(by="n")
        f.uns["meta"]["channels"].index = f.uns["meta"]["channels"].index.astype(int)
        f.uns["meta"]["channels"] = f.uns["meta"]["channels"].sort_index()
    except:
        f = pm.io.read_fcs(filepath, reindex=False)
        markers = {
            str(re.sub("S$", "", re.sub("^P", "", string))): f.uns["meta"][string]
            for string in f.uns["meta"].keys()
            if re.match("^P[0-9]+S$", string)
        }
        fluo_channels = list(markers.keys())
        non_fluo_channels = {
            i: f.uns["meta"]["channels"]["$PnN"][i] for i in f.uns["meta"]["channels"].index if i not in fluo_channels
        }
        index_markers = dict(markers, **non_fluo_channels)
        f.var.rename(index=index_markers, inplace=True)
        f.uns["meta"]["channels"]["$PnS"] = [index_markers[key] for key in f.uns["meta"]["channels"].index]
    return f