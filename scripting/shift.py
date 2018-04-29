#!/usr/bin/env python

'''
The "Context" Python class is used script the creation
of JSON files

'''

import json


class Body(object):
    def __init__(
            self,
            body_name,
            definition=None,
            mass=1,
            center_of_mass=[0., 0., 0.],
            frames=None,
            moment_of_inertia={
                "Ixx": 1.0,
                "Ixy": 0.0,
                "Izx": 0.0,
                "Iyy": 1.0,
                "Iyz": 0.0,
                "Izz": 1.0
            }):
        self.name = body_name
        self.definition = definition
        self.mass = mass
        self.center_of_mass = center_of_mass
        self.frames = frames
        self.moment_of_inertia = moment_of_inertia


class Frame(object):
    def __init__(self, frame_name, T=None, R=None):
        self.name = frame_name
        self.T = T
        self.R = R


class Joint(object):
    def __init__(self,
                 joint_name,
                 body_frame_pairs=None,
                 joint_type="Rx",
                 initial_displacement=0.,
                 initial_velocity=0):

        self.name = joint_name
        self.body_frame_pairs = body_frame_pairs
        self.type = joint_type
        self.initial_displacement = initial_displacement
        self.initial_velocity = initial_velocity


class Assembly(object):
    def __init__(self,
                 assembly_name):

        self.name = assembly_name
        self.assemblies = []
        self.bodies = []
        self.joints = []
        self.active = True

    def add_body(self, body):
        self.bodies.append(body)

    def add_joint(self, joint):
        self.joints.append(joint)


class Context(object):
    def __init__(self):
        self.data = {}
        self.data["model_parameters"] = {
            "version": "2.0",
            "units": {
                "angle": "radians",
                "length": "meters",
                "mass": "kilograms",
                "time": "seconds"
            },
            "gravity": [0.0, 0, 9.81],
            "include_dir": []
        }
        self.data["assemblies"] = []

    def add_include_dir(self, include_dir_name):
        self.data["model_parameters"]["include_dir"].append(include_dir_name)

    def add_assembly(self, assembly_obj, path=None):
        assembly = {
            "name": assembly_obj.name,
            "assemblies": [],
            "bodies": [],
            "joints": [],
            "active": assembly_obj.active
        }
        for body_obj in assembly_obj.bodies:
            body = {
                "name": body_obj.name,
                "definition": body_obj.definition,
                "mass": body_obj.mass,
                "center_of_mass": body_obj.center_of_mass,
                "frames": body_obj.frames,
                "moment_of_inertia": body_obj.moment_of_inertia
            }
            assembly["bodies"].append(body)
        for joint_obj in assembly_obj.joints:
            joint = {
                "name": joint_obj.name,
                "body_frame_pairs": joint_obj.body_frame_pairs,
                "type": joint_obj.type,
                "initial_displacement": joint_obj.initial_displacement,
                "initial_velocity": joint_obj.initial_velocity
            }
            assembly["joints"].append(joint)
        if not path:
            self.data["assemblies"].append(assembly)
            for subassembly_obj in assembly_obj.assemblies:
                self.add_assembly(self, subassembly_obj, assembly)
        else:
            path["assemblies"].append(assembly)

    def write_to_file(self, filename):
        with open(filename, "w") as outfile:
            json.dump(self.data, outfile, indent=2)


if __name__ == "__main__":
    pass
