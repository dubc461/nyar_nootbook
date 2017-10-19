import time
import numpy as np
import matplotlib.pyplot as plt
from collections import ChainMap


def read_file(fun_file_dir):
    file_raw = open(fun_file_dir, 'r')
    file_data = file_raw.readlines()
    file_raw.close()
    return file_data


def get_room_data(fun_data_raw):
    data = [line for line in fun_data_raw if len(line.split()) > 1]
    roomdata = dict()
    for line in data:
        line = line.split()
        sampling_time = int(int(line[-1]) / 10) * 10 # 时差没有解决
        wet = float(line[-3])
        temp = float(line[-7])
        smooth_mark_default = 0
        roomdata[sampling_time] = (temp, wet, smooth_mark_default)
    return roomdata


def data_smooth(fun_roomdata):
    fun_roomdata_iter_k = iter(fun_roomdata.keys())
    fun_roomdata_smooth = dict()
    former_time = next(fun_roomdata_iter_k)
    try:
        while True:
            latter_time = next(fun_roomdata_iter_k)
            if (latter_time - former_time) >= 120:
                gap_time = former_time + 120
                gap_temp = (fun_roomdata[latter_time][0] + fun_roomdata[former_time][0]) / 2
                gap_wet = (fun_roomdata[latter_time][1] + fun_roomdata[former_time][1]) / 2
                fun_roomdata_smooth[gap_time] = (gap_temp, gap_wet, 1)
            former_time = latter_time
    except StopIteration:
        pass
    return fun_roomdata_smooth


def plot_scatter(roomdata_update, start_time, end_time):
    if start_time < end_time:
        start_time, end_time = end_time, start_time
    roomdata_iter_k = iter(roomdata_update.keys())
    plot_key = [pt for pt in roomdata_iter_k if start_time >= pt >= end_time]
    ##
    # 数据取样方式
    ##
    data_temp = np.array(list([roomdata_update.get(sampling_time, default=0)[0] for sampling_time in plot_key]))
    data_wet = np.array(list([roomdata_update.get(sampling_time, default=0)[1] for sampling_time in plot_key]))
    plot_key = np.array(plot_key)

    temp_plot = plt.scatter(plot_key, data_temp, marker='o', s=5, )
    wet_plot = plt.scatter(plot_key, data_wet, marker='o', s=5)


    plt.legend((temp_plot, wet_plot), ('Temperature', 'Relative Humidity'))
    ##
    # X轴坐标转换
    ##
    plt.ylim(0, 70)
    plt.show()


def plot_line(roomdata_update, start_time, end_time):
    if start_time < end_time:
        start_time, end_time = end_time, start_time

    roomdata_iter_k = iter(roomdata_update.keys())
    plot_key = [pt for pt in roomdata_iter_k if start_time >= pt >= end_time]
    plot_key = sorted(plot_key)
    ##
    # 数据取样方式
    ##
    data_temp = list([roomdata_update.get(sampling_time, default=0)[0] for sampling_time in plot_key])
    data_wet = list([roomdata_update.get(sampling_time, default=0)[1] for sampling_time in plot_key])
    plot_key = list(plot_key)

    temp_plot = plt.plot(plot_key, data_temp, label="Temperature")
    wet_plot = plt.plot(plot_key, data_wet, label="Relative Humidity")
    plt.legend()
    ##
    # X轴坐标转换
    ##
    plt.ylim(0, 70)
    plt.show()


file_dir = "./Temp_Wet.dat"
data_raw = read_file(file_dir)
roomdata = get_room_data(data_raw)
#过滤异常值， wet大于零，temp = [-10, 60]
roomdata_smooth = data_smooth(roomdata)
roomdata_update = ChainMap(roomdata, roomdata_smooth)


# mode1
# 提供起始时间以及取样方式
start_time = 1507813202
end_time = 1507813202 - 15000

#plot_scatter(roomdata_update, start_time, end_time)
plot_line(roomdata_update, start_time, end_time)
