#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 20:33:19 2022

@author: liyuzhe
"""
import torch
import torch.nn as nn


class VAE(nn.Module):
    def __init__(self, x_dim, c_dim):
        super(VAE, self).__init__() 
        
        # encoder layer
        self.e_fc1 = self.fc_layer(x_dim, 1024,activation=3)
        self.e_fc2 = self.fc_layer(1024, 128,activation=3)
        
        self.mu_enc = nn.Linear(128, 10)
        self.var_enc = nn.Linear(128, 10)
        self.g_enc = nn.Linear(128, 10)
        

        # decoder layer
        self.d_fc1 = self.fc_layer(10, 128,activation=3)
        self.d_fc2 = self.fc_layer(128, 1024,activation=3)
        self.d_fc3 = self.fc_layer(1024, x_dim, activation=2)
        self.d_fc4 = self.fc_layer(10, c_dim, activation=1)


    def reparameterize(self, mu, log_var):
        # vae reparameterization trick
        std = torch.exp(0.5*log_var)
        eps = torch.randn_like(std)
        
        self.z_mean = mu
        self.z_sigma = std
        
        return mu + eps*std
        
    
    def forward(self,x):
        
        mu, log_var, g = self.encoder(x)     
        z = self.reparameterize(mu, log_var)
        
        return self.decoder(z,g)
    
    
    def encoder(self, x): 
        
        layer1 = self.e_fc1(x) 
        layer2 = self.e_fc2(layer1)
        
        mu=self.mu_enc(layer2)
        log_var=self.var_enc(layer2)
        g = self.g_enc(layer2)
        
        return mu, log_var, g
      
    
    def decoder(self, z, g):
        # z_g = torch.cat((z,g),dim=1)
        z_g=z+g
        recon_x= self.d_fc3(self.d_fc2(self.d_fc1(z_g)))
        recon_g = self.d_fc4(g)
       
        return recon_x,recon_g
 
    
    def fc_layer(self, in_dim, out_dim, activation=0):
        if activation == 1:
            layer = nn.Sequential(
                nn.Linear(in_dim, out_dim),
                nn.ReLU())
        elif activation == 2:
            layer = nn.Sequential(
                nn.Linear(in_dim, out_dim))
        elif activation == 3:
            layer = nn.Sequential(
                nn.Linear(in_dim, out_dim),
                nn.BatchNorm1d(out_dim),
                nn.LeakyReLU())
        
        return layer  
    
    def predict(self, data, device='cuda', out='z'):
        x = data.float().to(device)
        
        mu, log_var, g = self.encoder(x)
        z = self.reparameterize(mu, log_var)
        # g_0 = torch.zeros_like(g)
        
        if out == 'latent':
            z_g=z+g
            output=z_g.detach().cpu().data.numpy()
        elif out == 'z':
            output=z.detach().cpu().data.numpy()
        elif out == 'z_p':
            output=g.detach().cpu().data.numpy()
        elif out == 'x':
            recon_x, recon_g = self.decoder(z,g)
            output = recon_x.detach().cpu().data.numpy()
        elif out == 'g':
            recon_x, recon_g = self.decoder(z,g)
            output = recon_g.detach().cpu().data.numpy()
        return output
    
    
    def predict_oe(self, data, z_p, device='cuda'):
        x = data.float().to(device)
        mu, log_var,g = self.encoder(x)
        z = self.reparameterize(mu, log_var)
        z_p = z_p.float().to(device)
        
        recon_x, recon_g = self.decoder(z,z_p)
        output = recon_x.detach().cpu().data.numpy()
        
        return output

    def predict_ko(self, data, device='cuda'):
        x = data.float().to(device)
        mu, log_var,g = self.encoder(x)
        z = self.reparameterize(mu, log_var)
        g_0 = torch.zeros_like(g)
        
        recon_x, recon_g = self.decoder(z,g_0)
        output = recon_x.detach().cpu().data.numpy()
        
        return output
    
    def predict_kd(self, data, z_p, device='cuda'):
        x = data.float().to(device)
        mu, log_var,g = self.encoder(x)
        z = self.reparameterize(mu, log_var)
        z_p = z_p.float().to(device)
        
        recon_x, recon_g = self.decoder(z,z_p)
        output = recon_x.detach().cpu().data.numpy()
        
        return output
    
    
    def load_model(self, path):
        pretrained_dict = torch.load(path, map_location=lambda storage, loc: storage)
        model_dict = self.state_dict()
        pretrained_dict = {k: v for k, v in pretrained_dict.items() if k in model_dict}
        model_dict.update(pretrained_dict) 
        self.load_state_dict(model_dict)
        

    
