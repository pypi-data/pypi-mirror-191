"""Defines useful classes.

Classes
-------
Fits
	To easily manipulate data and headers from the images
maskedFits
	To work with masked images
CCD
    Provides an object with the CCD properties as attributes
"""

from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import os
from .utilities import discard_empty_hdus, get_histogram, n_gaussian_fit, plot_histogram, single_gaussian_fit, view_fancy


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class UnknownCCDError(Error):
    """Exception raised when the attributes of a .fits image
    do not match any of the listed CCDs.
    """

    def __init__(self, ccdprops_dict):
        print('No CCD found with the following properties:')
        print(ccdprops_dict)


class _BaseFits:
	"""
	Base class for FITS objects.

	...

	Attributes
	----------
	filename : str
		the name of the file from which the image was loaded
	nhdu : int
		the number of HDUs in the .fits file.
	data : list or 3-d np.ndarray
		list of the data for each HDU.
	hdr : list of astropy Headers
		list of headers, one for each HDU.
	lastHist : list of length nhdu
		list of the last histograms created, one element per HDU.
	"""

	def __init__(self, filename=None, data=None, header=None):
		"""Initialize the FITS object.

		Parameters
		----------
		filename : str, optional
			the name of the file to open.
		data : list or np.ndarray, optional
			if type is `list`, each element should be a 2-d `np.ndarray`. If it is a `np.ndarray`, it can be 2-d or 3-d. Ignored if `filename` is given.
		header : list or astropy fits.Header
			if type is `list`, each element should be an astropy header. Ignored if `filename` is given.

		Raises
		------
		TypeError:
			if `data` is not a list or a np.ndarray of 2 or 3-d.
		"""

		# create a Fits object from a file
		if filename is not None:
			# open with astropy
			with fits.open(filename) as hdu_list:
				new_hdu_list = discard_empty_hdus(hdu_list)
				# assign the data
				self.data = [ hdu.data for hdu in new_hdu_list ]
				# create a list of headers
				self.hdr = [ hdu.header for hdu in new_hdu_list ]

			# assign the filename
			self.filename = os.path.basename(filename)
			
			# check if all data are of the same size
			data_shape_list = np.empty((len(self.data), 2))
			for n, hdu_data in enumerate(self.data):
				data_shape_list[n] = hdu_data.shape
			# create a 3d numpy array if possible
			if np.all(data_shape_list==data_shape_list[0]): 
				self.data = np.array(self.data)
		
		# create a Fits object from data and given header
		else:
			if type(data) == list:
				self.data = data

			# check whether given array is 2 or 3-d
			elif len(data.shape) == 2:
				self.data = data[None,:]
			elif len(data.shape) == 3:
				self.data = data
			else: 
				raise TypeError('`data` should be a list or a np.ndarray of 2-d or 3-d.')

			# now assign the header(s)
			if type(header) == list:
				self.hdr = header
			else: self.hdr = [ header for i in range(len(self.data)) ]
			self.filename = ''

		# number of hdus
		self.nhdu = len(self.data)
		# initialize an empty list for the last histogram
		self.lastHist = [ None for i in range(self.nhdu) ]


	# Guarda la imagen a un archivo de nombre <filename>
	def save(self, filename, overwrite=True):
		"""
		Save the image to a file.

		Parameters
		----------
		filename : str
			The name of the file to which the new image will be saved.
		overwrite : bool, optional
			Whether to overwrite the file if it already exists or not
			(default is True)
		"""

		new_hdul = fits.HDUList()
		for hdu in range(self.nhdu):
			new_hdul.append(fits.ImageHDU(self.data[hdu], header=self.hdr[hdu]))
		new_hdul.writeto(filename, overwrite=overwrite)

	# permite visualizar una imagen fits (un solo hdu o todos)
	# imprime los fits dividiéndolos en los hdu y con escala de grises para ADU entre vmin y vmax (satura fuera de eso)
	def view(self, hdu=None, logscale=False, colorbar=True, save=False, pngname='foo.png', 
			 cmap='gnuplot', vmin=None, vmax=None, ax=None, **fig_kw):
		"""
		Visualize the image (one or all HDUs).

		Plots the images using `matplotlib` function `imshow`.

		Parameters
		----------
		hdu : int, list of int or None, optional
			The HDU(s) to view. If `None` (default), plots all available HDUs in a nice way.
		logscale : bool, optional
			Whether to use a logarithmic scale in the colormap or not. Default is `False`.
		colorbar : bool, optional
			Whether to plot the colorbar beside the images or not. Default is `True`.
		save : bool, optional
			Whether to save the plotted image or not. If `True`, saves to the file
			defined by the `pngname` parameter. Default is `False`.
		pngname : str, optional
			Name of the file to which save the plotted image. This parameter is
			ignored if `save` parameter is `False`. Default is `'foo.png'`.
		cmap : str, optional
			Name of the colormap to use. Must be one of those listed in `plt.colormaps()`. Default: `'gnuplot'`.
		vmin : int or float, optional
			Minimum value of the colormap. Values lesser than `vmin` will appear with
			the same color as the minimum.  If `None` (default), takes the minimum
			value of the whole image data (or of the selected HDU).
		vmax : int or float, optional
			Maximum value of the colormap. Values greater than `vmax` will appear 
			with the same color as the minimum.  If `None` (default), takes the 
			maximum value of the whole image data (or of the selected HDU).
		ax : matplotlib.Axes
			the Axes where to show the image. Ignored if `hdu` is a list or `None`.
		**fig_kw : 
			Keyword arguments passed to `plt.subplots`.

		Returns
		-------
		matplotlib.Axes or list of them
        	the Axes where the image(s) was(were) plotted.
		"""
		
		# If only one hdu given, plot only that one
		if type(hdu)==int:
			ax = view_fancy(self.data[hdu], logscale=logscale, colorbar=colorbar,
							cmap=cmap, vmin=vmin, vmax=vmax, ax=ax, **fig_kw)
			ax.set_title(self.filename+f'; hdu {hdu}')

		# if `hdu` not specified, view all hdus.
		else:
			if hdu == None:
				hdu_list = np.arange(self.nhdu)
			elif type(hdu)==list:
				hdu_list = hdu
			else: raise TypeError('`hdu` must be int, list or None.')

			# get the number of the subplots in columns and rows
			ncols = int(np.ceil(np.sqrt(len(hdu_list))))
			nrows = int(np.ceil(len(hdu_list) / ncols))
			
			# create the figure with all the axes
			fig, axs = plt.subplots(nrows, ncols, sharex=True, sharey=True, squeeze=False, 
									**fig_kw)
			ax = axs.ravel()
			
			# plot all the images
			for n, this_hdu in enumerate(hdu_list):
				view_fancy(self.data[this_hdu], logscale=logscale, colorbar=colorbar,
						   cmap=cmap, vmin=vmin, vmax=vmax, ax=ax[n])
				ax[n].set_title(f'hdu {this_hdu}')
			
			# delete exceding axes
			for n in range(len(hdu_list), nrows * ncols):
				fig.delaxes(axs[n // ncols][n % ncols])
			
			# figure title
			fig.suptitle(self.filename)

		plt.tight_layout()

		if save:
			plt.savefig(pngname)

		return ax


	# Plottea histograma del fits (uno o todos los hdu)
	def plotHistogram(self, hdu=None, xmin=None, xmax=None, nbins=100, save=False, 
					  pngname='foo.png', **fig_kw):
		"""Plot an histogram for one or all the hdus of this Fits object.

		Parameters
		-----------
		hdu : int, optional
			hdu to which plot the histogram. If `None`, plots it for all the hdus.
		xmin : float, optional
			histogram will contain values above `xmin`. Defaults to the minimum value of `data`.
		xmin : float, optional
			histogram will contain values below `xmax`. Defaults to the maximum value of `data`.
		nbins : int, optional
			number of bins to generate. Default: 100.
		save : bool, optional (default=False)
			whether to save the plot to a figure.
		pngname : str, optional
			if `save` is `True`, the name for the output file. Defaults to `foo.png`.
		**fig_kw
			keyword arguments passed to plt.subplots.

		Returns
		-------
		np.ndarray of shape (2,nbins)
			the first element contains the centers of the bins and the second contains the counts.
		matplotlib.Axes
			the Axes of the plotted histogram.
		"""

		# if no hdu is selected, plot all the histograms in a fancy way.
		if hdu == None:
			# get the number of the subplots in columns and rows
			ncols = int(np.ceil(np.sqrt(self.nhdu)))
			nrows = int(np.ceil(self.nhdu / ncols))

			# create the figure
			fig, axs = plt.subplots(nrows, ncols, constrained_layout=True, 
									squeeze=False, **fig_kw)
			ax = axs.ravel()

			for n in range(self.nhdu):
				# plot the histogram in the corresponding axes
				hist, foo = plot_histogram(self.data[n], xmin=xmin, xmax=xmax, nbins=nbins, 
										   ax=ax[n], **fig_kw)
				self.lastHist[n] = hist
				# nice settings
				ax[n].set_title('hdu '+str(n))
				ax[n].set_yscale('log')
				ax[n].set_ylim(ymin=0.9)
				ax[n].set_xlim(xmin,xmax)
				ax[n].grid()

			fig.suptitle(str(os.path.basename(self.filename)))
			
			# delete excess of axes
			for n in range(self.nhdu, nrows * ncols):
				fig.delaxes(axs[n // ncols][n % ncols])
			
			# save to png if requested
			if save:
				plt.savefig(pngname)
				plt.close()

			# return the histograms and the list of axes
			return self.lastHist, axs
			

		# histogram for only one hdu
		else:
			hist, ax = plot_histogram(self.data[hdu], xmin=xmin, xmax=xmax, nbins=nbins, **fig_kw)
			self.lastHist[hdu] = hist

			# nice settings
			plt.xlabel('ADU')
			plt.ylabel('pixel count')
			plt.yscale('log')
			plt.grid(True)
			plt.title(str(os.path.basename(self.filename))+' - hdu '+str(hdu))
			plt.ylim(ymin=0.9)
			plt.xlim(xmin,xmax)
			plt.tight_layout()

			# save to png if requested
			if save:
				plt.savefig(pngname)
				plt.close()

			# return the histogram and the axes
			return hist, ax
		


	# lo mismo que arriba pero sin plottear
	def getHistogram(self, hdu=None, xmin=None, xmax=None, nbins=100):
		"""Generate the histogram for one or all the hdus of this Fits object.

		Parameters
		-----------
		hdu : int, optional
			hdu to which compute the histogram. If `None`, computes it for all the hdus.
		xmin : float, optional
			histogram will contain values above `xmin`. Defaults to the minimum value of `self.data` or `self.data[hdu]` if selected.
		xmin : float, optional
			histogram will contain values below `xmax`. Defaults to the maximum value of `self.data` or `self.data[hdu]` if selected.
		nbins : int, optional
			number of bins to generate. Default: 100.

		Returns
		-------
		np.ndarray of shape (self.nhdu,2,nbins)
			the first element contains the centers of the bins and the second contains the counts.
		"""

		# if no hdu is selected, compute all the histograms.
		if hdu==None:
			for n in range(self.nhdu):
				self.lastHist[n] = get_histogram(self.data[n], xmin=xmin, xmax=xmax, nbins=nbins)

		# else compute only for that hdu.
		else:
			self.lastHist[hdu] = get_histogram(self.data[hdu], xmin=xmin, xmax=xmax, nbins=nbins)

		return self.lastHist


	# plottear los valores de cada hdu en función de los demás
	# para ver el ruido correlacionado
	def plotCorrelated(self, xmin=None, xmax=None):
		fig, axs = plt.subplots(self.nhdu-1, self.nhdu-1, sharex=True, sharey=True, gridspec_kw={'hspace': 0, 'wspace': 0}, squeeze=False)

		if xmin == None: xmin = self.data.min()
		if xmax == None: xmax = self.data.max()

		for j in range(self.nhdu-1):
			for i in range(j, self.nhdu-1):
				axs[i][j].scatter(self.data[j].flatten(), self.data[i+1].flatten(),
									s=1)
				axs[i][j].grid()
				axs[i][j].set_xlim(xmin,xmax)
				axs[i][j].set_ylim(xmin,xmax)
				if j == 0: axs[i][j].set_ylabel('hdu {}'.format(i+1))
				if i == self.nhdu-2: axs[i][j].set_xlabel('hdu {}'.format(j))
		
		for i in range(self.nhdu-1):
			for j in range(i+1, self.nhdu-1):
				fig.delaxes(axs[i][j])


	# Actualiza el header del fits con la variable y valor provistos. La variable debe ser un string.
	def updateHeader(self, variable, value, comment='', hdu=None):
		if hdu == None:
			if type(self.hdr) is list:
				for hdr in self.hdr:
					hdr[variable] = (value,comment)
			else:		
				self.hdr[variable] = (value,comment)
		else:
			self.hdr[hdu][variable] = (value,comment)

	# Genera un único hdu a partir de los 4, rotándolos y alineándolos como corresponde
	def generateOneImg(self):
		ldata = np.concatenate([self.data[0], np.flip(self.data[1], axis=0)], axis=0)
		rdata = np.concatenate([np.flip(self.data[3],axis=1), np.flip(self.data[2])], axis=0)
		return Fits(data=np.concatenate([ldata,rdata],axis=1)[None,:], header=self.hdr)

	# Ajuste gaussiano a partir de un histograma
	def gaussianFit(self, hdu, xmin=None, xmax=None, ax=None, plot=False, init_guess=None):
		"""Perform a gaussian fit on a given histogram.

		Parameters
		-----------
		hdu : int
			the number of the header for which the fit will be performed.
		xmin : scalar, optional
			bins with center below this value will be ignored for the fit.
		xmax : scalar, optional
			bins with center above this value will be ignored for the fit.
		ax : matplotlib.Axes, optional
			if given, the fit will be plotted in this Axes. If `None` (default) and `plot` is `False`, will perform the fit but not plot
		plot : bool, optional
			whether to create a new plot with the histogram and the fit. Ignored if `ax` is not `None`.
		init_guess : list, optional
			if given, `init_guess[0]` should be the guess for the amplitude of the gaussian, `init_guess[1]` the mean and `init_guess[2]` the standard deviation. If `None` (default), will try to infer these guesses from the data. 

		Returns
		-------
		GaussianPeak
            the result of the fit in the form of a GaussianPeak
		"""

		# get the last histogram made for this Fits object
		hist = self.lastHist[hdu]
		
		# fit
		return single_gaussian_fit(hist, xmin=xmin, xmax=xmax, ax=ax, plot=plot, init_guess=init_guess)


	def N_GaussianFit(self, hdu, p0, ax=None, xmin=None, xmax=None):
		# get the last histogram made for this FITS object
		hist = self.lastHist[hdu]
		
		# fit
		return n_gaussian_fit(hist, xmin=xmin, xmax=xmax, ax=ax, init_guess=p0)


class Fits(_BaseFits):

	# genera un maskedFITS con la misma metadata
	#def to_maskedFITS(self, mask):

	pass


# Clase para analizar imágenes enmascaradas
class maskedFits(_BaseFits):
	def __init__(self, data, mask):
		# Create masked array
		self.data = np.ma.masked_array(data=data, mask=mask)
		self.nhdu = data.shape[0]
		self.filename = ''
		self.lastHist = None
		# Create compressed data array(s)
		# if len(self.shape) == 3:
		# 	self.cdata = [self.data[n].compressed() for n in range(self.shape[0])]
		# elif len(self.shape) == 2:
		# 	self.cdata = self.data.compressed()
		# else:
		# 	print('Warning: wrong data shape (expected 2D or 3D): {}'.format(self.shape))

	def _plotHistogram(self, ax, hdu, xmin, xmax, nbins):
		return ax.hist(self.data[hdu].compressed(), bins=np.linspace(xmin,xmax,nbins+1))


	def changeMask(self, newmask):
		self.data = np.ma.masked_array(data=self.data.data, mask=newmask)
		# self.cdata = self.data.compressed()


class CCD:
    """Class with the properties of a CCD."""

    def __init__(self, ccdprops_dict):
        """ 
        Parameters
        ----------
        ccdprops_dict : dict
            a dictionary containing the following keys:
            'ccdncol': int
                number of columns in whole CCD
            'ccdnrow': int
                number of rows in whole CCD
            'total_amps': int
                number of amplifiers in CCD
            'prescan_size': int
                number of pixels of prescan
            'usual_gain_by_amp': list of length `namp`
                list of gain by amplifier, used to make the initial 
                guesses for the gaussian fits.
            'crosstalk_matrix': numpy array of shape [`namp`,`namp`]
                matrix to apply to remove cross-talk between amplifiers

        """

        self.ccdncol = ccdprops_dict['ccdncol']
        self.ccdnrow = ccdprops_dict['ccdnrow']
        self.total_amps = ccdprops_dict['total_amps']
        self.prescan_size = ccdprops_dict['prescan_size']
        self.usual_gain_by_amp = ccdprops_dict['usual_gain_by_amp']
        self.crosstalk_matrix = ccdprops_dict['crosstalk_matrix']


    def __repr__(self):
        return f"<CCD of {self.total_amps}x{self.ccdncol}x{self.ccdnrow}>"

