# Loading bodies and joints of the Delta Robot


## Identifying Directed Acyclic Graph, Spanning Tree and Chord Constraints
The user-defined model is a list of bodies and joints. The input file specifies a Directed Graph (DG) with possible cycles. When the input file is loaded, the software identifies any user-specified joints that are not aligned with the spanning tree, and flips the sense as necessary, thereby converting the DG to a Directed Acyclic Graph (DAG) (i.e. with cycles removed). If any joints are identified to be not aligned with the spanning tree during this process, the user-defined sense of the inverse transformation is used across the joint to maintain the user-defined sign of the joint as specified in the input file. In the Delta robot model, all user-defined joints were specified to be aligned with the spanning tree and therefore it was not necessary to flip the sense of any joints.

When the user input file is loaded, all user-defined bodies and joints are loaded into a `bodies` and `joints` list in the software. The pseudocode to identify the DAG and sort bodies and joints in level-increasing order follows below. The process starts by identifying all user specified joints with a connection to the fixed inertial reference frame as:

    @require joints
    @return temp
    @return joints
    temp = []
    for joint in joints:
      if joint.parent is fixed:
        joint.sense = positive
        joints.pop(joint)
        temp.append(joint)
      else if joint.child is fixed:
        joint.sense = negative
        joints.pop(joint)
        temp.append(joint)


If no joints with a connection to the fixed inertial reference frame are specified above, additional logic must be carried to reference a model to the fixed inertial reference frame using a 6DOF float joint. The additional logic for this operation is not discussed here.

After the above operation has been carried out, the temporary list `temp` will have been seeded with the first joints connected to the fixed frame. Bodies and joints are systematically removed from the user's initial list of bodies and joints specified in an arbitrary user-defined order in the input file and appended to the new temporary list of bodies and joints (specified as `bodies_temp` and `joints_temp` respectively below). In the below pseudocode, the notation `pop(0)` indicates to remove the first element of a list and `pop(element)` indicates to remove a specified element from the list. The notation `append(element)` indicates to append an element to the end of the list. The process continues sorting and flipping the sense of joints until all user-defined joints have been processed.

    @require temp
    @require bodies
    @require joints
    @return bodies
    @return joints
    @return chord_constraints

    bodies_temp = []
    joints_temp = []
    chord_constraints = []

    while(temp):

      joint = temp.pop(0)
      joints_temp.append(joint)

      if joint.sense is positive:
        body = joint.child
      else if joint.sense is negative:
        body = joint.parent

      if body in bodies:
        bodies.pop(body)
        bodies_temp.append(body)
      else:
        virtualbody
        chordconstraint
        chordconstraint.parent = virtualbody
        if joint.sense is positive:
          chordconstraint.child = joint.child
          joint.child = virtualbody
        else if joint.sense is negative:
          chordconstraint.child = joint.parent
          joint.parent = virtualbody
        chord_constraints.append(chord_constraint)
        bodies_temp.append(virtualbody)

      for joint in joints:
        if joint.parent is body:
          joint.sense = positive
          joints.pop(joint)
          temp.append(joint)
        else if joint.child is body:
          joint.sense = negative
          joints.pop(joint)
          temp.append(joint)

    bodies = bodies_temp
    joints = joints_temp


Note that additional processing must be performed to identify and book-keep coordinate systems and shape matrices on bodies.


## Delta Robot Model

The delta robot contains 16 joints and 11 bodies and therefore has 5 chord loop constraints. The bodies and joints specified in the input file are as follows:


### Bodies

  -1. Fixed

  0\. Base

  1\. Upper Link 1

  2\. Upper Link 2

  3\. Upper Link 3

  4\. Lower Link 1

  5\. Lower Link 2

  6\. Lower Link 3

  7\. Lower Link 4

  8\. Lower Link 5

  9\. Lower Link 6

  10\. End-Effector


### Joints

  A. -1 &rarr; 0, rigid

  B. 0 &rarr; 1, Rz

  C. 0 &rarr; 3, Rz

  D. 0 &rarr; 2, Rz

  E. 1 &rarr; 5, spherical

  F. 1 &rarr; 9, spherical

  G. 3 &rarr; 6, spherical

  H. 3 &rarr; 7, spherical

  I. 2 &rarr; 8, spherical

  J. 2 &rarr; 4, spherical

  K. 5 &rarr; 10, spherical

  L. 9 &rarr; 10, spherical

  M. 6 &rarr; 10, spherical

  N. 7 &rarr; 10, spherical

  O. 8 &rarr; 10, spherical

  P. 4 &rarr; 10, spherical



## Cut Body Version

After processing the input file, the virtual bodies and chord constraints are imposed, resulting in the additional virtual bodies and chord constraints.

### Virtual Bodies

  [11]. Virtual Body 1

  [12]. Virtual Body 2

  [13]. Virtual Body 3

  [14]. Virtual Body 4

  [15]. Virtual Body 5



### Chord Constraints

  [0]. [11] &rarr; 10

  [1]. [12] &rarr; 10

  [2]. [13] &rarr; 10

  [3]. [14] &rarr; 10

  [4]. [15] &rarr; 10
