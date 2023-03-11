# program to create an animated bar chart

import bar_chart_race as bcr
import pandas as pd

print(' ')
filename = '/Users/dennis/Documents/Python/Projects/Simulators/WorldSim/WorldSim_Y???_D???????_H??M??.csv'

outfile = 'WS_Y???_CHART_D??????_H??M??.gif'

df = pd.read_csv(filename)
df.set_index("Year", inplace=True)
df = df.apply(pd.to_numeric, downcast="integer", errors='coerce', axis=1)
df.replace(',', '', regex=True, inplace=True)

bcr.bar_chart_race(df=df,
                   title='Peeps World Simulator',
                   title_size=10,
                   orientation='h',
                   sort='desc',
                   n_bars=12,
                   bar_size=.99,
                   # fixed_order=True,
                   fixed_max=False,
                   steps_per_period=30,
                   period_length=1500,
                   interpolate_period=False,
                   label_bars=True,
                   cmap='Pastel',
                   figsize=(7, 5),
                   dpi=288,
                   bar_label_size=7,
                   tick_label_size=5,
                   filename=outfile,
                   shared_fontdict={'color': '.1'},
                   scale='linear',
                   fixed_order=['Population', 'Births', 'FoodG',
                                'Food', 'Famine', 'Spoild', 'Deaths', 'Natural', 'Starvation', 'Sudden',
                                'Disaster', 'Murders'],
                   period_label={'x': .99, 'y': .25,
                                 'ha': 'right', 'va': 'center'},
                   period_summary_func=lambda v, r: {'x': .99, 'y': .18,
                                                     's': 'Year',
                                                     'ha': 'right', 'size': 8, 'family': 'Courier New'}
                   )
print('\n >> Process complete \n')
