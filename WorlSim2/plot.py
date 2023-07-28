import matplotlib.pyplot as plt
import pandas as pd
import os

os.system('clear')

data = pd.read_csv('WorldSim4_Y225_D20230728_H15M01.csv')
print(data)

df = pd.DataFrame(data)

year = df['Year'].values
pop = df['Population'].values
workers = df["Workers"].values

fig = plt.figure(dpi = 128, figsize = (15,6))
plt.plot(workers, color='red', label="Workers")
plt.plot(pop, color='blue', label='Population')

plt.title('Population vs Workers over the Years', fontsize=14)
plt.xlabel('Year', fontsize=14, color='green')
plt.ylabel('Population', fontsize=14, color='blue')
plt.yscale('linear')
plt.grid(True)
plt.legend(loc='best', title='Legend')
plt.show()
