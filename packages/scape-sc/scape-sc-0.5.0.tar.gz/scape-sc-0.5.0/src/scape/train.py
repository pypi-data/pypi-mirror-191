#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 15:09:45 2022

@author: liyuzhe
"""
import os
import torch
from torch.utils.data import DataLoader
from torch.autograd import Variable
import numpy as np
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
from .loss import compute_mmd, mse_loss
import random

      

def adjust_learning_rate(init_lr, optimizer, iteration,seperation):
    lr = max(init_lr * (0.9 ** (iteration//seperation)), 0.0001)
    for param_group in optimizer.param_groups:
        param_group["lr"] = lr
    return lr


class EarlyStopping:
    """
    Early stops the training if loss doesn't improve after a given patience.
    """
    def __init__(self, patience=10, verbose=False, checkpoint_file=''):
        """
        Parameters
        ----------
        patience 
            How long to wait after last time loss improved. Default: 10
        verbose
            If True, prints a message for each loss improvement. Default: False
        """
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.loss_min = np.Inf
        self.checkpoint_file = checkpoint_file

    def __call__(self, loss, model):
        # loss=loss.cpu().detach().numpy()
        if np.isnan(loss):
            self.early_stop = True
        score = -loss

        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(loss, model)
        elif score < self.best_score:
            self.counter += 1
            if self.verbose:
                print(f'EarlyStopping counter: {self.counter} out of {self.patience}')
            if self.counter > self.patience:
                self.early_stop = True
                model.load_model(self.checkpoint_file)
        else:
            self.best_score = score
            self.save_checkpoint(loss, model)
            self.counter = 0

    def save_checkpoint(self, loss, model):
        '''
        Saves model when loss decrease.
        '''
        if self.verbose:
            print(f'Loss decreased ({self.loss_min:.6f} --> {loss:.6f}).  Saving model ...')
        torch.save(model.state_dict(), self.checkpoint_file)
        self.loss_min = loss



def train(model, data, condition, velocity,epoch, batch_size, lr, weight_decay,patience,GPU, seed,verbose, outdir,a):
    
    if torch.cuda.is_available(): # cuda device
        device='cuda'
        torch.cuda.set_device(GPU)
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    else:
        device='cpu'
    
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    
    model.to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay) 
    model.train()
    
    dataset = torch.utils.data.TensorDataset(data,condition,velocity)
    
    early_stopping = EarlyStopping(patience=patience, checkpoint_file=os.path.join(outdir,'model.pt'))
    
    y_loss = {}  # loss history
    y_loss['MSE1'] = []
    y_loss['MSE2'] = []
    y_loss['train']=[]
    x_epoch = []
    
    fig = plt.figure()
    
    for epoch in tqdm(range(1, epoch+1)):
        epoch_lr = adjust_learning_rate(lr, optimizer, epoch, seperation=10)
        MSE1_loss=0.0
        MSE2_loss=0.0
        train_loss=0.0
        train_data=DataLoader(dataset,batch_size=batch_size,shuffle=True, drop_last=True)
        for iteration,data_list in enumerate(train_data):
            x=data_list[0].to(device)
            c=data_list[1].to(device)
            v=data_list[2].to(device)
            optimizer.zero_grad()
            recon_x, recon_g = model(x)
            mu, log_var,g = model.encoder(x)     
            z = model.reparameterize(mu, log_var)
            
            true_samples = Variable(torch.randn(x.shape[0], 10), requires_grad=False)
            mmd = 100*compute_mmd(true_samples.to(device), z)
            
            mse1=a*mse_loss(recon_x,v)
            mse2=mse_loss(recon_g,c)
            mse = mse1+mse2 
            loss=mse+mmd 
            loss.backward()      
            optimizer.step()  
            
            MSE1_loss += mse1.item()
            MSE2_loss += mse2.item()
            train_loss += loss.item()

        epoch_loss1 = MSE1_loss / len(train_data)
        epoch_loss2 = MSE2_loss / len(train_data)
        epoch_loss3 = train_loss / len(train_data)
        y_loss['MSE1'].append(epoch_loss1)
        y_loss['MSE2'].append(epoch_loss2)
        y_loss['train'].append(epoch_loss3)
        x_epoch.append(epoch)
        if verbose:
            plt.plot(x_epoch, y_loss['train'], 'go-', label='train',linewidth=1.5, markersize=4)
            plt.plot(x_epoch, y_loss['MSE1'], 'ro-', label='MSE1',linewidth=1.5, markersize=4)
            plt.plot(x_epoch, y_loss['MSE2'], 'bo-', label='MSE2',linewidth=1.5, markersize=4)
            if len(x_epoch)==1:
                plt.legend()
            
        print('====> Epoch: {}, Loss: {:.4f}, MSE: {:.4f}, MMD: {:.4f}'.format(epoch,loss.cpu().data.numpy(),mse.cpu().data.numpy(),mmd.cpu().data.numpy()))
        early_stopping(loss.cpu().data.numpy(), model)
        if early_stopping.early_stop:
            print('EarlyStopping: run {} epoch'.format(epoch))
            break
    if verbose:  
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        fig.savefig(os.path.join(outdir, 'train_loss.pdf'))
    
    return device



