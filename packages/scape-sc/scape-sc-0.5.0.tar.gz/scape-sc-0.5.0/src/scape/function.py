#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 16:21:44 2022

@author: liyuzhe
"""
import os
import random
import pandas as pd
import numpy as np
import scanpy as sc
import scvelo as scv
import torch

from .model import VAE
from .train import train



def SCAPE(adata,adata_raw,genes,perturbation='KO',epoch=1000,lr=0.0005,patience=10,seed=42,GPU=0,batch_size=128,n_jobs=1,a=50,outdir='./',verbose=False):
    """
    Single-Cell data Analysis via Perturbation Estimation
    
    Parameters
    ----------
    adata
        An AnnData Object with cell x gene matrix stored.
    adata_raw
        An AnnData Object with cell x gene matrix stored.
    genes
        The list of genes for in silico genetic perturbation.
    perturbation
        The type of perturbation, including KO, KD, and OE. 
    lr
        Learning rate. Default: 5e-4.
    patience
        Patience in early stopping. Default: 10.
    epoch
        Max epochs for training. Default: 1000.
    seed
        Random seed. Default: 42. 
    GPU
        Index of GPU to use if GPU is available. Default: 0.
    batch_size
        Number of samples of each batch in training.
    n_jobs
        Number of CPUs.
    a
        The ratio of reconstruction loss.
    outdir
        Output directory. Default: '.'.
    verbose
        Verbosity, True or False. Default: False.
    
    
    Returns
    -------
    adata with the low-dimensional representation of the data stored at adata.obsm['latent'], and calculated neighbors and Umap. 
    The output folder contains:
    adata.h5ad
        The AnnData Object with the low-dimensional representation of the data stored at adata.obsm['latent'].
    checkpoint
        model.pt contains the variables of the model.
    """
    
    np.random.seed(seed) 
    torch.manual_seed(seed)
    random.seed(seed)
    
    os.makedirs(outdir, exist_ok=True)
    for i in genes:
        if i in list(adata.var[adata.var["velocity_genes"]].index):
            adata.var['velocity_genes'][[i]]=False
    # adata.var['velocity_genes'][genes]=False
    velocity_genes=adata.var[adata.var["velocity_genes"]].index.copy()
    
    cond = torch.from_numpy(adata_raw[:,genes].X.A.astype(np.float32).copy())
    data = torch.from_numpy(adata_raw[:, velocity_genes].X.A.astype(np.float32).copy())
    vel = torch.from_numpy(adata.layers["velocity"][:, adata.var["velocity_genes"]].astype(np.float32).copy())
    
    x_dim=data.shape[1]
    c_dim=cond.shape[1]
    
    model=VAE(x_dim, c_dim)
    
    device=train(model, data,condition=cond, velocity=vel,epoch=epoch, batch_size=batch_size,lr=lr,weight_decay=5e-4, patience=patience,GPU=GPU, seed=seed,verbose=verbose, outdir=outdir,a=a)
    
    # Load model
    pretrained_dict = torch.load(os.path.join(outdir,'model.pt'), map_location=device)                            
    model_dict = model.state_dict()
    pretrained_dict = {k: v for k, v in pretrained_dict.items() if k in model_dict}
    model_dict.update(pretrained_dict) 
    model.load_state_dict(model_dict)
    model = model.eval()
    
    # save velocity
    latent = model.predict(data,out='latent') 
    adata.obsm['latent']=latent.copy()
    
    latent_g = model.predict(data,out='z_p') 
    adata.obsm['latent_g']=latent_g.copy()

    if perturbation=='KO':
        recon_x = model.predict(data,out='x',device=device) 
        recon_x_ = model.predict_ko(data,device=device)
      
        adata.layers['velocity_scvelo']=adata.layers['velocity'].copy()
        
        gene_subset=adata.var["velocity_genes"]
        
        adata.layers['velocity_scape_unp'] = np.ones(adata.shape) * np.nan
        adata.layers['velocity_scape_unp'][:, gene_subset] = recon_x.copy()
        adata.layers['velocity_scape'] = np.ones(adata.shape) * np.nan
        adata.layers['velocity_scape'][:, gene_subset] = recon_x_.copy()
        velocity_delta = adata.layers['velocity_scape']-adata.layers['velocity_scape_unp']
        adata.layers['velocity_delta']=velocity_delta.copy()

    elif perturbation=='OE':
        recon_x = model.predict(data, out='x',device=device) 

        df=pd.DataFrame(adata[:,genes].X.A,index=adata.obs.index,columns=genes)
        idx=df.sort_values(by=genes,ascending=False).index[:int(adata.shape[0] * 0.01)]
        z_p = torch.from_numpy(adata[idx].obsm['latent_g'].mean(axis=0)).float().repeat(adata.shape[0],1)
        recon_x_ = model.predict_oe(data,z_p,device=device) 
        
        adata.layers['velocity_scvelo']=adata.layers['velocity'].copy()
        gene_subset=adata.var["velocity_genes"]
        adata.layers['velocity_scape_unp'] = np.ones(adata.shape) * np.nan
        adata.layers['velocity_scape_unp'][:, gene_subset] = recon_x.copy()
        adata.layers['velocity_scape'] = np.ones(adata.shape) * np.nan
        adata.layers['velocity_scape'][:, gene_subset] = recon_x_.copy()
        velocity_delta = adata.layers['velocity_scape']-adata.layers['velocity_scape_unp']
        adata.layers['velocity_delta']=velocity_delta.copy()

    elif perturbation=='KD':
        recon_x = model.predict(data, out='x',device=device) 

        df=pd.DataFrame(adata[:,genes].X.A,index=adata.obs.index,columns=genes)
        idx=df[df[genes]==0].index
        z_p = torch.from_numpy(adata[idx].obsm['latent_g'].mean(axis=0)).float().repeat(adata.shape[0],1)
        recon_x_ = model.predict_oe(data,z_p,device=device) 
        
        adata.layers['velocity_scvelo']=adata.layers['velocity'].copy()
        gene_subset=adata.var["velocity_genes"]
        adata.layers['velocity_scape_unp'] = np.ones(adata.shape) * np.nan
        adata.layers['velocity_scape_unp'][:, gene_subset] = recon_x.copy()
        adata.layers['velocity_scape'] = np.ones(adata.shape) * np.nan
        adata.layers['velocity_scape'][:, gene_subset] = recon_x_.copy()
        velocity_delta = adata.layers['velocity_scape']-adata.layers['velocity_scape_unp']
        adata.layers['velocity_delta']=velocity_delta.copy()
    
    adata.layers['velocity']=adata.layers['velocity_scape'].copy()
    scv.tl.velocity_graph(adata,n_jobs=n_jobs)

    #Output
    adata.write(os.path.join(outdir,'adata.h5ad'))   
    
    return adata
    
