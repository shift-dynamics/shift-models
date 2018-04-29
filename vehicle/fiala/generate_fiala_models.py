#!/usr/bin/env python

import numpy as np
import json

def rot_z_matrix(rot_angle):

    return [[np.cos(np.radians(rot_angle)), -np.sin(np.radians(rot_angle)), 0],
            [np.sin(np.radians(rot_angle)), np.cos(np.radians(rot_angle)), 0],
            [0.0, 0.0, 1.0]]


if __name__ == "__main__":

    with open("../tire_fiala_control.json", "r") as f:
        model = json.load(f)

    # generate 3000 N normal force
    for i in np.arange(0, 11, 2):
        R = rot_z_matrix(i)
        model["assemblies"][0]["bodies"][1]["frames"][0]["R"] = R
        filename = "tire_fiala_control_%d_yaw_%d.json" % (i, 3000)
        with open(filename, "w") as f:
            json.dump(model, f, indent=4)

    # generate 4500 N normal force
    for i in np.arange(0, 11, 2):
        R = rot_z_matrix(i)
        model["assemblies"][0]["bodies"][1]["frames"][0]["R"] = R
        model["assemblies"][0]["joints"][1]["stiffness"][0] = -4500.0
        filename = "tire_fiala_control_%d_yaw_%d.json" % (i, 4500)
        with open(filename, "w") as f:
            json.dump(model, f, indent=4)
