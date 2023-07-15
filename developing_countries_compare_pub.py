#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 15:56:45 2023

@author: usuari
"""

# DEVELOPING COUNTRIES ECONOMIC INDICES



import os
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
#from seaborn import set_theme

plt.style.use('seaborn-darkgrid')


sns.set_style("darkgrid")
#sns.set_style("whitegrid")


def sort_and_reset_ind_df(df,colnames):
    
    heads1 = df.columns
    dat = df.sort_values(by=colnames, ascending=True)
    datt = dat.reset_index()
    heads2 = datt.columns
    if len(heads2) > len(heads1) and 'index' in heads2:
        datt.drop(columns=['index'], inplace=True)
    return datt

os.chdir('set your current folder here')
cd = os.getcwd()


file_list = os.listdir(cd)

file_list = [item for item in file_list if '.xlsx' in item]


d = {}
for i in range(0,len(file_list)):
    
    name_excel = file_list[i]
    segments = name_excel.split("_");
    name = segments[-1];
    nm = name[0:4]
    df = pd.read_excel(name_excel)
    df.set_index(' ',inplace=True)
    df = df.replace('..', np.nan)

    df=df.transpose()

    for column in df.columns:
        
        df[column] = df[column].str.replace(',', '')
        
    df=df.astype(float)
    
    dim = df.shape
    
    df['country'] = [f'{nm}'] * dim[0]
    df['year'] = df.index
    
    df = sort_and_reset_ind_df(df,['year','country'])
    
    d[f"df_{nm}"] = df

data = pd.concat((d['df_phil'], d['df_thai'], d['df_mexi'],
                  d['df_braz'], d['df_paki'], d['df_pola'],
                  d['df_indo'], d['df_czec'], d['df_chil'],
                  d['df_roma'], d['df_japa'], d['df_nige'],
                  d['df_irel'], d['df_viet'], d['df_indi'],
                  d['df_mala'], d['df_kore']),axis=0)


countries = list(data['country'].unique())


iris = sns.color_palette("Spectral", len(countries))


columns = list(data.columns)


for column in columns:
    
    if not data[column].isnull().all():
    
        cur_data = data[[column,'country','year']]
        
        cur_data = sort_and_reset_ind_df(cur_data,['year','country'])
    
        cur_countries = list(cur_data['country'].unique())
        
        colors = iris[0:len(cur_countries)]

        with sns.axes_style("darkgrid"):
            
            fig = plt.figure(1)
            
            f = sns.lineplot(data=cur_data, 
                                x='year',
                                y=column,
                                 hue='country',
                                 palette=colors
                                  )
            
            f.set(ylabel=None)
            
            plt.title(f'{column[0:60]}')
    
            axes = f.axes
            
            sns.despine(left=True, bottom=True)
            
            plt.legend([],[], frameon=False)
                    

        lgd = axes.get_legend()
        lgd = fig.legend(prop={'size': 8},bbox_to_anchor=(1.1, 1.))
    
        fig.tight_layout()
        fig.savefig(f'{column[0:20]}',dpi=1000,bbox_inches='tight')
    
        plt.show()

            

          