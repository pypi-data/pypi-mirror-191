"""Skipper CCD image processing tools
"""

from .classes import Fits, maskedFits, CCD, UnknownCCDError
from .utilities import discard_empty_hdus, average_skipper_samples, correlated_noise_clustering, find_first_peak, read_ccd_params_json, remove_xtalk, split_image_parts, get_std_skipper
from ._auxiliary import recta
import numpy as np
import warnings
from astropy.io import fits
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


r2pi = np.sqrt(2*np.pi)


def skp2raw_lowmem(file_name: str, **kwargs):
    return skp2raw(file_name, **kwargs)


def skp2raw(img: Fits or str, subtract_median=True, ignore_samp=0, nsamp_name='NSAMP', 
            std=False, dtype='float32'):
    """Average the skipper samples of a Fits object or .Fits file.
    
    Parameters
    -----------
    img : Fits or str
        the Fits object that contains the .fits data and header. If a string, the name of the file to load and process.
    subtract_median : bool, optional
        whether to subtract the median of the data or not. Default: `True`.
    ignore_nsamp : int, optional
        how many samples to ignore before taking the average. Default is 0. Ignores the first `ignore_samp` samples; if the value is negative, ignores the last.
    nsamp_name : str, optional
        the name of the key in the .fits header that corresponds to the number of skipper samples in the image. Default: `NSAMP`.
    dtype: numpy dtype, optional (default: `'float32'`)
        the dtype in which the raw data will be saved.
    Returns
    -------
    Fits
        the Fits object with the averaged data and updated header.
    """

    # low-memory version
    if type(img) == str:
        with fits.open(img) as hdu_list:
            # discard empty hdus
            new_hdu_list = discard_empty_hdus(hdu_list)
            # get number of skipper samples
            Ns = int(new_hdu_list[0].header[nsamp_name])
            # average data in each hdu
            avg_data = [ average_skipper_samples(hdu.data, nsamp=Ns, ignore_samp=ignore_samp) 
                        for hdu in new_hdu_list ] 
            avg_data = np.array(avg_data)
            # get the std if requested
            std_data = [ get_std_skipper(hdu.data, nsamp=Ns, ignore_samp=ignore_samp) 
                        for hdu in new_hdu_list ] 
            std_data = np.array(std_data)
            # create the list of headers
            header = [ hdu.header for hdu in new_hdu_list ]
            # number of hdus
            nhdu = len(new_hdu_list)

    elif type(img) == Fits:
        # get number of skipper samples
        Ns = int(img.hdr[0][nsamp_name])
        # average
        avg_data = average_skipper_samples(img.data, nsamp=Ns, ignore_samp=ignore_samp)
        # std
        if std:
            std_data = get_std_skipper(hdu.data, nsamp=Ns, ignore_samp=ignore_samp)
        # set the alias for the header and number of hdus
        nhdu = img.nhdu
        header = img.hdr
    
    else: raise TypeError(f'Only `str` or `Fits` objects allowed as `img` argument (got {type(img)})')

    # subtract the hdu median (or not)
    if subtract_median: 
        data_median = np.median(avg_data, axis=(1,2))
        data = avg_data - data_median[:,None,None]
    else: data = avg_data
    
    # return the Fits object(s)
    raw_img = Fits(data=data.astype(dtype), header=header)
    raw_img.updateHeader('level', 'raw', 'averaged skipper samples')
    raw_img.updateHeader('ignsamp', ignore_samp, 'number of ignored skipper samples')
    if subtract_median:
        for hdu in range(nhdu):
            raw_img.updateHeader('median', data_median[hdu], 'subtracted median for this hdu', hdu=hdu)

    if std:
        std_img = Fits(data=std_data.astype(dtype), header=header)
        std_img.updateHeader('level', 'std', 'stddev of skipper samples')
        std_img.updateHeader('ignsamp', ignore_samp, 'number of ignored skipper samples')
        return raw_img, std_img
    
    return raw_img


def raw2proc(img: Fits, img_params, ccd=None, ccd_params_file=None,
             xtalk=True, subtract_baseline=True, return_ovsc=False):
    """Create a proc_ Fits from a raw_ Fits.

    Parameters
    ----------
    img : Fits
        the `raw_` img that will be converted to `proc`.
    img_params : dict


    """

    n_amps = img_params['total_amps']

    new_img = Fits(data=img.data[:n_amps], header=img.hdr)
    
    if ccd is None:
        ccd = CCD(read_ccd_params_json(ccd_params_file))

    # correct cross-talk (apply linear matrix)
    if xtalk:
        new_img.data = remove_xtalk(new_img.data, ccd.crosstalk_matrix)

    # split exposed and overscan, discard prescan
    # needed values: number of exposed pixel columns by hdu, prescan size, 
    # horizontal binning, number of amplifiers per row
    ncol = ccd.ccdncol // img_params['amps_per_row']
    nhbin = img_params['h_binning']
    prescan_size = ccd.prescan_size
  
    exposed_data, overscan_data = split_image_parts(new_img.data, ncol, 
                                prescan_size, h_binning=nhbin, n_amps=n_amps)

    # subtract the baseline. this depends on the method chosen
    noise_by_hdu = img_params['noise']
    gain_by_hdu = img_params['gain']
    
    # first peak method
    if (subtract_baseline==True) or (subtract_baseline=='global') or (subtract_baseline=='line'): 
        # global first peak
        global_data = np.concatenate((exposed_data, overscan_data), axis=2)
        for hdu, hdu_data in enumerate(global_data):
            try:
                gfit, hist = find_first_peak(hdu_data, width=noise_by_hdu[hdu])
            except Exception as e:
                print(f'Could not find first peak in hdu {hdu}. Not subtracting baseline.\nError: {e}.')
                continue
            new_img.data[hdu] -= gfit['mean']
            # first peak by line
            if subtract_baseline == 'line':
                for i, line in enumerate(hdu_data):
                    try:
                        gfit, hist = find_first_peak(line, width=noise_by_hdu[hdu], threshold=10)
                    except Exception as e:
                        print(f'Problem fitting first peak in hdu {hdu}, line {i}.')
                        continue
                    if np.abs(gfit['mean']>.5*gain_by_hdu[hdu]): continue
                    new_img.data[hdu, i] -= gfit['mean']

    if subtract_baseline == 'overscan':
        for hdu, hdu_data in enumerate(overscan_data):
            gfit, hist = find_first_peak(hdu_data, width=noise_by_hdu[hdu],
                                         threshold=10)
            new_img.data[hdu] -= gfit['mean']

    # other methods later ?

    # return exposed and maybe overscan images
    exposed_img = Fits(data=exposed_data, header=img.hdr)
    exposed_img.filename = 'proc_'+img.filename
    if return_ovsc:
        overscan_img = Fits(data=overscan_data, header=img.hdr)
        overscan_img.filename = 'ovsc_proc_'+img.filename
        return exposed_img, overscan_img
    return exposed_img


def proc2cal(img: Fits, verbose=False, ccd=None, gain_list=None,
                cal_errors='break', return_gain=False, N_gaussians=3):
    """Create a cal_ Fits from a proc_ Fits.
    
    """
    # get ccd properties if not given
    if ccd == None:
        ccd = get_ccd_properties(img)
    
    # check if image is a proc
    img_prop = get_img_properties(img)
    LEVEL = img_prop['level']
    if LEVEL != 'proc':
        print('Warning: \'proc\' was not found in the image header. ')

    if verbose:
        print('> Calibrating image...')

    zero_list = np.zeros(img.nhdu)

    # get gain: fit two or three gaussians
    gain_fit_flag = False
    if gain_list == None:
        gain_fit_flag = True
        if verbose:
            print('> gain list not given, will try to fit gaussians.')
        zero_list = []
        gain_list = []
        N_0e_list = []
        N_1e_list = []
        if N_gaussians == 3:
            N_2e_list = []
        errors_by_hdu = []
        for hdu in range(img.nhdu):	
            hist = img.getHistogram(hdu, xmin=-ccd.usual_gain_by_amp[hdu], 
                            xmax=ccd.usual_gain_by_amp[hdu]*2.5, nbins=300)
            bin_width = hist[hdu,0,1] - hist[hdu,0,0]
            # first gaussian fit will get important parameters
            if verbose:
                print('> Performing initial Gaussian fit in hdu {}...'.format(hdu)
                      , end=' ')
            try:
                initial_fit = img.gaussianFit(hdu, 
                                xmax=ccd.usual_gain_by_amp[hdu]*.5)
            except Exception as e:
                print('Error: Could not perform initial Gaussian fit in hdu {}. Skipping.'.format(hdu))
                if cal_errors != 'break':
                    errors_by_hdu.append(hdu)
                    gain_list.append(1)
                    continue
                else: return None

            if verbose: print('success!')
            zeroth_amplitude = initial_fit['amp']
            hdu_noise = initial_fit['std']

            first_amplitude = hist[hdu,1][hist[hdu,0]>ccd.usual_gain_by_amp[hdu]][0]

            if N_gaussians == 2:
                p0 = [zeroth_amplitude, 0, hdu_noise, 
                    first_amplitude, ccd.usual_gain_by_amp[hdu], hdu_noise]
                # fit!
                if verbose:
                    print('> Performing two Gaussian fits in hdu {}...'.format(hdu)
                        , end=' ')
                try:
                    this_fit_results = img.N_GaussianFit(2, hdu, p0=p0)
                except Exception as e:
                    print('Error: Could not perform two Gaussian fit in hdu {}. Skipping.'.format(hdu))
                    if cal_errors != 'break':
                        errors_by_hdu.append(hdu)
                        gain_list.append(1)
                        continue
                    else: return None

            elif N_gaussians == 3:
                # initialize three gaussian fit parameters
                second_amplitude = hist[hdu,1][hist[hdu,0]>2*ccd.usual_gain_by_amp[hdu]][0]
                p0 = [zeroth_amplitude, 0, hdu_noise, 
                    first_amplitude, ccd.usual_gain_by_amp[hdu], hdu_noise, 
                    second_amplitude, ccd.usual_gain_by_amp[hdu]*2, hdu_noise]
                # fit!
                if verbose:
                    print('> Performing three Gaussian fits in hdu {}...'.format(hdu)
                        , end=' ')
                try:
                    this_fit_results = img.N_GaussianFit(3, hdu, p0=p0)
                except Exception as e:
                    print('Error: Could not perform three Gaussian fit in hdu {}. Skipping.'.format(hdu))
                    if cal_errors != 'break':
                        errors_by_hdu.append(hdu)
                        gain_list.append(1)
                        continue
                    else: return None

            if verbose: print('success!')
            # get the interesting data
            zero = this_fit_results['params_0']['mean']
            gain = this_fit_results['params_1']['mean'] - zero
            N_0e = this_fit_results['params_0']['amp'] * this_fit_results['params_0']['std'] * r2pi / bin_width
            N_1e = this_fit_results['params_1']['amp'] * this_fit_results['params_1']['std'] * r2pi / bin_width
            if N_gaussians == 3:
                N_2e = this_fit_results['params_2']['amp'] * this_fit_results['params_2']['std'] * r2pi / bin_width
            # save it
            zero_list.append(zero)
            gain_list.append(gain)
            N_0e_list.append(N_0e)
            N_1e_list.append(N_1e)
            if N_gaussians == 3:
                N_2e_list.append(N_2e)
        if errors_by_hdu != []:
            print('> Could not calibrate hdu(s) ', end='')
            for e in errors_by_hdu:
                print('{}, '.format(e), end='')
            print('')

    # create calibrated data
    calibrated_data = img.data - np.array(zero_list)[:,None,None]
    calibrated_data = calibrated_data / np.array(gain_list)[:,None,None]
    
    # create a calibrated image
    calibrated_img = Fits(data=calibrated_data.astype('float32'), 
                            header=img.hdr)
    for hdu in range(img.nhdu):
        
        calibrated_img.updateHeader('gain', gain_list[hdu], 'fitted gain', hdu=hdu)
        if gain_fit_flag:
            calibrated_img.updateHeader('zero', zero_list[hdu], 'fitted zero electron mean', hdu=hdu)
            calibrated_img.updateHeader('N_0e', N_0e_list[hdu], 'number of pixels with 0 electrons', hdu=hdu)
            calibrated_img.updateHeader('N_1e', N_1e_list[hdu], 'number of pixels with 1 electron', hdu=hdu)
            if N_gaussians == 3:
                calibrated_img.updateHeader('N_2e', N_2e_list[hdu], 'number of pixels with 2 electrons', hdu=hdu)
    calibrated_img.updateHeader('imglevel', 'cal', 'image calibrated in electrons')

    if verbose: print('> All done! Returning ', end='')
    if return_gain:
        if verbose: print('calibrated Fits and gain list.')
        return calibrated_img, gain_list

    else:
        if verbose: print('calibrated Fits.')
        return calibrated_img


def cal2phys(cal_img: Fits, verbose=False, max_e=2, max_sum=4, plot=False,
             mask_val=None, apply2D=True):
    """Create a phys_ img from a cal_ img. Apply the clustering algorithm.  """

    # check if image is a cal
    img_prop = get_img_properties(cal_img)
    LEVEL = img_prop['level']
    if LEVEL != 'cal':
        print('Warning: \'cal\' was not found in the image header. ')

    # default mask value to nan
    if mask_val is None:
        mask_val = -1

    # apply first clustering
    if verbose:
        print('> Applying first clustering ({}-D)...'.format(cal_img.nhdu))
    phys_image, mask = correlated_noise_clustering(cal_img.data, max_e, max_sum, mask_val, plot)

    if apply2D and cal_img.data.shape[0] > 2:
        if verbose: print('> Applying 2D clustering...', flush=True)
        # first create a list of temporary images (will average them later)
        n_temp_images = ((cal_img.nhdu)*(cal_img.nhdu-1))//2
        temp_image_list = np.nan*np.ones((n_temp_images,cal_img.nhdu,(~mask).sum()))

        # apply 2D clustering
        n = 0
        for i in range(cal_img.nhdu-1):
            for j in range(i, cal_img.nhdu-1):
                if verbose: print('> > hdus {} & {}'.format(i,j+1), flush=True)
                image = np.array([cal_img.data[i,~mask], cal_img.data[j+1,~mask]])
                this_max_sum = max_sum
                errors_2d = True
                while errors_2d:
                    if this_max_sum < 1:
                        print('2-D clustering between hdus {} and {} failed.'.format(i,j+1))
                        temp_image = np.nan*np.ones((2,(~mask).sum()))
                        break
                    try:
                        temp_image, temp_mask = correlated_noise_clustering(
                            image, max_e=max_e, max_sum=this_max_sum, mask_val=np.nan, plot=plot)
                        errors_2d = False
                    except ValueError:
                        this_max_sum -= 1
                temp_image_list[n,i] = temp_image[0]
                temp_image_list[n,j+1] = temp_image[1]
                n += 1

        # now average 
        if verbose: print('> > Averaging and masking values...')
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', message='Mean of empty slice')
            avg_vals = np.nanmean(temp_image_list, axis=0)
        avg_vals[np.isnan(avg_vals)] = mask_val

        # check which values are integers, mask them if they are not
        integer_mask = (avg_vals == np.floor(avg_vals))
        avg_vals[~integer_mask] = mask_val

        # assign final values to the phys image
        phys_image[:,~mask] = avg_vals

    # round value of pixels above max_e+0.7
    if mask_val == -1:
        phys_image[cal_img.data>max_e+.7] = np.round(cal_img.data[cal_img.data>max_e+.7])

    # create the phys Fits
    phys_img = Fits(data=phys_image, header=cal_img.hdr)
    phys_img.updateHeader('imglevel', 'phys')

    return phys_img



# def infer_img_params(img: Fits):
    
#     params_dict = {
#         'ccdncol' : None,
#         'prescan_size' : 8,
#         'amps_per_row' : 2,
#         'total_amps' : 4,
#         'h_binning' : 1,
#         'crosstalk_matrix' : None,
#     }

#     header = img.hdr[0]

#     params_dict['ccdncol'] = header['ccdncol']
#     params_dict['prescan_size'] = header['ccdnpres']
#     params_dict['total_amps'] = len(img.data)
#     params_dict['amps_per_row'] = params_dict['total_amps'] // 2 
#     params_dict['h_binning'] = header['nbincol']

#     return params_dict


def generateMask(phys_img: Fits, structure=None, iterations=2,
                 serial_mask=False, bright_columns=False, event_charge=4,
                 mask_touching=False):

    """ Generate a mask for a Fits object.

    Parameters
    -----------
    phys_img : Fits
        the Fits object that contains the .fits data and header. Should be a 'phys'
        image, prints warning if not.
    structure : `numpy.ndarray` of shape (3,3), optional
        the structuring element to use in the binary dilation algorithm. If `None`
        (default), use a full structuring element (`np.ones((3,3))`) 
    iterations : int, optional
        the number of iterations for the binary dilation algorithm. Default is 2.
    serial_mask : bool, optional
        whether to apply or not a mask to try and filter serial register events.
        Default is `False`.
    bright_columns : bool, optional
        whether to apply or not a mask to try and filter bright columns.
        Default is `False`.
    event_charge : int, optional
        the charge in electrons of a pixel for it to be considered part of an event.
        Default is 4.
    mask_touching : bool, optional
        whether to mask pixels that touch with each other even if their charge is 
        lower than `event charge`. Default is False.

    Returns
    -------
    maskedFits
        the Fits object plus the mask

    """

    from skimage.morphology import remove_small_objects
    from scipy.ndimage import binary_dilation, label

    # check if image is a phys
    try:
        img_prop = get_img_properties(phys_img)
        LEVEL = img_prop['level']
        if LEVEL != 'phys':
            print('Warning: \'phys\' was not found in the image header. ')
    except KeyError:
        print('Warning: data not found in the image header.')

    # event mask structure matrix
    if structure is None:
        structure = np.ones((3,3)) # full

    # generate binary masks
    
    event_mask = phys_img.data>=event_charge    # pixels with events
    undef_mask = phys_img.data==-1              # cal2phys masked pixels
    total_mask = np.zeros_like(event_mask)

    for hdu in range(phys_img.nhdu):
        # sum all masks
        total_mask[hdu] = event_mask[hdu]
        if mask_touching:
            # this masks all events except those which are isolated
            nonempty_mask = phys_img.data!=0    # all but empty pixels
            remove_small_objects(nonempty_mask[hdu], min_size=2, connectivity=1, in_place=True)
            total_mask[hdu] += nonempty_mask[hdu]

        # apply binary dilation
        total_mask[hdu] = binary_dilation(total_mask[hdu], structure=structure, iterations=iterations)

        # include pixels with undefined value
        total_mask[hdu] += undef_mask[hdu]

    # generate the masked fits
    mimg = maskedFits(data=phys_img.data, mask=total_mask)

    # now mask serial register hits and bright columns
    for hdu in range(phys_img.nhdu):
        N_masked = -1
        while N_masked != 0:
            N_masked = 0

            if serial_mask:
                # serial register hits mask
                hcharge = mimg.data[hdu].mean(axis=1)
                serial_hit = hcharge>(hcharge.mean()+3*hcharge.std())
                serial_hit[1:]+=serial_hit[:-1] # extend to following line
                serial_hit_mask = np.repeat(serial_hit,mimg.data.shape[2]).reshape(mimg.data[hdu].shape)
                mimg.data[hdu].mask += serial_hit_mask
                N_masked += serial_hit.sum()

            if bright_columns:
                # bright columns mask
                vcharge = mimg.data[hdu].mean(axis=0)
                bright_col = vcharge>(vcharge.mean()+3*vcharge.std())
                bright_col_mask = np.repeat(bright_col,mimg.data.shape[1]).reshape(mimg.data[hdu].shape, order='F')
                mimg.data[hdu].mask += bright_col_mask
                N_masked += bright_col.sum()
    
    return mimg


def get_ccd_properties(img: Fits, verbose=False):
    """ Read the header of `img` and get the properties of the CCD, if it is known.

    Parameters
    -----------
    img : Fits
        the Fits object that contains the .fits data and header
    verbose : bool, optional
        whether to print what is being done or not

    Returns
    -------
    CCD
        an object with the CCD properties

    Raises
    ------
    UnknownCCDError
        If no known CCD matches the information in the header.
    """

    # get ccd params. 
    if verbose:
        print('> Getting CCD parameters...')

    ccdprops_dict = {}
    # these are fixed for each Skipper:
    CCDNCOL = int(img.hdr[0]['CCDNCOL'])
    CCDNROW = int(img.hdr[0]['CCDNROW'])

    ccdprops_dict['CCDNCOL'] = CCDNCOL
    ccdprops_dict['CCDNROW'] = CCDNROW
    
    if (CCDNCOL==724) and (CCDNROW==1248):
        ## toti params ##
        if verbose:
            print('Known CCD: \"Toti\".')
        ccdprops_dict['NAMP'] = 4
        ccdprops_dict['prescan_size'] = 8
        ccdprops_dict['usual_gain_by_amp'] = [605, 555, 519, 620]
        ccdprops_dict['crosstalk_matrix'] = 1/np.array([[1.0, 3362.0, 4069.0, 3991.0], 
                                    [3631.0, 1.0, 4337.0, 4393.0], 
                                    [4482.0, 4592.0, 1.0, 3793.0], 
                                    [4570.0, 4629.0, 3668.0, 1.0]])

    elif ((CCDNCOL==6144) or (CCDNCOL==684)) and (CCDNROW==1024): # first images, should be corrected later
        ## acds13 params ##
        if verbose:
            print('Known CCD: \"ACDS13\".')
        ccdprops_dict['NAMP'] = 4
        ccdprops_dict['prescan_size'] = 8
        ccdprops_dict['usual_gain_by_amp'] = [209, 200, 200, 200] # TBC
        ccdprops_dict['crosstalk_matrix'] = np.array(
            [[ 1.        , 1.7656e-04, 0., 0.],
             [ 1.6619e-04, 1.        , 0., 0.],
             [ 5.9560e-04, 6.0970e-04, 1., 0.],
             [ 0.        ,-4.8208e-04, 0., 1.]])
        ccdprops_dict['CCDNCOL'] = 684

    else:
        raise UnknownCCDError(ccdprops_dict)
    
    return CCD(ccdprops_dict)


def get_img_properties(img: Fits):
    # these depend on how the image was taken:
    NCOL = int(img.hdr[0]['NCOL'])
    NROW = int(img.hdr[0]['NROW'])
    # these keys do not always exist. Treat them as one if that is the case
    try:
        NVBIN = int(img.hdr[0]['NVBIN']) # in connie: NBINROW
    except KeyError:
        NVBIN = 1
    try:
        NHBIN = int(img.hdr[0]['NHBIN']) # in connie: NBINCOL
    except KeyError:
        NHBIN = 1
    try:
        LEVEL = img.hdr[0]['imglevel']
    except KeyError:
        LEVEL = 'unknown'

    return {'ncol': NCOL,
            'nrow': NROW,
            'nvbin': NVBIN, 
            'nhbin': NHBIN,
            'level': LEVEL,
            }


def _xtalk_iteration(x, y, slope_guess, gain, x_min):
    
    y_max = x*slope_guess + .5*gain

    mask = (x>x_min) & (y<y_max)
    xdata = x[mask].flatten()
    ydata = y[mask].flatten()

    popt, pcov = curve_fit(recta, xdata, ydata)
    
    return popt


def get_xtalk(img: Fits, h0: int, h1: int, slope_guess: float,
              gain: int or list, x_min: float, iterations=None, tol=1e-7,
              plot=False, verbose=False):
    """ Find cross-talk matrix element between hdus `h0` and `h1` for given image.

    Performs a linear fit between the values of pixels in `h0` and the same pixels in `h1` and returns the slope. Takes into account the gain and the initial guess to fit only those pixels that should have a value of zero in `h1`.

    Parameters
    -----------
    img : Fits
        the Fits object that contains the .fits data
    h0, h1 : int
        number of the Fits hdus to which compute the cross-talk matrix
    slope_guess : float
        initial guess for the cross-talk value
    gain : int or list
        gain of the given hdus. If `int`, apply the same for each hdu; if `list`, use each element of the list as gain for each hdu
    x_min : float
        the minimum value of pixels `h0` to perform the linear fit
    iterations : int or None, optional
        number of iterations of the algorithm. If `None` (default), iterate until convergence to a tolerance of `tol`
    tol : float, optional
        tolerance to reach if `iterations==None`, ignored otherwise. Default: `1e-7`.
    plot : bool, optional
        whether to plot the process or not. Default: False

    Returns
    -------
    float
        the slope of the fit after all iterations.
    """
    
    if verbose: print(f'> Analyzing cross-talk between hdus {h0} & {h1}...')

    x = img.data[h0]
    y = img.data[h1]

    new_slope = slope_guess

    if iterations == None:
        if verbose: print(f'>> Will iterate until reaching convergence value of {tol}.')
        converged = False
        i = 0
        while not converged:
            if i > 20:
                print('Too many iterations!')
                raise ValueError
            i += 1
            if verbose: print(f'>>> Iteration {i}')
            new_slope, origin = _xtalk_iteration(x, y, new_slope, gain, x_min)
            if np.abs(slope_guess-new_slope) < tol:
                converged = True
            slope_guess = new_slope
            
    
    else:
        if verbose: print(f'>> Will iterate {iterations} times.')
        for i in range(iterations):
            if verbose: print(f'>>> Iteration {i+1}')
            new_slope, origin = _xtalk_iteration(x, y, new_slope, gain, x_min, tol)
        i += 1

    if verbose: print('> Done!\n')

    if plot:
        fig, axs = plt.subplots(1,2,sharex=True,sharey=True,figsize=(12,6))

        axs[0].plot(x.flatten(), y.flatten(), 'o', markersize=2)
        axs[0].set_xlabel(f'hdu {h0}')
        axs[0].set_ylabel(f'hdu {h1}')

        xx = np.linspace(0, x.max(), 5)
        yy = xx*new_slope + origin

        newy = y - x*new_slope

        axs[0].plot(xx, xx*new_slope+.5*gain, 'gray', ls='--')
        axs[0].plot(xx, yy, 'g--')
        axs[0].text(x_min, x_min*new_slope + .5*gain, f'slope={new_slope:.3e}')

        axs[1].plot(x.flatten(), newy.flatten(), 'o', markersize=2)
        axs[1].set_xlabel(f'hdu {h0}')
        axs[1].set_ylabel(f'Corrected hdu {h1}')

        if new_slope < 0:
            plt.ylim(x.max()*new_slope - gain, gain)
        else:
            plt.ylim(-gain, x.max()*new_slope - gain)
        plt.suptitle(f'Iteration {i}')
        plt.show()

    return new_slope

