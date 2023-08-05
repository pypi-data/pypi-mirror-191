"""Analysis tools for image-like arrays"""

# imports
from ._auxiliary import binCenters
from .gfits import single_gaussian_fit, n_gaussian_fit, GaussianPeak, NGaussianPeaks
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import AutoMinorLocator
import json


# constants
R2PI = np.sqrt(2*np.pi)


# functions

### UTILITIES FOR FITS CLASS ###
# discard the empty hdus of an image
def discard_empty_hdus(hdu_list):
    new_hdu_list = []
    for i in range(len(hdu_list)):
        if hdu_list[i].data is None:
            continue
        new_hdu_list.append(hdu_list[i])
    return new_hdu_list


# show the image in a fancy way
def view_fancy(data: np.ndarray, logscale=False, colorbar=False, cmap='gnuplot', vmin=None, 
               vmax=None, ax=None, **fig_kw):
    """Show the image in a nice fashion.

    Parameters
    ----------
    data : 2-d np.ndarray
        the data of the image.
    logscale : bool, optional (default: False)
        whether to apply a logarithmic scale to the colormap.
    colorbar : bool, optional (default: False)
        whether to plot the colorbar.
    cmap : matplotlib colormap, optional
        what colormap to use. Default: 'gnuplot'.
    vmin : float, optional
        the minimum value for the colormap. Defaults to data.min().
    vmax : float, optional
        the maximum value for the colormap. Defaults to data.max().
    ax : matplotlib.Axes, optional
        if given, will not create a new figure but show the image in an existing axes.
    **fig_kw
        keyword arguments for plt.subplots. Ignored if `ax` is not `None`

    Returns
    -------
    matplotlib.AxesSubplot
        the Axes where the image was plotted.
    """

    # set the limits for the colormap
    if vmin == None:
        vmin = data.min()
    if vmax == None:
        vmax = data.max()
    
    # create the figure
    if ax is None:
        fig, ax = plt.subplots(**fig_kw)
    
    # define the colormap normalization
    if logscale:
        # vmin cannot be negative or zero
        if vmin <= 0:
            vmin = 1
        norm = colors.LogNorm(vmin=vmin, vmax=vmax, clip=True)
    else:
        norm = colors.Normalize(vmin=vmin, vmax=vmax, clip=True)
    
    im = ax.imshow(data, cmap=cmap, norm=norm)

    if colorbar:
        if colorbar==True:
            cbar_loc = 'bottom'
        else: cbar_loc = colorbar
        plt.colorbar(im, ax=ax, shrink=.7, location=cbar_loc)
    
    return ax


# generate a plottable histogram
def get_histogram(data: np.ndarray or np.ma.core.MaskedArray, xmin=None, xmax=None, nbins=100):
    """Generate the data of an histogram from a given array.

    Parameters
    -----------
    data : np.ndarray or np.ma.core.MaskedArray
        the data of the image.
    xmin : float, optional
        histogram will contain values above `xmin`. Defaults to the minimum value of `data`.
    xmin : float, optional
        histogram will contain values below `xmax`. Defaults to the maximum value of `data`.
    nbins : int, optional
        number of bins to generate. Default: 100.

    Returns
    -------
    np.ndarray of shape (2,nbins)
        the first element contains the centers of the bins and the second contains the counts.
    
    Raises
    ------
    TypeError
        if data is not a numpy array or masked array.
    """

    # by default, the histogram will be generated for the whole range of the data
    if xmin == None:
        xmin = data.min()
    if xmax == None:
        xmax = data.max()

    # define the binning
    bins = np.linspace(xmin,xmax,nbins+1)

    # slight difference between a common and a masked array
    if type(data) == np.ndarray:
        val, bins = np.histogram(data.flatten(), bins=bins)
    elif type(data) == np.ma.core.MaskedArray:
        val, bins = np.histogram(data.compressed(), bins=bins)
    else: raise TypeError('Expected numpy array as input.')

    # return
    bin_centers = binCenters(bins)
    return np.array([bin_centers, val])


# generate and plot an histogram
def plot_histogram(data: np.ndarray or np.ma.core.MaskedArray, xmin=None, xmax=None, nbins=100, ax=None, **kwargs):
    """Plot an histogram from a given array.

    Parameters
    -----------
    data : np.ndarray or np.ma.core.MaskedArray
        the data of the image.
    xmin : float, optional
        histogram will contain values above `xmin`. Defaults to the minimum value of `data`.
    xmin : float, optional
        histogram will contain values below `xmax`. Defaults to the maximum value of `data`.
    nbins : int, optional
        number of bins to generate. Default: 100.
    ax : matplotib.Axes, optional
        the axes where to plot the histogram. If None, will create a new figure.
    **kwargs
        keyword arguments passed to plt.subplots in case ax is None.

    Returns
    -------
    np.ndarray of shape (2,nbins)
        the first element contains the centers of the bins and the second contains the counts.
    matplotlib.Axes
        the Axes of the plotted histogram.
    
    Raises
    ------
    TypeError
        if data is not a numpy array or masked array.
    """

    hist = get_histogram(data, xmin=xmin, xmax=xmax, nbins=nbins)
    bin_width = hist[0,1] - hist[0,0]
    if ax is None:
        fig, ax = plt.subplots(**kwargs)
    bar_plot = ax.bar(hist[0], hist[1], width=bin_width)

    # logscale and grid by default
    ax.set_ylim(.9)
    ax.set_yscale('log')
    ax.grid()

    # xlim to limits of histogram
    ax.set_xlim(xmin, xmax)

    return hist, ax


### UTILITIES FOR SKP2RAW ###
# auxiliary functions for average_skipper_samples
def _process_skipper(data: np.ndarray, ncol, nrow, nsamp, ignore_samp, fun):
    # reshape to split samples of each pixel
    rdata = data.reshape([nrow, nsamp, ncol], order='F')
    rdata = rdata[:,ignore_samp:]
    # get the average
    return fun(rdata, axis=1)


def _assert_compatible_nsamp(orig_ncol, nsamp):
    # make sure we are not messing up with the value of nsamp
    if orig_ncol % nsamp != 0:
        raise ValueError(f'Cannot split {orig_ncol} values in array into chunks of size {nsamp} (not a multiple).')
    pass


def process_skipper_samples(data: np.ndarray, nsamp: int, ignore_samp=0, fun=np.mean):
    """Process the samples of a given `skp` image using the given function.

    Parameters
    -----------
    data : np.ndarray
        the data of the image in the form of a numpy array. Can be 2-d (single image) or 3-d (multiple images of the same shape).
    nsamp : int
        the number of skipper samples taken.
    ignore_samp : int, optional
        how many samples to ignore before taking the average. Default is 0. Ignores the first `ignore_samp` samples; if the value is negative, ignores the last. 
    fun : function
        what function to use to process the samples. It should be a numpy function as it should accept an `axis` argument. Default: `np.mean`.

    Returns
    -------
    np.ndarray
        the processed image in a numpy array of 2-d or 3-d, depending on the input.

    Raises
    ------
    TypeError
        if `data` is not 2-d or 3-d.
    ValueError
        if the number of columns in `data` is not a multiple of `nsamp`.
    """

    # process the samples of a simple image
    if len(data.shape) == 2:
        # assign nice names
        nrow = data.shape[0]
        orig_ncol = data.shape[1]
        # assert that nsamp is compatible with the data
        _assert_compatible_nsamp(orig_ncol, nsamp)
        ncol = orig_ncol // nsamp
        # do the processing
        return _process_skipper(data, ncol, nrow, nsamp, ignore_samp, fun)

    # process the samples of an image with several hdus
    elif len(data.shape) == 3:
        # assign nice names
        nhdus = data.shape[0]
        nrow = data.shape[1]
        orig_ncol = data.shape[2]
        # assert that nsamp is compatible with the data
        _assert_compatible_nsamp(orig_ncol, nsamp)
        ncol = orig_ncol // nsamp
        # initialize a new array
        new_data = np.zeros((nhdus, nrow, ncol))
        # get the average for each hdu
        for n in range(nhdus):
            new_data[n] = _process_skipper(data[n], ncol, nrow, nsamp, ignore_samp, fun)
        return new_data
    
    else:
        raise TypeError('Only 2- or 3-dimensional arrays should be passed as `data`.')


def average_skipper_samples(data: np.ndarray, nsamp: int, ignore_samp=0):
    """Average the samples of a given `skp` image.

    Parameters
    -----------
    data : np.ndarray
        the data of the image in the form of a numpy array. Can be 2-d (single image) or 3-d (multiple images of the same shape).
    nsamp : int
        the number of skipper samples taken.
    ignore_samp : int, optional
        how many samples to ignore before taking the average. Default is 0. Ignores the first `ignore_samp` samples; if the value is negative, ignores the last. 

    Returns
    -------
    np.ndarray
        the averaged image in a numpy array of 2-d or 3-d, depending on the input.

    Raises
    ------
    TypeError
        if `data` is not 2-d or 3-d.
    ValueError
        if the number of columns in `data` is not a multiple of `nsamp`.
    """

    return process_skipper_samples(data, nsamp, ignore_samp, np.mean)


def get_std_skipper(data: np.ndarray, nsamp: int, ignore_samp=0):
    """Get the standard deviation of the samples of a given `skp` image.

    Parameters
    -----------
    data : np.ndarray
        the data of the image in the form of a numpy array. Can be 2-d (single image) or 3-d (multiple images of the same shape).
    nsamp : int
        the number of skipper samples taken.
    ignore_samp : int, optional
        how many samples to ignore before taking the average. Default is 0. Ignores the first `ignore_samp` samples; if the value is negative, ignores the last. 

    Returns
    -------
    np.ndarray
        the standard deviation of the image in a numpy array of 2-d or 3-d, depending on the input.

    Raises
    ------
    TypeError
        if `data` is not 2-d or 3-d.
    ValueError
        if the number of columns in `data` is not a multiple of `nsamp`.
    """

    return process_skipper_samples(data, nsamp, ignore_samp, np.std)


### UTILITIES FOR RAW2PROC ###
# read image parameters from .json file
def read_img_params_json(file_name: str):
    """Read image parameters from .json file `file_name`.
    """

    params_dict = {
        'amps_per_row' : 2,
        'total_amps' : 4,
        'h_binning' : 1,
        'noise' : None,
        'gain' : None,
    }

    with open(file_name) as f:
        rdict = json.load(f)
        for key in params_dict.keys():
            if key in rdict: params_dict[key] = rdict[key]

    return params_dict


def read_ccd_params_json(file_name: str):
    """Read CCD parameters from .json file `file_name`.
    """

    params_dict = {
        'ccdncol' : None,
        'ccdnrow' : None,
        'prescan_size' : None,
        'total_amps' : None,
        'usual_gain_by_amp' : None,
        'crosstalk_matrix' : None,
    }

    with open(file_name) as f:
        rdict = json.load(f)
        for key in params_dict.keys():
            if key in rdict: params_dict[key] = rdict[key]

    return params_dict


# split horizontal overscan, discard prescan
def split_image_parts(data: np.ndarray, n_exposed: int, n_prescan: int, 
                      h_binning=1, n_amps=None):
    """Return views of data, one for the exposed part and another for the overscan.

    Parameters
    ----------
    data : np.ndarray
        the data of the image. Can be 2D or 3D.
    exposed_size : int
        the number of columns of the exposed data.
    prescan_size : int
        the number of columns of prescan.
    h_binning : int, optional
        number of horizontally binned pixels.
    n_amps : int or None
        the number of amplifiers if data is 3D. If None, defaults to data.shape[0].

    Returns
    -------
    tuple of two views of `data`: (exposed, overscan)
    """

    prescan_size = int(np.ceil(n_prescan/h_binning))
    exposed_size = int(np.floor(n_exposed/h_binning))
    overscan_size = int(np.floor((data.shape[-1] - n_prescan - n_exposed) / h_binning))

    if len(data.shape) == 2:
        exposed_data = data[:, prescan_size:prescan_size+exposed_size]
        overscan_data = data[:, -overscan_size:]

    elif len(data.shape) == 3:
        if n_amps == None: n_amps = data.shape[0]
        exposed_data = data[:n_amps, :, prescan_size:prescan_size+exposed_size]
        overscan_data = data[:n_amps, :, -overscan_size:]

    return exposed_data, overscan_data


# find the first gaussian peak in an image, hopefully the "0-electron" peak
def find_first_peak(data: np.ndarray, width: float, plot=False,
                    threshold=1000):
    """ Find and fit the first peak of the histogram of the given image.

    Parameters
    -----------
    data : np.ndarray or np.ma.core.MaskedArray
        the data of the image.
    width : float
        approximate width of the peak.
    plot : bool, optional
        whether to plot the process or not. Default: False.
    threshold: int, optional (Default: 1000)
        the minimum value of the pixel count to be considered a peak.

    Returns
    -------
    GaussianPeak
        the `GaussianPeak` with the results of the fit as parameters.
    numpy.ndarray
        the array containing the generated histogram
    matplotlib.Axes 
        the Axes object of the generated histogram if `plot==True`.
    """

    data = data.flatten()

    # start with a histogram of the whole data and "zoom in" the first bin 
    # that goes above threshold until reaching a reasonable scale
    xmin = data.min()
    xmax = data.max()
    hist = get_histogram(data, xmin=xmin, xmax=xmax)
    while (xmax - xmin) > 8*width:
        bin_to_zoom = hist[0][hist[1]>threshold][0]
        bin_width = hist[0,1]-hist[0,0]
        xmin = bin_to_zoom - bin_width/2 - width*3
        xmax = bin_to_zoom + bin_width/2 + width*3
        hist = get_histogram(data, xmin=xmin, xmax=xmax)

    # fit the gaussian
    gfit = single_gaussian_fit(hist, xmin=xmin, xmax=xmax, 
                              init_guess={'std': width})

    if plot:
        fig, ax = plt.subplots()
        bar_plot = ax.bar(hist[0], hist[1], width=gfit.bin_width)
        ax.plot(hist[0], gfit.evaluate(hist[0], rescale=False), 'g-')
        ax.set_ylim(.9)
        return gfit, hist, ax

    return gfit, hist


def find_n_peaks(data: np.ndarray, n: int, first_peak: GaussianPeak, approx_gain, 
                 plot=False, threshold=2):
    
    xmin = first_peak.mean - first_peak.std * 3
    xmax = first_peak.mean + (n-.75)*approx_gain + first_peak.std*3

    if plot:
        hist, ax = plot_histogram(data, xmin=xmin, xmax=xmax, nbins=50*n)
    else:
        hist = get_histogram(data, xmin=xmin, xmax=xmax, nbins=50*n)
        ax = None

    bin_width = hist[0,1] - hist[0,0]

    # width_min = first_peak.std / bin_width
    # width_max = first_peak.std*3 / bin_width

    # dist_min = first_peak.std / bin_width

    # peaks, props = find_peaks(hist[1], width=5,
    #                           distance=dist_min)

    # if peaks.size < n:
    #     raise ValueError(f'Could not find {n} peaks in data. `peaks`={peaks}')
    
    peak_list = [first_peak]

    for i in range(n-1):
        prev_peak = peak_list[-1]
        gev = prev_peak.evaluate(hist[0])
        mask = (hist[0] > prev_peak.mean) & (gev<hist[1]/2)
        fit_xmin = hist[0][mask][0]
        new_peak, nhist = find_first_peak(data[data>fit_xmin], 
                        width=prev_peak.std, threshold=threshold)
        peak_list.append(new_peak)
    
    if plot:
        for peak in peak_list:
            y = peak.evaluate(hist[0])
            ax.plot(hist[0], y, 'm-')

    gfits = NGaussianPeaks(peak_list)

    if plot:
        return gfits, hist, ax
    
    return gfits, hist


def remove_xtalk(data: np.ndarray, crosstalk_matrix: list or np.ndarray):
    
    if len(data.shape) != 3:
        raise TypeError('`data` must be a 3-d numpy array')
    
    nhdus = data.shape[0]
    new_data = np.dot(crosstalk_matrix, data.reshape((nhdus, -1))).reshape(data.shape)
    
    return new_data


def get_baseline(data: np.ndarray, xmin=None, xmax=None, method='median', verbose=True,
                 interpolate=False, **gaussian_kw):
    """
    """

    if len(data.shape) != 2:
        raise TypeError(f'Expected 2D numpy array, got {len(data.shape)}D.')

    nrows = data.shape[0]

    if method == 'gaussian':

        if 'width' not in gaussian_kw:
            raise ValueError('`width` parameter should be specified for `gaussian` method.')

        baseline = np.zeros(nrows)

        # fit a gaussian for each row
        for n in range(nrows):
            try:
                g0, hist = find_first_peak(data[n], **gaussian_kw)
            except Exception as e:
                if verbose:
                    print(f'Problem fitting gaussian in line {n}.')
                b = 0
            else:
                b = g0.mean
                if xmin is not None:
                    if b < xmin:
                        if verbose:
                            print(f'Line {n}: Mean value too low! Ignoring gaussian fit.')
                        b = 0
                if xmax is not None:
                    if b > xmax:
                        if verbose:
                            print(f'Line {n}: Mean value too high! Ignoring gaussian fit.')
                        b = 0
            finally:
                baseline[n] = b
        

    elif method=='median':

        # get the global median
        global_median = np.median(data)

        # get the median for each row
        median_per_row = np.median(data, axis=1)
        baseline = median_per_row.copy()

        # ignore high or low values
        if xmin is not None:
            baseline[median_per_row<xmin] = global_median
        if xmax is not None:
            baseline[median_per_row>xmax] = global_median
    
    else:
        raise ValueError('`method` can only be `gaussian` or `median`.')
    
    if interpolate:
        bErrors = False
        idx_failed = np.where(baseline==0)[0]
        for idx in idx_failed:
            try:
                baseline[idx] = (baseline[idx-1] + baseline[idx+1])*.5
            except:
                print(f'Interpolation failed for line {idx}')
                bErrors = True
        if bErrors:
            bsl_median = np.median(baseline)
            baseline[baseline==0] = bsl_median

    return baseline
        

### UTILITIES FOR CAL2PHYS
def correlated_noise_clustering(image: np.ndarray, max_e=2, max_sum=4, 
                                mask_val=-1, plot=False):
    
    from sklearn.mixture import GaussianMixture

    # number of clustering dimensions is same as hdus in the image
    N_dim = image.shape[0]
    # don't ask. This is magic. Initialize the means of the clusters
    means_by_dim = [np.arange(max_e+1) for i in range(N_dim)]
    mean_list = np.array(np.meshgrid(*means_by_dim)).T.reshape((-1,N_dim))
    # crop the clusters with sum > max_sum
    mean_list = mean_list[mean_list.sum(axis=1)<=max_sum]
   
    # generate the gaussian mixture model
    gmm = GaussianMixture(n_components=mean_list.shape[0], 
                          covariance_type='tied',
                          means_init=mean_list)
    
    # generate the data. First mask the image
    mask = image < max_e + 0.5
    mask = mask.all(axis=0)

    # mask if sum of values is greater than max_sum
    sum_mask = image.sum(axis=0) < max_sum+.7
    mask = np.all([sum_mask, mask], axis=0)

    train_data = image[:,mask].T

    # now begin the training!
    gmm.fit(train_data)

    # get the clusters
    predicted_clusters = gmm.predict(train_data)
    round_means = np.round(gmm.means_)

    # now generate the phys_ image (note that masked pixels get a value of mask_val)
    phys_image = mask_val*np.ones(image.shape,dtype='int')
    for i in range(N_dim):
        phys_image[i,mask] = round_means[:,i][predicted_clusters]

    # if we want to plot the clusters in a nice way
    if plot:
        color_index_list = _get_color_index(round_means, max_e)
        cluster_list = []
        for i in range(len(color_index_list)):
            cluster_list.append(color_index_list[i, predicted_clusters])
        axs = _plot_clusters(train_data, cluster_list, N_dim, max_e)
        return gmm, phys_image, axs

    return gmm, phys_image


def _plot_clusters(train_data, cluster_list, nhdus, max_e):
    # Initialize the plots
    fig, axs = plt.subplots(nhdus-1, nhdus-1, sharex=True, sharey=True, gridspec_kw={'hspace': 0, 'wspace': 0}, squeeze=False)
    # plot
    hidx = 0
    for j in range(nhdus-1):
        for i in range(j, nhdus-1):
            for n in range((max_e+1)**2+1):
                # plots a different set of data for each cluster
                axs[i][j].scatter(train_data[:,j][cluster_list[hidx]==n]
                                , train_data[:,i+1][cluster_list[hidx]==n]
                                , s=1)
            axs[i][j].grid()
            axs[i][j].set_xlim(-1,max_e+.5)
            axs[i][j].set_ylim(-1,max_e+.5)
            if j == 0: axs[i][j].set_ylabel('hdu {}'.format(i+1))
            if i == nhdus-2: axs[i][j].set_xlabel('hdu {}'.format(j))
            hidx += 1
    # delete the redundant axes
    for i in range(nhdus-1):
        for j in range(i+1, nhdus-1):
            fig.delaxes(axs[i][j])
    return axs


def _get_color_index(round_means: np.ndarray, max_e: int):
    nclusters = round_means.shape[0]
    nhdus = round_means.shape[1]
    
    color_index = np.zeros(((nhdus*(nhdus-1))//2, nclusters), dtype='uint8')

    hidx = 0
    for m in range(nhdus):
        for n in range(m+1, nhdus):
            cidx = 0
            for i in range(max_e+1):
                for j in range(max_e+1):
                    mask = (round_means[:,n]==i) & (round_means[:,m]==j)
                    color_index[hidx,mask] = cidx
                    cidx += 1
            hidx += 1
    
    return color_index


# other utilities. Note that these may be too specific
def plot_voltages(vdict, ax=None, legend=True, **kwargs):

    if type(vdict) != dict:
        vdict = get_voltages(vdict)

    xh = ['vh', 'tgh', 'hh', 'swh', 'ogh', 'vr', 'dgh']
    xl = ['vl', 'tgl', 'hl', 'swl', 'ogl', 'vr', 'dgl']

    yh = [vdict[x] for x in xh]
    yl = [vdict[x] for x in xl]

    xticks = ['v', 'tg', 'h', 'sw', 'og', 'vr', 'dg']

    xx = np.arange(len(xticks)+1)

    if ax is None:
        fig, ax = plt.subplots(**kwargs)

    for i in range(len(xticks)):
        ax.hlines(yh[i], xmin=xx[i], xmax=xx[i+1], colors='r')
        ax.hlines(yl[i], xmin=xx[i], xmax=xx[i+1], colors='b')

    _ = ax.set_xticks(xx[:-1]+.5, xticks)
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.tick_params(axis='x', which='major', length=0)
    ax.grid(linestyle='--', which='minor')
    ax.axhline(0, ls='--', c='k')

    if legend:
        s = voltages_to_string(vdict)
        ax.text(1.05, .5, s, linespacing=1.5, transform=ax.transAxes, 
                va='center', ha='left')
    ax.set_ylim(-10.5, 5.5)
    plt.tight_layout()


def get_voltages(header):
    d = {}
    d['vh'] = float(header['v1ah'])
    d['vl'] = float(header['v1al'])
    d['tgh'] = float(header['tgah'])
    d['tgl'] = float(header['tgal'])
    
    d['hh'] = float(header['h1ah'])
    d['hl'] = float(header['h1al'])
    d['swh'] = float(header['swah'])
    d['swl'] = float(header['swal'])
    d['ogh'] = float(header['ogah'])
    d['ogl'] = float(header['ogal'])
    d['vr'] = float(header['vr'])
    d['dgh'] = float(header['dgah'])
    d['dgl'] = float(header['dgal'])
    d['vdrain'] = float(header['vdrain'])

    d['rgh'] = float(header['rgah'])
    d['rgl'] = float(header['rgal'])
    d['vdd'] = float(header['vdd'])
    d['vsub'] = float(header['vsub'])

    return d


def voltages_to_string(vdict):
    s = ''
    for x in vdict.keys():
        s = s+f'{x}={vdict[x]:.1f}\n'

    return s

