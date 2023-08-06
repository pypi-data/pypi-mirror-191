import muon as mu
import numpy as np
import scanpy as sc


def rna_preprocess(adata,
                   min_features=200,
                   min_cells=3,
                   pct_counts_mt=20,
                   target_sum=1e4,
                   n_top_features=None,
                   transform=None,
                   inplace=True):
    """
    scRNA-seq data preprocess
    """
    if not inplace:
        adata = adata.copy()

    adata.layers['counts'] = adata.X
    sc.pp.filter_cells(adata, min_genes=min_features)
    sc.pp.filter_genes(adata, min_cells=min_cells)

    if pct_counts_mt is not None:
        adata.var['mt'] = adata.var_names.str.startswith(tuple(['ERCC', 'MT-', 'mt-']))
        sc.pp.calculate_qc_metrics(adata,
                                   qc_vars=['mt'],
                                   percent_top=None,
                                   log1p=False,
                                   inplace=True)
        mu.pp.filter_obs(adata, 'pct_counts_mt', lambda x: x < pct_counts_mt)

    sc.pp.normalize_total(adata, target_sum=target_sum)
    sc.pp.log1p(adata)
    adata.raw = adata
    if n_top_features is not None:
        if type(n_top_features) == int:
            if n_top_features > 0:
                sc.pp.highly_variable_genes(adata, n_top_genes=n_top_features, subset=True)
            else:
                raise ValueError("Illegal n_top_features input!")
        elif type(n_top_features) == str:
            n_top_features = np.loadtxt(n_top_features, dtype=str)
            idx = [i for i, g in enumerate(n_top_features) if g in adata.var_names]
            adata = adata[:, idx]
    if transform:
        if sc.settings.verbosity > 1:
            print('transform...')
        adata.X = transform(adata.X)

    return adata if not inplace else None


def atac_preprocess(adata,
                    min_features=200,
                    min_cells=3,
                    peaks_filter_ratio=0.75,
                    n_top_regions=None,
                    transform=None,
                    inplace=True):
    """
    scATAC-seq data preprocess, tf-idf normalization is used.
    """
    if not inplace:
        adata = adata.copy()

    adata.layers['counts'] = adata.X
    sc.pp.filter_cells(adata, min_genes=min_features)
    sc.pp.filter_genes(adata, min_cells=min_cells)
    mu.atac.pp.tfidf(adata, scale_factor=1e4)
    sc.pp.normalize_per_cell(adata, counts_per_cell_after=1e4)
    sc.pp.log1p(adata)
    if peaks_filter_ratio:
        quantile = adata.var.n_cells.quantile(peaks_filter_ratio)
        mu.pp.filter_var(adata, 'n_cells', lambda x: x > quantile)
    adata.raw = adata
    if n_top_regions is not None:
        sc.pp.highly_variable_genes(adata, n_top_genes=n_top_regions, subset=True)
    if transform:
        if sc.settings.verbosity > 1:
            print('transform...')
        adata.X = transform(adata.X)

    return adata if not inplace else None