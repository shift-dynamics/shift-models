#!/usr/bin/env python

'''
The Shift "Context" Python class is used to script the creation
of Shift JSON files

'''

import shift


if __name__ == "__main__":
    cube = shift.Context()

    cube.add_include_dir(".")

    main_assembly = shift.Assembly("main_assembly")

    main_assembly.add_body(
        shift.Body("cube",
                   definition=["cube.obj", "cube.mtl"]))

    main_assembly.add_joint(
        shift.Joint("joint1",
                    body_frame_pairs=[
                        ["fixed", "origin"], ["cube", "origin"]]))

    cube.add_assembly(main_assembly)

    cube.write_to_file("cube.json")
