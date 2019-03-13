from __future__ import print_function, division
import numpy as np
import scipy as sp
from scipy.optimize import curve_fit
from ROOT import TCanvas, TGraph, TH1F, TF1, gStyle, TH1D
import ROOT as r
import matplotlib.pyplot as plt
import sys

plt.ion()
c1 = TCanvas()
gStyle.SetOptFit(111)

mean, std = 1 , 0.1
data = sp.random.normal(mean,std,500)

xmin = np.floor(10.*data.min())/10.
xmax = np.ceil(10.*data.max())/10.
nbins = int((xmax-xmin)*100)
hist, bin_edges, patches = plt.hist(data,nbins,(xmin,xmax))
bin_centers = (bin_edges[1:]+bin_edges[:-1])/2.
nz = hist>0

first_nz = bin_centers[nz][ 0] - 0.005
last_nz  = bin_centers[nz][-1] + 0.005

root_hist = np.zeros(nbins+2,dtype=float)
root_hist[1:-1] = hist
h = TH1D('h','hist',nbins,bin_edges)
h.SetContent(root_hist)
# h.Fit('gaus','','',first_nz,last_nz)
h.Fit('gaus','','',0.85,1.15)
h.Draw()
c1.SaveAs('root_fit.png')

# Get Root Fit and Goodness of Fit Parameters #
f = h.GetFunction('gaus')
const,mu,sigma = f.GetParameter(0), f.GetParameter(1), f.GetParameter(2)
econst,emu,esigma = f.GetParError(0), f.GetParError(1), f.GetParError(2)
ndf,chi2,prob = f.GetNDF(),f.GetChisquare(),f.GetProb()

# print(const, mu, sigma)
# print(econst, emu, esigma)
# print(ndf, chi2, prob)

# Scipy Fit :
def gaus(x, const, mu, sigma):
    return const* np.exp(-0.5*((x - mu)/sigma)**2)

#coeff, covar = curve_fit(gaus, bin_centers, hist)
rng = (bin_centers>=0.85)*(bin_centers<=1.15)
coeff, covar = curve_fit(gaus, bin_centers[rng], hist[rng])

# Compare ROOT and curve_fit results
x = bin_centers
root_gaus = (const,mu,sigma)
opti_gaus = coeff
si = np.sqrt(hist)
f_root = gaus(x,*root_gaus)
f_opti = gaus(x,*opti_gaus)
# ch2_root = np.sum( (hist[nz]-f_root[nz])**2/si[nz]**2 )
# ch2_opti = np.sum( (hist[nz]-f_opti[nz])**2/si[nz]**2 )
# dof = len(x[nz])-3
ch2_root = np.sum( (hist[rng]-f_root[rng])**2/si[rng]**2 )
ch2_opti = np.sum( (hist[rng]-f_opti[rng])**2/si[rng]**2 )
dof = len(x[rng])-3

print(ch2_root, ch2_opti)
# print(ch2_root/dof, ch2_opti/dof)

# Draw Hitogram and Fit with Python Mathplotlib :
root_txt = '\n'.join((
    r'Pyroot Fit:',
    r'$height={0:.4f}$'.format(const),
    r'$\mu={0:.4f}$'.format(mu),
    r'$\sigma={0:.4f}$'.format(sigma),
    r'$\chi^2 / ndf ={0:.4f} / {1}$'.format(ch2_root, ndf),
    r'$prob ={0:.4f}$'.format(prob)))

scipy_txt = '\n'.join((
    r'Scipy Fit:',
    r'$height={0:.4f}$'.format(coeff[0]),
    r'$\mu={0:.4f}$'.format(coeff[1]),
    r'$\sigma={0:.4f}$'.format(np.abs(coeff[2])),
    r'$\chi^2 / ndf \approx{0:.4f} / {1}$'.format(ch2_opti, dof)))

# plt.plot(bin_centers[rng], f_root[rng], 'k--', linewidth=2, label='ROOT')
# plt.plot(bin_centers[rng], f_opti[rng], 'r--', linewidth=2, label='curve_fit')
plt.hist(data,nbins,(xmin,xmax),color='g',alpha=0.6)
plt.plot(bin_centers[rng], f_root[rng], 'k--', linewidth=2, label='ROOT')
plt.plot(bin_centers[rng], f_opti[rng], 'r--', linewidth=2, label='curve_fit')
xmin,xmax = plt.xlim()
ymin,ymax = plt.ylim()
xtxt,ytxt = xmin+0.05*(xmax-xmin), ymin+0.95*(ymax-ymin)
plt.text(xtxt, ytxt, root_txt, verticalalignment='top')
xtxt,ytxt = xmin+0.05*(xmax-xmin), ymin+0.65*(ymax-ymin)
plt.text(xtxt, ytxt, scipy_txt,verticalalignment='top', color='r')
title = 'Pyroot vs. Scipy Fit'
plt.title('ROOT vs. Scipy curve_fit')
plt.grid()
plt.savefig('python_fit.png')
