# Breakout Groups System Diagram

## Overview

The breakout groups application is designed to assign attendees of an event into small groups.  There may be multiple sessions of small groups and the goal is to have as much interaction among the participants as possible, minimizing the number of times an attendee is in a group with the same other attendees.

The output is a 'card' for each attendee which identifies by session which group the attendee is assigned to. 

Several reports are provided to analyze the effectiveness of the grouping alogrithm - is it achieving the interactions desired.  These reports also allow for comparision of different algorithms.

## System diagram

```mermaid
  graph TD;
      A[breakout_groups.py]-->B[config<br/>contains run parameters];
      B-->C[Events];
      C-->|grouping<br/>algorithm parm| D(Sessions);
      C-->E(Cards);
      C-->F(Reports);
      G(Constraints &<br/>Exceptions)-->D;
      D-->H(algo 1);
      D-->I(algo 2);
```
## Config

*import src.config as cfg*

This module should be imported as the first application module.  The first import reads the config file (data/breakout_groups.ini) and loads the runtime values.  If the ini file does not exist, it is created with the default values.

TODO: Add version number & grouping algrothrim parm.  When version changes, read ini file & rewrite with new information while perserving values set in parm.

## Sessions Class

The Sessions

One or two variables will be added to the config file:
```
[SYSTEM]
sys_group_algorithm = "mmmmmm"
sys_group_class = "ccccccccc"
```
>where:
>* mmmmmm = the grouping algorithm module name without the .py located in src
>* cccccc = the class name, if classes are used.

The Sessions Class will:
* dynamically call the sys_group_algorithm and load the class
* call the 'build_sessions' or 'run' function - pick one for all modules
* the module will return a dict of sessions in the format of
  ``` 
        {0:[[1,2,3],[4,5,6],....],
         1:[[6,3,8], [7,1,9],...],
        }
    one entry for each session.
  ```


### Design Approach (maybe - to be reviewed)

one approach is to use polymorphism to create different class with the same interface. 

```mermaid
  classDiagram
      Sessions <|-- Random1
      Sessions <|-- Random2
      Sessions <|-- Perfect
      Sessions : +String grouping algorithm
      Sessions : +Dict list of groups by session
      Sessions : +build_sessions() Dict
      class Random1{
        +build_sessions():Dict
      }
      class Random2{
        +build_sessions():Dict
      }
      class Perfect{
        +build_sessions():Dict
      }
```

The implementation of this concept can be done multiple ways.  Each approach assumes a parameter will be passed to identify the appropriate algorithm to use:

* creating an interface class and subclassing based on a parameter
* importing the appropriate module based on the parameter

**TODO**: Pass exceptions or constraints to the grouping algorithm to modify the grouping interactions.  To be defined.