"""
cell type annotation utils.
---
Ning Weixi 20230209
"""
import scanpy as sc
import numpy as np


def infer_celltype_from_dotplot(adata, groupby, markers):
    """
    params
    ---
    markers: same as `var_names` in `sc.pl.DotPlot`. a `dict` of `celltype: gene list` pairs.
    
    returns
    ---
    cts: a `dict` of `celltype: group list` pairs.
    """
    dp = sc.pl.DotPlot(adata, groupby=groupby, use_raw=True, var_names=markers)
    inferred_cts = np.array(
        sum([[celltype] * (item[1] + 1 - item[0])
             for celltype, item in zip(dp.var_group_labels, dp.var_group_positions)],
            start=[]))[np.argmax((dp.dot_color_df * dp.dot_size_df).values, axis=1)]
    cts = {ct: np.where(inferred_cts == ct)[0].tolist() for ct in np.unique(inferred_cts)}
    return cts