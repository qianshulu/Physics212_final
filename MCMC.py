#!/usr/bin/env python3
import sys
sys.path = ["./plc_3.0/plc-3.01/lib/python/site-packages"]+sys.path

import numpy as np
import camb as camb
from camb import model, initialpower, CAMBError, CAMBValueError, CAMBParamRangeError
import math
import clik

import scipy.stats as stats


class MCMC:
    
    # Initializer / instance attributes
    def __init__(self, num_chain, chain_length, datafile):
        self.num_chains = num_chain
        self.length = chain_length
        self.chain = None
        
        self.param_names = np.array(['ombh2', 'omch2', '100thetaMC', 'tau', 'ns', 'log10to10As'])
        
        # All priors are flat except for the last one, Planck absolute calibration, which is Gaussian
        self.priors = np.array([[0.005, 0.1],[0.001, 0.99],[0.5, 10.0],[0.01, 0.08],[0.9, 1.1],[2.7, 4.0],[1.0, 0.0025]])
        
        # This is the starting point of the MC chain
        self.params = np.array([[0.0220981386, 0.1223302021, 1.0406124113, 0.0487720060, 0.9584767704, 3.0335752930, 0.9972325150],[0.0222016616, 0.1198321067, 1.0405862949, 0.0691682301, 0.9633628523, 3.0733209766, 0.9995508352],[0.0222579046, 0.1249771297, 1.0403435221, 0.0660488831, 0.9515182965, 3.0853630432, 1.0032000206],[0.0219338687, 0.1195137025, 1.0403897640, 0.0699657014, 0.9612076581, 3.0623862644, 0.9935071817]])
        
        self.camb_params = np.zeros(6)
        self.num_params = 7
        self.dataf = datafile
        self.conv = 100
        self.ready = False
        
        self.camb_pars = camb.CAMBparams()

        self.draw_width = np.array([0.00004, 0.0003, 0.00008, 0.0015, 0.0009, 0.004, 0.0004])
       
        self.camb_Cls = None
        self.likelihood = np.zeros(4)
        self.posterior = np.zeros(4)
        
        self.plik = clik.clik('./plik')

    
    # Draw from a normal distribution until all values are within flat prior
    def draw_state(self, center):
        temp = np.zeros(center.shape[0])
        for i in range(self.num_params-1):
            while True:
                temp[i] = np.random.normal(center[i], self.draw_width[i])
                if self.priors[i,0] <= temp[i] <= self.priors[i, 1]:
                    break
        temp[6] = np.random.normal(center[6], self.draw_width[6])
        return(temp)
    
    # module to calculate probability density of a point in normal distribution
    def normpdf(self, x, mean, sd):
        var = float(sd)**2
        denom = (2*math.pi*var)**.5
        num = math.exp(-(float(x)-float(mean))**2/(2*var))
        return num/denom
    
    # module to convert parameters in MC units to CAMB units
    def mc_to_camb(self, params):
        temp = np.copy(params)
        temp[2] = params[2]/100        
        temp[5] = math.exp(params[5])/10**10
        return(temp)
    
    # Run CAMB and PLIK to calculate likelihood from a set of parameters
    def calc_likelihood(self, last_state, draw_state):
        # generate a new state
        if draw_state:
            while True:
                cand_param = self.draw_state(last_state)
                cand_camb_params = self.mc_to_camb(cand_param)

                # Make sure parameters generated has reasonabl cosmology (i.e. H0 within 10 to 100)
                try:
                    self.camb_pars.set_cosmology(ombh2=cand_camb_params[0], omch2=cand_camb_params[1], mnu=0.06, omk=0, cosmomc_theta=cand_camb_params[2], tau=cand_camb_params[3])
                    break
                except CAMBParamRangeError:
                    # Bad cosmology. Try again.
                    continue
        # For initialization of Markov chain
        else:
            cand_param = last_state
            cand_camb_params = self.mc_to_camb(last_state)
            try:
                self.camb_pars.set_cosmology(ombh2=cand_camb_params[0], omch2=cand_camb_params[1], mnu=0.06, omk=0, cosmomc_theta=cand_camb_params[2], tau=cand_camb_params[3])
            except CAMBParamRangeError:
                print("Bad cosmology. Pick a different starting value.")

        print("state is {}".format(cand_param))
        
        # Set CAMB parameters and calculate Cls
        self.camb_pars.set_for_lmax(lmax=2508)
        self.camb_pars.InitPower.set_params(ns=cand_camb_params[4], As=cand_camb_params[5], r=0)
        results = camb.get_results(self.camb_pars)
        powers=results.get_cmb_power_spectra(self.camb_pars, raw_cl=True, lmax=2508, CMB_unit='muK')
        self.camb_CLs = powers['total'][:, 0]
        self.camb_CLs = np.append(self.camb_CLs, cand_camb_params[6])
        
        # Calculate likelihood using plik
        print("log likelihod is {}".format(self.plik(self.camb_CLs)[0]))
        return(math.exp(self.plik(self.camb_CLs)[0]), cand_param)
    
    # Calculate total posterior given log likelihood and value of parameters
    def total_posterior(self, likelihood, params):
        for i in range(6):
            if self.priors[i, 0] <= params[i] <= self.priors[i, 1]:
                continue
            else:
                return(0)
        # All priors are flat, except parameter at index 6 which has a Gaussian prior. Weigh likelihood by that prior.
        posterior = likelihood*self.normpdf(params[6], self.priors[6, 0], self.priors[6, 1])
        return(posterior)
        
    def initialize(self, file_path=None):

        print("Starting initialization.")
        
        for j in range(self.num_chains):
            # Calculate likelihood using CAMB and plik
            self.likelihood[j], a =self.calc_likelihood(self.params[j], False)
            # Calculate total posterior
            self.posterior[j] = self.total_posterior(self.likelihood[j], self.params[j])
        
        print("The likelihood is {}\n".format(self.likelihood))
        print("The posterior is {}\n".format(self.posterior))
 
        # Initialize numerical parameter chains
        self.chain = np.zeros((self.num_chains, self.length, self.num_params))
        self.weight = np.zeros((self.num_chains, self.length))
        for j in range(self.num_chains):
            self.chain[j, 0] =  self.params[j]        
        
        # Set ready flag for run() function
        self.ready = True
        
        print("Ending initialization.")
        
        
    def run(self):
        if self.ready is False:
            print("run() warning: MCMC not properly initalized.")
            return
        print("Starting MCMC run.")
        
        cand_likelihood = np.zeros(4)
        cand_param = np.zeros((4, 7))
        cand_posterior = np.zeros(4)
        for i in range(1, self.length):
            for j in range(0, self.num_chains):
                print("\n")
                print("At chain No.{} position {}".format(j, i))
                # Calculate likelihood
                cand_likelihood[j], cand_param[j] = self.calc_likelihood(self.chain[j, i-1], True)
                cand_posterior[j] = self.total_posterior(cand_likelihood[j], cand_param[j])
                
                # Calculate MH ratio and accept or reject the state
                ratio = min(1, cand_posterior[j]/self.posterior[j])

                random = np.random.uniform(0.0, 1.0)
                if random < ratio:
                    print("candidate accepted.")
                    self.chain[j, i] = cand_param[j]
                    self.weight[j, i] = 0
                    self.posterior[j] = cand_posterior[j]
                else:
                    print("candidate rejected.")
                    self.chain[j, i] = self.chain[j, i-1]
                    self.weight[j, i] = 1
                
                acceptance = 1-np.sum(self.weight[j, 1:i+1])/i
                print("Cumulative acceptance rate is {}".format(acceptance))
                
                # Save chain to text file (this is really redundance since it saves the full array every time)
                np.savetxt(self.dataf+str(j)+str(".txt"), self.chain[j], '%.10f')

if __name__ == "__main__":
    mcmc = MCMC(4, 5000, "chain_data")
    mcmc.initialize()
    mcmc.run()
    print("End of operation.")