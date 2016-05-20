import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

wine_data=pd.read_csv("/home/deva/NUS-ISS/SEM-1/CI1/CA/NN/winequality-white1.csv")
columns=wine_data.columns
wine_data[columns[:-1]]=wine_data[columns[:-1]]+1


#Boxplots
for col in wine_data.columns[:-1]:
    wine_data[col].plot.box()
    plt.savefig("/home/deva/PycharmProjects/ISS/CI_NN/plots/box/"+col+'.png')
    plt.clf()

plt.close()

#Histogram plots
for col in wine_data.columns[:-1]:
    wine_data[col].plot.hist()
    plt.savefig("/home/deva/PycharmProjects/ISS/CI_NN/plots/histograms/"+col+'.png')
    plt.clf()

plt.close()


#Boxplots Log normalized data
for col in wine_data.columns[:-1]:
    wine_data[col].apply(math.log10).plot.box()
    plt.savefig("/home/deva/PycharmProjects/ISS/CI_NN/plots/box_log/"+col+'.png')
    plt.clf()

plt.close()

#Histogram plots Log normalized data
for col in wine_data.columns[:-1]:
    wine_data[col].apply(math.log10).plot.hist()
    plt.savefig("/home/deva/PycharmProjects/ISS/CI_NN/plots/histograms_log/"+col+'.png')
    plt.clf()

plt.close()


