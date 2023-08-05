""" Utilities for gaussian fits in Skipper-CCD images.
"""

# imports
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


# constants
R2PI = np.sqrt(2*np.pi)


# classes
class GaussianPeak:
    def __init__(self, amplitude, mean, std, bin_width=None, cov_matrix=None):
        
        self.amplitude = amplitude
        self.mean = mean
        self.std = std

        self.params = [self.amplitude, self.mean, self.std]

        self.bin_width = bin_width
        self.cov_matrix = cov_matrix
    

    def fit(self, hist: np.ndarray, xmin=None, xmax=None, ax=None, plot=False):

        gfit = single_gaussian_fit(hist, xmin=xmin, xmax=xmax, ax=ax, 
                                   plot=plot, init_guess=self.params)
        return gfit


    def evaluate(self, x: np.ndarray, rescale=True):
        
        if rescale:
            new_bin_width = x[1]-x[0]
            params = self.rescale(new_bin_width).params
        else: params = self.params

        return gaussian(x, *params)


    def from_dict(params_dict: dict):

        amplitude = params_dict['amp']
        mean = params_dict['mean']
        std = params_dict['std']

        if 'bin_width' in params_dict:
            bin_width = params_dict['bin_width']
        else: bin_width = None

        if 'cov_matrix' in params_dict:
            cov_matrix = params_dict['cov_matrix']
        else: cov_matrix = None
        
        return GaussianPeak(amplitude, mean, std, bin_width, cov_matrix)


    def integrate(self):

        integrated = self.amplitude * self.std * R2PI / self.bin_width

        if self.cov_matrix is None:
            err_integrated = None
        else:
            var_amp = self.cov_matrix[0,0]
            var_std = self.cov_matrix[2,2]
            cov_amp_std = self.cov_matrix[0,2]

            v1 = self.std**2 * var_amp
            v2 = 2 * self.std * self.amplitude * cov_amp_std
            v3 = self.amplitude**2 * var_std

            err_integrated = R2PI/self.bin_width * np.sqrt(v1+v2+v3)

        return integrated, err_integrated


    def rescale(self, new_bin_width):
        new_amplitude = new_bin_width * self.amplitude / self.bin_width

        return GaussianPeak(new_amplitude, self.mean, self.std, new_bin_width)


class NGaussianPeaks():
    
    def __init__(self, peaks: list, bin_width=None, cov_matrix=None, same_std=False):
        
        self.n = len(peaks)

        if all([type(peak)==dict for peak in peaks]):
            self.peaks = []
            for peak in peaks:
                self.peaks.append(GaussianPeak.from_dict(peak))

        elif all([type(peak)==GaussianPeak for peak in peaks]):
            self.peaks = peaks

        else: 
            raise TypeError(f'type(s) {[type(peak) for peak in peaks]} not supported in NGaussianPeaks.')


        if same_std:
            self.params = [ None for i in range(self.n*2+1) ]
            self.params[0] = peaks[0].std

            for i, peak in enumerate(self.peaks):
                self.params[i*2+1] = peak.amplitude
                self.params[i*2+2] = peak.mean

        else:
            self.params = [ None for i in range(self.n*3) ]
            
            for i, peak in enumerate(self.peaks):
                self.params[i*3] = peak.amplitude
                self.params[i*3+1] = peak.mean
                self.params[i*3+2] = peak.std

        self.cov_matrix = cov_matrix
        self.bin_width = bin_width
        self.same_std = same_std


    def from_dict(params_dict: dict):

        n = 0
        peaks = []
        while True:
            if f'params_{n}' in params_dict:
                peaks.append(GaussianPeak.from_dict(params_dict[f'params_{n}']))
                n += 1
            else: break

        if 'bin_width' in params_dict:
            for peak in peaks:
                peak.bin_width = params_dict['bin_width']

        if 'cov_matrix' in params_dict:
            cov_matrix = params_dict['cov_matrix']
        else: cov_matrix = None

        return NGaussianPeaks(peaks, cov_matrix)
    

    def fit(self, hist, xmin=None, xmax=None, ax=None, bound_gain=False, tol=.3):

        ngfit = n_gaussian_fit(hist, init_guess=self.params, ax=ax, 
                               xmin=xmin, xmax=xmax, same_std=self.same_std, 
                               bound_gain=bound_gain, tol=tol)
        return ngfit

    
    def rescale(self, new_bin_width):
        new_peak_list = []
        for peak in self.peaks:
            new_peak = peak.rescale(new_bin_width)
            new_peak_list.append(new_peak)
        return NGaussianPeaks(new_peak_list, bin_width=new_bin_width, cov_matrix=self.cov_matrix, same_std=self.same_std)


    def evaluate(self, x: np.ndarray, rescale=True):
        
        if rescale:
            new_bin_width = x[1]-x[0]
            params = self.rescale(new_bin_width).params
        else: params = self.params

        if self.same_std:
            fun = tied_n_gaussians
        else:
            fun = n_gaussians

        return fun(x, *params)


    def integrate(self):

        # initialize output dictionary
        d = {}

        # compute integrated peaks
        integrated = 0
        for i, peak in enumerate(self.peaks):
            d[f'N{i}'] = peak.amplitude * peak.std * R2PI / peak.bin_width
            integrated += d[f'N{i}']
        d['N'] = integrated

        # compute covariance matrix
        if self.cov_matrix is None:
            d['cov_matrix'] = None

        else:
            # follow error propagation formula
            n = self.n
            d['cov_matrix'] = np.zeros((n,n))

            for i in range(n):
                
                Ai = self.peaks[i].amplitude
                si = self.peaks[i].std

                for j in range(n):
                    Aj = self.peaks[j].amplitude
                    sj = self.peaks[j].std

                    if self.same_std:
                        v1 = Ai*Aj*self.cov_matrix[0,0]
                        v2 = si*Aj*self.cov_matrix[i*2+1,0]
                        v3 = Ai*sj*self.cov_matrix[0,i*2+1]
                        v4 = si*sj*self.cov_matrix[i*2+1,j*2+1]

                    else:
                        v1 = Ai*Aj*self.cov_matrix[i*3+2,j*3+2]
                        v2 = si*Aj*self.cov_matrix[i*3,j*3+2]
                        v3 = Ai*sj*self.cov_matrix[i*3+2,j*3]
                        v4 = si*sj*self.cov_matrix[i*3,j*3]

                    d['cov_matrix'][i,j] = v1 + v2 + v3 + v4

            d['cov_matrix'] = d['cov_matrix'] * 2*np.pi /self.bin_width**2
            d['N_err'] = np.sqrt(d['cov_matrix'].sum())

        return d


# evaluation functions
def gaussian(x, amplitude, mu, sigma):
    return amplitude * np.exp(-0.5*((x-mu)/sigma)**2)


def n_gaussians(x, *params):

    if len(params) % 3 != 0:
        raise ValueError('`params` length should be a multiple of 3.')

    n = len(params) // 3
    evaluated_gaussians = []

    for i in range(n):
        this_params = params[i*3:(i+1)*3]
        evaluated_gaussians.append(gaussian(x, *this_params))

    return sum(evaluated_gaussians)


def tied_n_gaussians(x, *params):

    if len(params) % 2 != 1:
        raise ValueError('`params` length should be odd (2n per gaussian + std).')
    
    # number of parameters per gaussian is 2
    n = (len(params)-1) // 2

    # first param is std
    sparams = [ p for i in range(n) for p in [params[i*2+1], params[i*2+2], params[0]] ]

    evaluated_gaussians = []

    for i in range(n):
        this_params = sparams[i*3:(i+1)*3]
        evaluated_gaussians.append(gaussian(x, *this_params))

    return sum(evaluated_gaussians)


# perform a gaussian fit on a given histogram
def _parse_guess(guess):
    if type(guess) == list:
        if len(guess) == 3:
            return guess
        else: raise ValueError('length of `init_guess` must be 3.')
    
    parsed_guess = [None,None,None]
    if type(guess) == dict:
        if 'amp' in guess: parsed_guess[0] = guess['amp']
        if 'mean' in guess: parsed_guess[1] = guess['mean']
        if 'std' in guess: parsed_guess[2] = guess['std']

    elif guess is not None:
        raise TypeError('`init_guess` should be dict, list or `None`.')

    return parsed_guess


def single_gaussian_fit(hist, xmin=None, xmax=None, ax=None, plot=False,
                        init_guess=None):
    """Perform a gaussian fit on a given histogram.

    Parameters
    -----------
    hist : np.ndarray
        the data of the histogram in the form of a numpy array. Must be of shape (2,`n`) with `n` the number of bins. The first element must contain the values of the bin centers and the second element the number of counts of each bin.
    xmin : scalar, optional
        bins with center below this value will be ignored for the fit.
    xmax : scalar, optional
        bins with center above this value will be ignored for the fit.
    ax : matplotlib.Axes, optional
        if given, the fit will be plotted in this Axes. If `None` (default) and `plot` is `False`, will perform the fit but not plot
    plot : bool, optional
        whether to create a new plot with the histogram and the fit. Ignored if `ax` is not `None`.
    init_guess : list or dict, optional
        if list, `init_guess[0]` should be the guess for the amplitude of the gaussian, `init_guess[1]` the mean and `init_guess[2]` the standard deviation. If dict, the corresponding keys are `amp`, `mean` and `std`.  If `None` (default), will try to infer these guesses from the data. 

    Returns
    -------
    GaussianPeak
        the result of the fit in the form of a GaussianPeak
        
    Raises
    ------
    TypeError
        if `hist` is not of shape (2,n).
    """

    if hist.shape[0] != 2:
        raise TypeError('`hist.shape` must be (2,n).')

    hist_x = hist[0]
    hist_y = hist[1]
    bin_width = hist[0,1] - hist[0,0]
    
    # mask the values below xmin and above xmax
    if xmin:
        mask = hist_x >= xmin
        hist_x = hist_x[mask]
        hist_y = hist_y[mask]
    if xmax:
        mask = hist_x < xmax
        hist_x = hist_x[mask]
        hist_y = hist_y[mask]
    
    # get the initial guess
    p0 = _parse_guess(init_guess)

    # infer missing from data
    if p0[0] == None: # amplitude
        p0[0] = hist_y.max()
    if p0[1] == None: # mean
        p0[1] = hist_x[hist_y == hist_y.max()][0]
    if p0[2] == None: # standard deviation
        p0[2] = hist_x[hist_y > hist_y.max()/2][-1] - p0[1]
    
    # fit!
    popt, pcov = curve_fit(gaussian, hist_x, hist_y, p0=p0, bounds=([0, -np.inf, 0],np.inf))

    # plot
    evaluated_gaussian = gaussian(hist_x, *popt)
    if ax is not None:
        ax.plot(hist_x, evaluated_gaussian,'g-', label='gaussian fit')
    elif plot==True:
        fig = plt.figure()
        bar_plot = plt.bar(hist[0], hist[1], width=bin_width)
        plt.plot(hist_x, evaluated_gaussian,'g-', label='gaussian fit')

    # save the fitted values
    # dict_of_data = {'amp': popt[0], 
    #                 'mean': popt[1], 
    #                 'std': popt[2], 
    #                 'cov_matrix': pcov,
    #                 'bin_width': bin_width}

    return GaussianPeak(*popt, bin_width=bin_width, cov_matrix=pcov)


def n_gaussian_fit(hist: np.ndarray, init_guess: list, ax=None, xmin=None, xmax=None,
                   same_std=False, bound_gain=False, tol=.3):
    """
    """

    if same_std:
        if len(init_guess) % 2 != 1:
            raise ValueError('`init_guess` length should be odd with `same_std=True`.')
        n = (len(init_guess)-1) // 2

        # fit bounds
        if bound_gain:
            mean_lower_bounds = [ init_guess[i*2+2]-np.abs(init_guess[i*2+2])*tol for i in range(n) ]
            mean_upper_bounds = [ init_guess[i*2+2]+np.abs(init_guess[i*2+2])*tol for i in range(n)]

            lower_bounds = np.concatenate([[0], [ p for i in range(n) for p in [0, mean_lower_bounds[i]]]])

            upper_bounds = np.concatenate([[np.inf], [ p for i in range(n) for p in [np.inf, mean_upper_bounds[i]]]])

        else:
            lower_bounds = np.concatenate([[0], [0, -np.inf]*n])
            upper_bounds = np.inf

        # function to fit
        fun = tied_n_gaussians

    else:
        if len(init_guess) % 3 != 0:
            raise ValueError('`init_guess` length should be a multiple of 3.')
        n = len(init_guess) // 3

        # fit bounds
        if bound_gain:
            mean_lower_bounds = [ init_guess[i*3+1]-init_guess[i*3+1]*tol for i in range(n) ]
            mean_upper_bounds = [ init_guess[i*3+1]+init_guess[i*3+1]*tol for i in range(n) ]

            lower_bounds = np.concatenate([ p for i in range(n) 
                                            for p in [0, mean_lower_bounds[i], 0]])

            upper_bounds = np.concatenate([ p for i in range(n) 
                                            for p in [np.inf, mean_upper_bounds[i], np.inf]])

        else:
            lower_bounds = np.array([0, -np.inf, 0]*n)
            upper_bounds = np.inf

        # function to fit
        fun = n_gaussians

    # translate histogram into x and y data
    hist_x = hist[0]
    hist_y = hist[1]
    # get the bin width
    bin_width = hist[0,1] - hist[0,0]

    # define the limits of the data
    if xmin:
        mask = np.where(hist_x >= xmin)
        hist_x = hist_x[mask]
        hist_y = hist_y[mask]
    if xmax:
        mask = np.where(hist_x < xmax)
        hist_x = hist_x[mask]
        hist_y = hist_y[mask]

    # parse the initial guess?

    # Fit
    popt, pcov = curve_fit(fun, hist_x, hist_y, p0=init_guess, bounds=(lower_bounds, upper_bounds))
    
    # create the NGaussianPeaks to return
    peaks = []
    if same_std:
        for i in range(n):
            peaks.append(GaussianPeak(popt[i*2+1], popt[i*2+2], popt[0], bin_width))

    else:
        for i in range(n):
            peaks.append(GaussianPeak(popt[i*3], popt[i*3+1], popt[i*3+2], bin_width))

    gfits = NGaussianPeaks(peaks, bin_width, pcov, same_std=same_std)

    # Plot
    if ax is not None:
        ax.plot(hist_x, fun(hist_x, *popt), 'r-', label=f'{n}-gaussian fit')

    return gfits