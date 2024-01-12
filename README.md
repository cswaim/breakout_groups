# Breakout Groups

## Overview

The breakout groups application is designed to assign attendees of an event into small groups.  There may be multiple sessions of small groups and the goal is to have as much interaction among the participants as possible, minimizing the number of times an attendee is in a group with the same other attendees.

The output is a 'card' for each attendee which identifies by session which group the attendee is assigned to.

Several reports are provided to analyze the effectiveness of the grouping algorithm - is it achieving the interactions desired.  These reports also allow for comparison of different algorithms.

## Table of Contents
1. [System Diagram](#system-diagram)
1. [Sessions Class](#sessions-class)
1. [Algorithm Implementation](#algorithm-implementation)
1. [Getting Started](#getting-started)

## System Diagram

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

*`import src.config as cfg`*

This module should be imported as the first application module.  The first import reads the config file (`data/breakout_groups.cfg`) and loads the runtime values.  If the cfg file does not exist, it is created with the default values.

The config creates a namespace so variables can be referenced as cfg.var.  The variable is defined with its default in the namespace.  A config file, *`breakout_groups.cfg`* is created on the first run if it does not exist.

Any changes to the cfg file in the data folder are local and override the defaults.

If a new variable is added or if the variable name changes, then the version number should be updated.  This will rewrite the local cfg file with the new variable.

## Sessions Class

### The Sessions

Two variables in the config file control which grouping algorithm is utilized:
```
[SYSTEM]
sys_group_algorithm = mmmmmm
sys_group_algorithn_class = cccccc
```
>where:
>* mmmmmm = the grouping algorithm module name without the .py located in src
>* cccccc = the class in the grouping algorithm module to be loaded

The Sessions Class will:
* dynamically call the sys_group_algorithm and load the class
* call the 'run' method of the class
* the module will return a dict of sessions in the format of
  ```
        {0:[[1,2,3],[4,5,6],....],
         1:[[6,3,8], [7,1,9],...],
        }
    one entry for each session.
  ```
* optionally: a dictionary of interactions will be returned.  An interaction is a dictionary
      with an entree for each attendee with a Counter.  The counter contains the number of interactions
      with other participants


### Algorithm Implementation

The sessions generation algorithm is implemented by having the sessions class load the grouping algorithm module and run a predefined function (run) in the algorithm module.

```mermaid
  classDiagram
      Sessions <|-- Random1
      Sessions <|-- Random2
      Sessions <|-- Perfect
      Sessions : +String grouping algorithm
      Sessions : +String grouping algorithm class
      Sessions : +Dict list of groups by session
      Sessions : -load_algorithm() Dict
      class Random1{
        +run():Dict
      }
      class Random2{
        +run():Dict
      }
      class Perfect{
        +run():Dict
      }
```

See *`src/sessions_model.py`* for a sample of the session algorithm

**TODO**: Pass exceptions or constraints to the grouping algorithm to modify the grouping interactions.  To be defined.


## Getting Started ##

### Summary of set up
* run git clone
* make sure all modules in requirements.txt are installed in python  
    recommend using virtualenv and install with pip install -r requirements.txt
* from the root directory of the project run:  
    ***python breakout_groups.py init***  
    (this creates the breakout_groups.cfg in the data folder)
* configure the configuration file (see [Configuration](#Configuration) below)

### Analyze the Event
To determine which algorithm performs best for an event, 
* Set up the config file for your event
* Run the algorithm compare job  
    ***python bg_algo_compare.py 1000 ***
    this will run each algorithm 1000 times with the settings in the config file
* At the end of the run the top three runs for each algorithm is printed and the seed is shown
* Select the run with the best interactions and set the seed in the config file
* Run the Application

### Run the Application
Help is available by passing the -h or --help parameter on the python cmd line 
* run the application:  
   ***python breakout_groups.py***  
   This will produce a set of reports and a pdf of the cards
* Print the cards on 3x5 cards to be given to attendees to direct them to the appropriate breakout group

### Configuration
* in the data folder change the configuration file breakout_groups.cfg
* set title, sub-title, date and breakout session names
* set the number of attendees, number of groups, group_size
* set the seed if you wish to reproduce specific results

### How to run tests
* from the root folder run:  
  ***pytest -vs***

