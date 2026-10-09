"""Units-aware observational analysis of public Réunion TCCON data."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent

def to_unit(values,source,target):
    factors={'1':1.0,'mol/mol':1.0,'ppm':1e-6,'ppb':1e-9}
    if source not in factors or target not in factors:
        raise ValueError(f'Unsupported gas unit: {source} -> {target}')
    return np.asarray(values)*factors[source]/factors[target]

def aggregate_observations(frame):
    if frame.time.duplicated().any(): raise ValueError('Duplicate observation times')
    if not frame.time.is_monotonic_increasing: frame=frame.sort_values('time')
    d=frame.set_index('time').resample('D').agg({'xco2_ppm':['mean','median','std','count'],
        'xco_ppb':['mean','median','std'],'xch4_ppb':['mean','median','std']})
    d.columns=['_'.join(x) for x in d.columns]
    d=d.rename(columns={'xco2_ppm_count':'n_observations'})
    d.index.name='date'
    return d[d.n_observations>0]

def run():
    out=ROOT/'results'; out.mkdir(exist_ok=True)
    d=pd.read_csv(ROOT/'data/reunion_daily.csv',parse_dates=['date']).set_index('date')
    assert d.index.is_unique and (d.n_observations>0).all()
    assert d.xco2_ppm_mean.between(300,600).all(), 'Check CO2 units'
    monthly=d.resample('MS').agg({'xco2_ppm_mean':'mean','xco_ppb_mean':'mean','xch4_ppb_mean':'mean','n_observations':'sum'})
    monthly['observed_days']=d.xco2_ppm_mean.resample('MS').count()
    monthly.to_csv(out/'monthly_summary.csv')
    event=d.loc['2019-09-20':'2019-10-05'].dropna(subset=['xco2_ppm_mean','xco_ppb_mean'])
    # Correlation uses daily aggregates, not thousands of correlated scans.
    r=float(event.xco2_ppm_mean.corr(event.xco_ppb_mean))
    metrics={'source_observations':int(d.n_observations.sum()),'observed_days':len(d),
        'first_day':str(d.index.min().date()),'last_day':str(d.index.max().date()),
        'event_days':len(event),'event_daily_pearson_r_co2_co':r,
        'co2_unit':'ppm','co_unit':'ppb','ch4_unit':'ppb',
        'interpretation':'Descriptive co-variation only; no source attribution or satellite validation.'}
    (out/'metrics.json').write_text(json.dumps(metrics,indent=2))
    event.to_csv(out/'event_daily.csv')
    fig,axes=plt.subplots(3,1,figsize=(10,8),sharex=True)
    for ax,col,label,color in zip(axes,['xco2_ppm_mean','xco_ppb_mean','xch4_ppb_mean'],['XCO₂ (ppm)','XCO (ppb)','XCH₄ (ppb)'],['#126a8a','#ce6b32','#66549c']):
        ax.scatter(d.index,d[col],s=4,alpha=.3,color=color,label='Daily mean')
        ax.plot(monthly.index,monthly[col],color=color,lw=2,label='Mean of observed daily means')
        ax.set_ylabel(label); ax.grid(alpha=.15)
    axes[0].legend(loc='upper left'); axes[0].set_title('Réunion TCCON: observed days, March 2015–July 2020')
    fig.tight_layout();fig.savefig(out/'gas_timeseries.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(6.5,4.5))
    ax.scatter(event.xco_ppb_mean,event.xco2_ppm_mean,c=np.arange(len(event)),cmap='viridis',s=55)
    ax.set(xlabel='Daily XCO (ppb)',ylabel='Daily XCO₂ (ppm)',title=f'20 Sep–5 Oct 2019: n={len(event)} days; r={r:.3f}')
    ax.grid(alpha=.2);fig.tight_layout();fig.savefig(out/'event_covariation.png',dpi=160);plt.close(fig)
    return metrics

if __name__=='__main__': print(json.dumps(run(),indent=2))
