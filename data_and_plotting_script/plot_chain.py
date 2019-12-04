#!/usr/bin/env python
import sys
import numpy as np
import math
import matplotlib
from matplotlib import pyplot as plt
import kde # code for 2D confidence region, from http://www.mit.edu/~iancross/python/kdestats.html
import scipy.ndimage



# Calculate upper and lower end of 1-dimensional confidence interval given marginalized data array
def interval_dim1(data_all, percent, nbins):
    sig1_interval = np.zeros(3)
    overall_mean = np.mean(data_all)
    
    hist, bin_edges = np.histogram(data_all, bins=nbins)
    total = hist.sum()

    center_index = 0
    for i in range(bin_edges.shape[0]):
        if overall_mean < bin_edges[i]:
            center_index = i-1
            break

    total_count = hist[center_index]
    sig1_index = 0

    for i in range(1, bin_edges.shape[0]/2):
        total_count += hist[center_index + i]
        if 1.0*total_count/total > percent:
            sig1_index = +i
            break
        total_count += hist[center_index - i]
        if 1.0*total_count/total > percent:
            sig1_index = -i
            break
    sig1_interval[0] = overall_mean
    sig1_interval[1] = (bin_edges[center_index+sig1_index]+bin_edges[center_index+sig1_index+1])/2
    sig1_interval[2] = (bin_edges[center_index-sig1_index]+bin_edges[center_index-sig1_index+1])/2

    return(sig1_interval)


# Return B, W, V, and R of Gelman-Rubin diagnostics given a nchains x nlength array of data
def Gelman_Rubin(data, nchains, nlength):
    in_chain_mean = np.zeros(nchains)
    in_chain_var = np.zeros(nchains)

    length = float(nlength)
    num_chains = float(nchains)
    for j in range(nchains):
        in_chain_mean[j] = np.mean(data[j])
        for i in range(nlength):
            in_chain_var[j] += (data[j, i]-in_chain_mean[j])**2
        in_chain_var[j] = in_chain_var[j]/length

    overall_mean = np.mean(in_chain_mean)

    b_param = 0
    w_param = 0
    for j in range(nchains):
        b_param += length/(num_chains - 1)*(overall_mean - in_chain_mean[j])**2
        w_param += 1/num_chains*in_chain_var[j]
    v_param = (length - 1)/length*w_param + (num_chains+1)/(num_chains*length)*b_param
    ratio_param = v_param/w_param
    
    return math.sqrt(ratio_param)

if __name__ == '__main__':
    data0 = np.loadtxt("data0.txt")
    data1 = np.loadtxt("data1.txt")
    data2 = np.loadtxt("data2.txt")
    data3 = np.loadtxt("data3.txt")

    # 5000 burn-in steps
    data = np.zeros((4, data0.shape[0]-5000, data0.shape[1]))
    data[0] = data0[5000:, :]
    data[1] = data1[5000:, :]
    data[2] = data2[5000:, :]
    data[3] = data3[5000:, :]

    data_all = np.transpose(np.concatenate((data[0], data[1], data[2], data[3])))
    
    # do Gelman-Rubin test
    for j in range(7):
        print(Gelman_Rubin(data[:, :, j], data.shape[0], data.shape[1]))
    
    # calculate posterior mean and confidence intervals
    for i in range(7):
        print(interval_dim1(data_all[i], 0.6827, 50))

    
    # plot posterior distribution for each parameter in each chain
    ticks = np.array([[0.0216, 0.0224], [0.1150, 0.120, 0.125], [1.0395, 1.0405, 1.0415], [0.02, 0.04, 0.06, 0.08], [0.95, 0.96, 0.97], [3.0, 3.05, 3.10]])
    ranges = np.array([[0.0213, 0.0227], [0.113, 0.128], [1.039, 1.042], [0.038, 0.085], [0.945, 0.98], [2.995, 3.105]])
    filenames = np.array(['ombh2_all_chains.png', 'omch2_all_chains.png', 'thetamc_all_chains.png', 'tau_all_chains.png',  'ns_all_chains.png', 'As_all_chains.png'])
    lables = np.array([r'$\Omega_b h^2$', r'$\Omega_c h^2$', r'$100 \theta_{MC}$', r'$\tau$', r'$n_s$',  r'$\log 10^{10}A_s$'])
    
    plot_chains = 0
    
    if plot_chains:
        for index in range(6):
            fig, ax = plt.subplots(2, 2)
            fig.set_size_inches(8, 6)
            plt.subplots_adjust(wspace=0.5, hspace=0.5)
            ax[0, 0].set_ylabel('Events', fontsize=16)
            ax[0, 0].set_title('chain 1', fontsize=16)
            ax[0, 0].set_xlim(ranges[index])
            ax[0, 0].set_xticks(ticks[index])
            ax[0, 0].set_xlabel(lables[index], fontsize=16)
            ax[0, 0].tick_params(labelsize=16)
            
    
    
            ax[0, 1].set_ylabel('Events', fontsize=16)
            ax[0, 1].set_title('chain 2',fontsize=16)
            ax[0, 1].set_xlim(ranges[index])
            ax[0, 1].set_xticks(ticks[index])
            ax[0, 1].set_xlabel(lables[index], fontsize=16)
            ax[0, 1].tick_params(labelsize=16)
        
    
    
            ax[1, 0].set_ylabel('Events', fontsize=16)
            ax[1, 0].set_title('chain 3',fontsize=16)
            ax[1, 0].set_xlim(ranges[index])
            ax[1, 0].set_xticks(ticks[index])
            ax[1, 0].set_xlabel(lables[index], fontsize=16)
            ax[1, 0].tick_params(labelsize=16)
            
    
            ax[1, 1].set_ylabel('Events', fontsize=16)
            ax[1, 1].set_title('chain 4',fontsize=16)
            ax[1, 1].set_xlim(ranges[index])
            ax[1, 1].set_xticks(ticks[index])
            ax[1, 1].set_xlabel(lables[index], fontsize=16)
            ax[1, 1].tick_params(labelsize=16)
            
            ax[0, 0].hist(data[0, :, index], bins=50)
            ax[0, 1].hist(data[1, :, index], bins=50)
            ax[1, 0].hist(data[2, :, index], bins=50)
            ax[1, 1].hist(data[3, :, index], bins=50)
            fig.savefig(filenames[index])
    
    # Plot 2D 68% and 95% confidence region
    # For 2D contour, set ticks and range to be as close to Planck 2018 as possible
    ticks_contour = np.array([[0.021, 0.023], [0.104, 0.120, 0.136], [1.038, 1.044], [0.925, 0.975, 1.025]])
    ranges_contour = np.array([[0.020, 0.025], [0.100, 0.140], [1.035, 1.048], [0.90, 1.05]])
    contour_index = np.array([0, 1, 2, 4])
    filenames_contour = np.array(['ombh2', 'omch2', 'thetamc',  'ns'])
    label_contour = np.array([r'$\Omega_b h^2$', r'$\Omega_c h^2$', r'$100 \theta_{MC}$',  r'$n_s$'])

    plot_contour = 1
    if plot_contour:
        for i in range(4):
            for j in range(i+1, 4):
                fig1, ax1 = plt.subplots(1, 1)
                fig1.tight_layout(rect=(0.2, 0.1, 1, 1))
                plt.subplots_adjust(wspace=0.3, hspace=0.5)

                ax1.set_xlabel(label_contour[i], fontsize=20)
                ax1.set_ylabel(label_contour[j], fontsize=20)
                ax1.set_xticks(ticks_contour[i])
                ax1.set_yticks(ticks_contour[j])
                ax1.set_xlim(ranges_contour[i])
                ax1.set_ylim(ranges_contour[j])
                ax1.tick_params(labelsize=20)
                kdehist = kde.kdehist2(data_all[contour_index[i]], data_all[contour_index[j]], [50, 50])

                clevels_sig1 = kde.confmap(kdehist[0], [.6827])
                clevels_sig2 = kde.confmap(kdehist[0], [.9545])

                ax1.contour(kdehist[1], kdehist[2], kdehist[0], clevels_sig1, colors='b', alpha=0.7)
                ax1.contour(kdehist[1], kdehist[2], kdehist[0], clevels_sig2, colors='b', alpha=0.4)
    
                fig1.savefig(filenames_contour[i]+'_'+filenames_contour[j]+'_contour.png')

    

    
