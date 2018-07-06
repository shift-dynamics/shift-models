Scripting model generation with Python
======================================

This directory contains an example of building a *Shift* `JSON <http://shift-dynamics.io/file_format/file_format.html>`_ model programmatically using Python.

The **shift.py** module contains *Shift* datastructures and utility functions. The module can be imported into another Python script as::

  import shift.py


An assembly can be added to the model as::

  main_assembly = shift.Assembly("main_assembly")


Bodies are added to the assembly as::

  main_assembly.add_body(
      shift.Body("cube",
                 definition=["cube.obj", "cube.mtl"]))


If no inertial properties are specified, as in the above example, the body will have have a mass of 1 and moments of inertia Ixx = Iyy = Izz = 1 and Ixy = Iyz = Izx = 0.

A joint is then added to reference the body to the fixed inertial frame::

  main_assembly.add_joint(
      shift.Joint("joint1",
                  body_frame_pairs=[
                      ["fixed", "origin"], ["cube", "origin"]]))


Now the assembly is added to the *Shift* context created earlier::

  cube.add_assembly(main_assembly)


And the file is written to disk as::

  cube.write_to_file("cube.json")


Refer to **cube.py** for the complete source code.

.. image:: cube.png
