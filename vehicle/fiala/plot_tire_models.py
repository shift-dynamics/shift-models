#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import csv
from os import listdir
from os.path import isfile, join

if __name__ == "__main__":
    dat_files = [f for f in listdir('.') if isfile(f) and f.split('.')[-1] == 'dat']

    # six axes, returned as a 2-d array
    fig, axarr = plt.subplots(3, 2)
    fig.set_size_inches(8, 11)

    axarr[0, 0].set_title('Longitudinal Tire Force\nin Local SAE Frame\n')
    axarr[0, 0].set_ylabel('Force (N)')
    axarr[0, 0].set_xlabel('slip angle (degrees)')

    axarr[0, 1].set_title('Lateral Tire Force\nin Local SAE Frame\n')
    axarr[0, 1].set_ylabel('Force (N)')
    axarr[0, 1].set_xlabel('slip angle (degrees)')

    axarr[1, 0].set_title('Vertical Tire Force\nin Local SAE Frame')
    axarr[1, 0].set_ylabel('Force (N)')
    axarr[1, 0].set_xlabel('slip angle (degrees)')

    axarr[1, 1].set_title('X Tire Moment\nin Local SAE Frame')
    axarr[1, 1].set_ylabel('Moment (Nm)')
    axarr[1, 1].set_xlabel('slip angle (degrees)')

    axarr[2, 0].set_title('Y Tire Moment\n in Local SAE Frame')
    axarr[2, 0].set_ylabel('Moment (Nm)')
    axarr[2, 0].set_xlabel('slip angle (degrees)')

    axarr[2, 1].set_title('Z Tire Moment\n in Local SAE Frame')
    axarr[2, 1].set_ylabel('Moment (Nm)')
    axarr[2, 1].set_xlabel('slip angle (degrees)')

    fx_3000 = [0] * 6
    fy_3000 = [0] * 6
    fz_3000 = [0] * 6
    mx_3000 = [0] * 6
    my_3000 = [0] * 6
    mz_3000 = [0] * 6
    fx_4500 = [0] * 6
    fy_4500 = [0] * 6
    fz_4500 = [0] * 6
    mx_4500 = [0] * 6
    my_4500 = [0] * 6
    mz_4500 = [0] * 6

    slip_angles = np.arange(0, 11, 2)

    for dat_file in dat_files:

        vertical_load = dat_file.split(".")[0].split("_")[-1]
        if vertical_load == "3000" or vertical_load == "4500":
            vertical_load = float(vertical_load)
            slip_angle = float(dat_file.split(".")[0].split("_")[3])

            fx = []
            fy = []
            fz = []
            mx = []
            my = []
            mz = []

            with open(dat_file, "r") as f:
                dat_reader = csv.reader(f, delimiter=',')
                for row in dat_reader:
                    if float(row[0]) > 9.0:
                        fx.append(float(row[7]))
                        fy.append(float(row[8]))
                        fz.append(float(row[9]))
                        mx.append(float(row[10]))
                        my.append(float(row[11]))
                        mz.append(float(row[12]))

            if vertical_load == 4500:
                fx_4500[int(slip_angle / 2)] = np.mean(fx)
                fy_4500[int(slip_angle / 2)] = np.mean(fy)
                fz_4500[int(slip_angle / 2)] = np.mean(fz)
                mx_4500[int(slip_angle / 2)] = np.mean(mx)
                my_4500[int(slip_angle / 2)] = np.mean(my)
                mz_4500[int(slip_angle / 2)] = np.mean(mz)
            elif vertical_load == 3000:
                fx_3000[int(slip_angle / 2)] = np.mean(fx)
                fy_3000[int(slip_angle / 2)] = np.mean(fy)
                fz_3000[int(slip_angle / 2)] = np.mean(fz)
                mx_3000[int(slip_angle / 2)] = np.mean(mx)
                my_3000[int(slip_angle / 2)] = np.mean(my)
                mz_3000[int(slip_angle / 2)] = np.mean(mz)

            print(
            "slip_angle:", slip_angle, "vertical_load:", vertical_load,
            "fx", np.mean(fx), "fy", np.mean(fy), "fz", np.mean(fz),
            "mx", np.mean(mx), "my", np.mean(my), "mz", np.mean(mz))

    line1_handle = axarr[0, 0].plot(slip_angles, fx_3000, label="3000 N normal load")
    line2_handle = axarr[0, 0].plot(slip_angles, fx_4500, label="4500 N normal load")
    # axarr[0, 0].legend(loc='upper center', bbox_to_anchor=(0.5, 1.11),
    #       fancybox=False, shadow=False, ncol=2, fontsize=7)

    axarr[0, 1].plot(slip_angles, fy_3000, label="3000 N normal load")
    axarr[0, 1].plot(slip_angles, fy_4500, label="4500 N normal load")

    axarr[1, 0].plot(slip_angles, fz_3000, label="3000 N normal load")
    axarr[1, 0].plot(slip_angles, fz_4500, label="4500 N normal load")

    axarr[1, 1].plot(slip_angles, mx_3000, label="3000 N normal load")
    axarr[1, 1].plot(slip_angles, mx_4500, label="4500 N normal load")

    axarr[2, 0].plot(slip_angles, my_3000, label="3000 N normal load")
    axarr[2, 0].plot(slip_angles, my_4500, label="4500 N normal load")

    axarr[2, 1].plot(slip_angles, mz_3000, label="3000 N normal load")
    axarr[2, 1].plot(slip_angles, mz_4500, label="4500 N normal load")

    handles, labels = axarr[0, 1].get_legend_handles_labels()
    fig.legend(
        handles, labels, loc = 'lower center',
        bbox_to_anchor=(0.5, 0.0),
        ncol=2)

    fig.tight_layout()
    fig.subplots_adjust(top=0.9, bottom=0.1)

    fig.savefig('fiala_steady_state_tire_slip_angle.png')
