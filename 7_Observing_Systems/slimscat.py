"""
.. module:: slimscat
   :platform: Unix
   :synopsis: Simulate effect of isotropic scattering.

.. moduleauthor:: Katherine Rosenfeldl <krosenf@gmail.com>


"""

import numpy as np
import struct
from scipy.interpolate import RectBivariateSpline
from scipy.ndimage.interpolation import rotate
import pdb

def generate_screen(nphi=2**13,dx=1.,wavelength=1.3e-6,\
    r=5.8e3,dpc=8.4e3,r_outer=1e7,r_inner=12.,alpha=5./3,\
    ips=10,screenfile='screen.bin'):
  '''
  Generate isotropic scattering screen. Defaults are for Sgr A*.

  :param nphi: number of pixels in original screen
  :param dx: pixel scale of image
  :param wavelength: observing wavelength [m]
  :param r: source-scatterer distance [pc]
  :param dpc: earth-source distance [pc]
  :param r_outer: outer turbulence scale [r0]
  :param r_inner: inner turbulence scale [r0]
  :param alpha: power-law index
  :param ips: image to screen pixel ratio
  :param screenfile: screen file name

  '''
  AU = 149597871e0   # 1 AU in km
  PC = 3.08567758e13 # 1 pc in km
  RADPERUAS = np.radians(1./(3600*1e6))
  d = dpc - r
  m = d/r
  r0 = 3136.67*(1.3e-6/wavelength)
  rf = np.sqrt(dpc*PC / (2*np.pi/wavelength)*m / (1+m)**2)
  screen_dx = 1e-6*dx*d*AU / ips
  screen_res = screen_dx / r0
  qmax = 1.*screen_res/r_inner
  qmin = 1.*screen_res/r_outer

  # frequency array, squared
  x2 = np.fft.fftfreq(nphi)**2

  # do not include anisotropy
  qy2, qx2 = np.meshgrid(x2, x2, indexing='ij')     # Y,X?
  rr = qx2+qy2
  rr[0,0] = 0.02  # normalize power

  # generating phases with given power spectrum
  size = (nphi,nphi) # shape of screen
  phi_t = (1/np.sqrt(2) * np.sqrt(np.exp(-1./(qmax**2)*rr) * (rr + qmin**2)**(-0.5*(alpha+2.)))) \
          * (np.random.normal(size=size) + 1j*np.random.normal(size=size))

  # calculate structure function
  phi = np.fft.fft2(phi_t).real

  # normalize structure function
  nrm = screen_dx/(r0*np.sqrt(1.*((phi[:-1,:] - phi[1:,:])**2).sum()/(nphi*(nphi-1))))
  phi *= nrm

  # calculate gradient
  #pdb.set_trace()
  imax = int(np.ceil((nphi-2.) / ips)) * ips
  dphi_x = (0.5 * rf**2 / (screen_dx**2 * ips )) * \
            (phi[:imax:ips,2::ips] - phi[:imax:ips,:imax:ips])
  dphi_y = (0.5 * rf**2 / (screen_dx**2 * ips )) * \
            (phi[2::ips,:imax:ips] - phi[:imax:ips,:imax:ips])

  # write out:
  f = open(screenfile,'wb')

  # write header size (4)
  f.write(struct.pack('i',2*4 + 4*8))
  # write array size (4)
  f.write(struct.pack('i',dphi_x.size))
  # write resolution element (8)
  f.write(struct.pack('d',dx))
  # write r0 (8)
  f.write(struct.pack('d',r0))
  # write wavelength (8)
  f.write(struct.pack('d',wavelength))
  # write m (8)
  f.write(struct.pack('d',m))

  # write gradient arrays
  for i in dphi_x.ravel():
    f.write(struct.pack('d',i))
  for i in dphi_y.ravel():
    f.write(struct.pack('d',i))
  f.close()

def fetch_hdr(screenfile='screen.bin'):
  '''
  Get screen header

  :param screenfile: (optional) screen file
  '''
  hdr = {}
  f = open(screenfile,'rb')
  hdr['hdrsize'] = struct.unpack('i',f.read(4))[0]
  hdr['nphi'] = int(np.sqrt(struct.unpack('i',f.read(4))[0]))
  hdr['dx'] = struct.unpack('d',f.read(8))[0]
  hdr['r0'] = struct.unpack('d',f.read(8))[0]
  hdr['wavelength'] = struct.unpack('d',f.read(8))[0]
  hdr['m'] = struct.unpack('d',f.read(8))[0]
  return hdr


def run_slimscat(isrc,idx,screenfile='screen.bin'):
  '''
  Scatter source image.

  :param isrc: source image
  :param idx: source pixel scale
  :param screenfile: screen file

  '''

  # read in screen parameters
  f = open(screenfile,'rb')
  hdrsize = struct.unpack('i',f.read(4))[0]
  nphi = int(np.sqrt(struct.unpack('i',f.read(4))[0]))
  dx   = struct.unpack('d',f.read(8))[0]
  f.seek(hdrsize)

  # filter image

  # check fov
  iny,inx = isrc.shape
  ny = int(np.floor(iny*idx/dx))
  nx = int(np.floor(inx*idx/dx))
  assert idx*max([iny,inx]) < nphi*dx

  # read in screen
  dphi_x = np.empty((ny,nx),dtype=np.float64)
  dphi_y = np.empty((ny,nx),dtype=np.float64)
  for i in range(ny):
    f.seek(hdrsize + i*8*1*nphi,0)
    dphi_x[i,:] = struct.unpack('{0:d}d'.format(nx),f.read(nx*8))
  for i in range(ny):
    f.seek(hdrsize + 8*nphi*nphi + i*8*1*nphi,0)
    dphi_y[i,:] = struct.unpack('{0:d}d'.format(nx),f.read(nx*8))

  f.close()

  # construct spline fit to source image
  f_isrc = RectBivariateSpline(idx/dx*(np.arange(iny) - 0.5*(iny-1)),\
                               idx/dx*(np.arange(inx) - 0.5*(inx-1)),\
                               isrc)

  # scatter pixel coordinates
  yy,_xx = np.meshgrid((np.arange(ny) - 0.5*(ny-1)),\
                       (np.arange(nx) - 0.5*(nx-1)),indexing='ij')
  _xx += dphi_x
  yy += dphi_y

  return f_isrc.ev(yy.flatten(),_xx.flatten()).reshape((ny,nx))
