import astropy.units as u

max_uvwave = 93873.4
res_rad = 1.0/max_uvwave*u.rad
res_arcsec = res_rad.to(u.arcsec)
print('Resolution: %.4f arcsec' %res_arcsec.value)
