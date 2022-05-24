import pandas as pd
from itertools import groupby
import matplotlib.pyplot as plt

sykkel_raw = pd.read_csv('sykkel_tabell.csv', delimiter=';', usecols=['moned', 'skade'])

var_raw = pd.read_csv('var_tabell.csv', delimiter=';', usecols=['Time', 'Rain', 'Temperature', 'Wind', 'Snow'])

sykkel_data_all = []

for i in range(len(sykkel_raw['moned'])):
    year = sykkel_raw['moned'][i].split("M")[0]
    month = sykkel_raw['moned'][i].split("M")[1]

    sykkel_data_all.append([sykkel_raw['moned'][i], sykkel_raw['skade'][i]])

sykkel_data_grouped = []
for i, g in groupby(sorted(sykkel_data_all), key=lambda x: x[0]):
    sykkel_data_grouped.append([i, sum(v[1] for v in g)])

sykkel_data_final = []

for sykkel in sykkel_data_grouped:
    token = sykkel[0].split('M')
    time = int(token[1])
    hurt = int(sykkel[1])
    sykkel_data_final.append([time, hurt])

sykkel_data_average = []

for i, g in groupby(sorted(sykkel_data_final), key=lambda x: x[0]):
    sykkel_data_average.append([i, sum(v[1] for v in g) / 10])

over_all_time = [x[0] for x in sykkel_data_average]
sykkel_skade = [y[1] for y in sykkel_data_average]

temp_final = []
rain_final = []
snow_final = []
wind_final = []

for i in range(len(var_raw)):
    time = int(str(var_raw['Time'][i]).split('.')[0])
    temp = float(var_raw['Temperature'][i].replace(',', '.'))
    rain = float(var_raw['Rain'][i].replace(',', '.'))
    snow = float(var_raw['Snow'][i].replace(',', '.').replace('-', '0'))
    wind = float(var_raw['Wind'][i].replace(',', '.').replace('-', '0'))
    temp_final.append([time, temp])
    rain_final.append([time, rain])
    snow_final.append([time, snow])
    wind_final.append([time, wind])

temp_avg = []
for i, g in groupby(sorted(temp_final), key=lambda x: x[0]):
    temp_avg.append(sum(v[1] for v in g) / 10)

rain_avg = []
for i, g in groupby(sorted(rain_final), key=lambda x: x[0]):
    scale = 10
    rain_avg.append(sum(v[1] for v in g) / (10*scale))

snow_avg = []
for i, g in groupby(sorted(snow_final), key=lambda x: x[0]):
    snow_avg.append(sum(v[1] for v in g))


wind_avg = []
for i, g in groupby(sorted(wind_final), key=lambda x: x[0]):
    wind_avg.append(sum(v[1] for v in g) / 10)


weather_avg = []

for i in range(0, 12):
    avg = (temp_avg[i] + rain_avg[i] + snow_avg[i] + wind_avg[i])/4
    weather_avg.append(avg)

print(weather_avg)

ax = plt.axes()
plt.axhline(0, color='black')
plt.axvline(0, color='red')

plt.text(12.2,-1, 'Måned', rotation=0)
# plt.text(min(sykkel_data[1]), max(sykkel_data[1]), 'SKADE', rotation=0)



ax.set_xlim(1, 12)
ax.set_ylim(0, max(sykkel_skade)+10)

plt.plot(over_all_time, sykkel_skade, label="Skade")

# plt.plot(over_all_time, temp_avg, label="Temperatur")
# plt.plot(over_all_time, rain_avg, label="Nedbør")
# plt.plot(over_all_time, snow_avg, label="Sno")
# plt.plot(over_all_time, wind_avg, label="Vind")

# plt.plot(over_all_time, weather_avg, label="Var")

plt.legend(loc="upper left")
plt.show()

# sum = 0
# length = 0
# for x in sykkel_data_final:
#     if x[0] == 2:
#         sum += x[1]
#         length +=1
#
# print(sum/length)
