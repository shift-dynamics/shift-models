#!/usr/bin/env python

import argparse
import numpy as np
import json
import random
import string
import copy

template = {
    "model_parameters": {
        "version": "0.2",
        "units": {
            "angle": "radians",
            "length": "meters",
            "mass": "kilograms",
            "time": "seconds"
        },
        "gravity": [
            0.0,
            0.0,
            9.81
        ],
        "include_dir": [
          "."
        ],
        "simulation": {
            "integration_type": "ode113b",
            "time_span": 100,
            "time_step": 0.03,
            "relative_error": 1e-9,
            "absolute_error": 1e-9
        }
    },
    "fixed": {
        "frames": [
            {
                "name": "overhead_1",
                "T": [0.0, 0.0, -24.0],
                "R": [[1.0, 0.0, 0.0],
                      [0.0, -1.0, 0.0],
                      [0.0, 0.0, -1.0]]
            },
            {
                "name": "overhead_2",
                "T": [36.0, 36.0, -12.0],
                "R": [[1.0, 0.0, 0.0],
                      [0.0, -1.0, 0.0],
                      [0.0, 0.0, -1.0]]
            }
        ],
        "lights": [
            {
                "name": "overhead_1",
                "type": "point",
                "parent": ["fixed", "overhead_1"],
                "Ka": [0.2, 0.2, 0.2],
                "Kd": [1.0, 1.0, 1.0],
                "Ks": [0.8, 0.8, 0.8]
            },
            {
                "name": "overhead_2",
                "type": "point",
                "parent": ["fixed", "overhead_2"],
                "Ka": [0.2, 0.2, 0.2],
                "Kd": [1.0, 1.0, 1.0],
                "Ks": [0.8, 0.8, 0.8]
            }
        ]
    },
    "assemblies": [
        {
            "name": "collision_test",
            "active": True,
            "bodies": [],
            "joints": []
        }
    ]
}

body_template = {
    "name": "body1",
    "definition": [
        "stanford_bunny.obj"
    ],
    "collision_geometry": "convex_hull",
    "center_of_mass": [
        0.0,
        0.0,
        0.0
    ],
    "mass": 1.0,
    "moment_of_inertia": {
        "Izx": 0.0,
        "Ixx": 1.0,
        "Ixy": 0.0,
        "Izz": 1.0,
        "Iyy": 1.0,
        "Iyz": 0.0
    }
}

joint_template = {
    "name": "A",
    "body_frame_pairs": [
        [
          "fixed",
          "origin"
        ],
        [
          "body1",
          "origin"
        ]
    ],
    "type": "float",
    "initial_displacement": None,
    "initial_velocity": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
}


def rand_rotation_matrix(deflection=1.0, randnums=None):
    """
    Creates a random rotation matrix.

    deflection: the magnitude of the rotation. For 0, no rotation; for 1,
    competely random
    rotation. Small deflection => small perturbation.
    randnums: 3 random numbers in the range [0, 1]. If `None`, they will be
    auto-generated.
    """
    # from http://www.realtimerendering.com/resources/GraphicsGems/gemsiii/
    # rand_rotation.c

    if randnums is None:
        randnums = np.random.uniform(size=(3,))

    theta, phi, z = randnums

    theta = theta * 2.0 * deflection * np.pi  # Rotation about the pole (Z).
    phi = phi * 2.0 * np.pi  # For direction of pole deflection.
    z = z * 2.0 * deflection  # For magnitude of pole deflection.

    # Compute a vector V used for distributing points over the sphere
    # via the reflection I - V Transpose(V).  This formulation of V
    # will guarantee that if x[1] and x[2] are uniformly distributed,
    # the reflected points will be uniform on the sphere.  Note that V
    # has length sqrt(2) to eliminate the 2 in the Householder matrix.

    r = np.sqrt(z)
    Vx, Vy, Vz = V = (
        np.sin(phi) * r,
        np.cos(phi) * r,
        np.sqrt(2.0 - z)
        )

    st = np.sin(theta)
    ct = np.cos(theta)

    R = np.array(((ct, st, 0), (-st, ct, 0), (0, 0, 1)))

    # Construct the rotation matrix  ( V Transpose(V) - I ) R.
    M = (np.outer(V, V) - np.eye(3)).dot(R)
    return M.tolist()


def rand_vector(args):
    x_range = args.x_max - args.x_min
    y_range = args.y_max - args.y_min
    z_range = args.z_max - args.z_min
    x = x_range * np.random.uniform() + args.x_min
    y = y_range * np.random.uniform() + args.y_min
    z = z_range * np.random.uniform() + args.z_min
    return [x, y, z]


def rand_collision_model():
    return random.choice(["convex_hull", "ellipsoid", "sphere"])


def divmod_excel(n):
    a, b = divmod(n, 26)
    if b == 0:
        return a - 1, b + 26
    return a, b


def int_to_string(num):
    chars = []
    while num > 0:
        num, d = divmod_excel(num)
        chars.append(string.ascii_uppercase[d - 1])
    return ''.join(reversed(chars))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("body_count", type=int)
    parser.add_argument("x_min", type=float)
    parser.add_argument("x_max", type=float)
    parser.add_argument("y_min", type=float)
    parser.add_argument("y_max", type=float)
    parser.add_argument("z_min", type=float)
    parser.add_argument("z_max", type=float)
    args = parser.parse_args()

    json_file = template

    for i in range(args.body_count):
        body = copy.deepcopy(body_template)
        body_name = "body%s" % i
        body["name"] = body_name
        body["collision_geometry"] = rand_collision_model()

        joint = copy.copy(joint_template)
        joint["name"] = int_to_string(i + 1)
        body_frame_pairs = copy.deepcopy(joint["body_frame_pairs"])
        body_frame_pairs[1][0] = body_name
        joint["body_frame_pairs"] = body_frame_pairs
        joint["initial_displacement"] = {
            "R": rand_rotation_matrix(),
            "T": rand_vector(args)
        }

        json_file["assemblies"][0]["bodies"].append(body)
        json_file["assemblies"][0]["joints"].append(joint)

    print(json.dumps(json_file, sort_keys=False, indent=2))
