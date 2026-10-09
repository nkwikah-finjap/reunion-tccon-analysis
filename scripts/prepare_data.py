"""Download authoritative netCDF and regenerate the bundled daily summary."""
from pathlib import Path
import sys, urllib.request
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pandas as pd
import xarray as xr
from analysis import to_unit, aggregate_observations

ROOT=Path(__file__).resolve().parents[1]
URL='https://dap.ceda.ac.uk/neodc/tccon/tccon_mirror/data/reunion01/ggg2020/ra20150301_20200718.public.qc.nc?download=1'
if __name__=='__main__':
    raw=ROOT/'data/raw/reunion.nc'; raw.parent.mkdir(exist_ok=True)
    if not raw.exists(): urllib.request.urlretrieve(URL,raw)
    with xr.open_dataset(raw) as ds:
        f=pd.DataFrame({'time':pd.to_datetime(ds.time.values),
            'xco2_ppm':to_unit(ds.xco2.values,ds.xco2.attrs['units'],'ppm'),
            'xco_ppb':to_unit(ds.xco.values,ds.xco.attrs['units'],'ppb'),
            'xch4_ppb':to_unit(ds.xch4.values,ds.xch4.attrs['units'],'ppb')})
    aggregate_observations(f).to_csv(ROOT/'data/reunion_daily.csv',float_format='%.8f')
    print('Regenerated daily observations; gaps are preserved.')
