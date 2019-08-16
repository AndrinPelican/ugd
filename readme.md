# Uniform Graph Draw


This package implements random draw algorithm for networks. In particular it creates uniform samples of networks with a
given degree-sequence and partition constraints (fixed number of crossing edges/arrows between node-groups in partition).
The literature reefers to this set of constraint also as Partition Adjacency Matrix (PAM) restrictions. 
 


It is implemented according to the paper:

- [*Pelican, A (2019). Uniform Sampling of Graphs with Fixed Degree
Sequence under Partition Constraints. Master Thesis, FernUniversität in Hagen.*](https://www.fernuni-hagen.de/MATHEMATIK/DMO/pubs/Master_Andrin_Pelican.pdf) 
    - Proof of correctness of the algorithm
    - Discussion of the PAM-realization problem
    
- *Pelican, A. & Graham, B. S. (2019). Testing for strategic interaction in social and economic
network formation. Technical report, University of California - Berkeley.*
    - Derivation of a locally most powerful test statistic for a n-person network formation game in normal form


## Get it Running 

Install the paper via pip:


- pip install ugd
 
then run
    
    #import modules
    import ugd
    import numpy
    
    # create ajdancy matrix
    adj_m = numpy.zeros((4,4))
    adj_m[0,1] = 1
    adj_m[1,0] = 1
    adj_m[3,2] = 1
    adj_m[2,3] = 1
    
    # create dictionary of nodeatributes 
    var_dict ={
        0: {'gender': 'm'},
        1: {'gender': 'm'},
        2: {'gender': 'f'},
        3: {'gender': 'f'},
    }
    out_dict = ugd.graph_hyp_test(adj_m=adj_m, var_dict = var_dict, test_variable= ('gender','m','f'),mixing_time=1000, anz_sim=100, show_polt=True)

### Working with ugd

The easiest way to use ugd is by simply passing in the adjacency matrix and set show_plot=True. This runs the simulation
algorithm and plots a default statistic. 

The statistic can be customized. Firstly by entering a dictionary with node characteristics and testing for one characteristic.
Secondly by writing a costume test statistic and enter it into the function as 'stat_f'. How to write a "locally most powerful"
test statistic for a specific network formation game is derived in *Pelican, A. & Graham, B. S. (2019)*. The weights for the optimal
test statistic is not calculated by this package, it has to be done with other statistical packages and
feed in via 'stat_f' or directly applied to the list of graphs returned by the ugd package.

Node characteristic can be added as controls. The algorithm then generated uniformly graphs with also have the same number
of edges between the node-groups induced by the controls. Note that the algorithm is slower if many controls are added. 
Hard constraints (where there are no edges within, or some the groups), such as the group constraint in a bipartite graph 
do not slow the algorithm.

The processing of the individual graphs can be easily customized by working directly with the simulated graphs.

An entry point of testing social and economic networks can be found here [https://arxiv.org/abs/1908.00099](https://arxiv.org/pdf/1908.00099.pdf).

## API

There are two functions provided.

1) graph_hyp_test
    - generating a sequence of uniform sampled *graphs* under the desired set of constrains.
2) digraph_hyp_test
    - generating a sequence of uniform sampled *digraphs* under the desired set of constrains.


For the API the two functions only differs in that the interpretation of the adjacency matrix is once 
as digraph representation and once as graph representation.


    
    INPUT:
    :param adj_m:         A numpy array containing 0 and 1s as elements, representing
                          adjacency matrix of the graph
    :param var_dict:      A dictionary with the integers 1..n as primary key (representing
                          the n nodes). The values are dictionaries containing the 
                          Variable name as keys and the values can either be numbers or be
                          numbers or strings
    :param stat_f:        A function which maps the adj_m and var_dict to a number "the
                          statistic of interest".
    :param test_variable: Alternative to stat_f, creating a statistic which counts the
                          arrows form a node-subset into another. It is a triple with 
                          first element variable name, second the value of the variable 
                          for the set where the arrows leave and third the value of the 
                          subset where the arrow go to.
    :param controlls:     List of variable names, the number of arrows crossing the groups
                          induced by the controls is constant in all the simulation.
    :param mixing_time:   Number of runs (steps in the markov graph) before a the graph
                          is considered random
    :param anz_sim:       Number of simulations
    :param show_polt:     Boolean whether a plot is desired

    OUTPUT:
    :return: out_dict     Dictionary with keys 'graph_list', 'stat_list', 'plot',
                          and 'info_dict'
    graph_list:           List of random adjacency matrices with the given degree-sequence
                          and arrows between the controls
    stat_list:            List of the statistics stat_f evaluated for the random graphs
    plot:                 Plot with the illustration of the estimation output
    info_dict:            Dictionary with the information about the simulation
    



## Architecture:


All the logic is implemented in the digraph_draw folder. it is divided into

*  markov_walk

     Implementation of algorithm 1 from the paper *Markov Draw Algorithm*

* schlaufen_construction
       
     Implementation of algorithm 2 from the paper *Schlaufen Detection Algorithm*
     

*  model
 
    containing the data models (appropriate Graph representation  and node representation for 
    efficient construction of the altering paths in the Schlaufen)
  
* user_interface

    Contains the all the logic used for *input validation, parsing of input, estimation of runtime, 
    transformation of the graph format, output processing*.
    
*  help_functions


### Comment

The current implementation, includes only controlling of a fixed number of crossing edges/arrows between node-groups as 
constraints. More complex complex can be implemented by writing a consum implementation of the *no_violation* function 
in *constraint_violation_check*. Note, that depending on the constraint the construction of the Schlaufensequence should
 not be stopped because a feasible one is found, but only due to the random stop. This in order to preserve correctness.
 
## Testing

All tests are in the test folder. They are written using pytest. 
To execute them cd into the test folder and run

- pytest 

in the terminal.






