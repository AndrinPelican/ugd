# Uniform Graph Draw


This package implements random draw algorithm for networks. In particular it creates uniform samples of networks with a
given degree-sequence and partition constraints (fixed number of crossing edges/arrows between node-groups in partition).
The literature reefers to this set of constraint also as Partition Adjacency Matrix (PAM) restrictions. 

It is implemented according to the paper:

- [*Pelican, A (2019). Uniform Sampling of Graphs with Fixed Degree Sequence under Partition Constraints. Master Thesis, FernUniversität in Hagen.*](https://www.fernuni-hagen.de/MATHEMATIK/DMO/pubs/Master_Andrin_Pelican.pdf) 
    - Proof of correctness of the algorithm
    - Discussion of the PAM-realization problem
    
- [*Pelican, A. & Graham, B. S. (2020). An optimal test for strategic interaction in social and economic network formation between heterogeneous agents*](https://arxiv.org/pdf/2009.00212.pdf)
    - Derivation of a locally most powerful test statistic for a n-person network formation game in normal form


## Get it Running 

Install the package via pip:

- pip install ugd
 
then run
    
    #import modules
    import ugd
    import numpy
    
    # create adjacency matrix
    adj_m = numpy.zeros((4,4))
    adj_m[0,1] = 1
    adj_m[1,0] = 1
    adj_m[3,2] = 1
    adj_m[2,3] = 1
    
    # create dictionary of node attributes
    var_dict ={
        0: {'gender': 'm'},
        1: {'gender': 'm'},
        2: {'gender': 'f'},
        3: {'gender': 'f'},
    }
    
    # UNDIRECTED CASE, test whether there are abnormal many connection between groups:
    
    # test undirected: note there are 3 possible networks, and only one has no male, female edges
    out_dict = ugd.graph_hyp_test(adj_m=adj_m, var_dict = var_dict, test_variable= ('gender','m','f'),mixing_time=1000, anz_sim=100, show_polt=True)
    
    # DIRECTED CASE, test a utility funktion with the local optimal test:
    
    # testing whether there is taste for reciprocity:
    def edge_util_function(adj_m):
        # the utility is reciprocity -> i gets utility form an edge to j if j has an edge to i
        return numpy.transpose(adj_m)
    
    optimal_stat_for_reciprocity = ugd.make_lcl_mst_pwf_stat(adj_m, edge_util_function= edge_util_function)
    
    # there are 9 graphs, for 3 the reciprocity is high, for 6 low, due to symmetry the optimal stat only takes on 2 values
    out_dict = ugd.digraph_hyp_test(adj_m=adj_m, stat_f=optimal_stat_for_reciprocity , mixing_time=100, anz_sim=100, show_polt=False)
    
    print("is stat value of the original graph:")
    print(out_dict["info_dict"]["original_value"])
    print("the values of the simulated graphs:")
    print(out_dict["stat_list"])
    var_dict = var_dict, test_variable= ('gender','m','f'),mixing_time=1000, anz_sim=100, show_polt=True)

### Working with ugd

The easiest way to use ugd is by simply passing in the adjacency matrix and set show_plot=True. This runs the simulation
algorithm and plots a default statistic. 

The statistic can be customized. Firstly by entering a dictionary with node characteristics and testing for one characteristic.
Secondly by writing a custom test statistic and passing it into the function as 'stat_f'. How to write a "locally most powerful"
test statistic for a specific network formation game is derived in *Pelican, A. & Graham, B. S. (2019)*. The weights for the optimal
test statistic are not calculated by this package, it has to be done with other statistical packages and
feed in via 'stat_f' or directly applied to the list of graphs returned by the ugd package.

Node characteristic can be added as controls. The algorithm then generated uniformly graphs with also have the same number
of edges between the node-groups induced by the controls. Note that the algorithm is slower if many controls are added. 
Hard constraints (where there are no edges within, or across some the groups), such as the group constraint in a bipartite graph 
do not slow the algorithm.

The processing of the individual graphs can be easily customized by working directly with the simulated graphs.

An entry point of testing social and economic networks can be found here [https://arxiv.org/abs/1908.00099](https://arxiv.org/pdf/1908.00099.pdf).

## API

There are 3 functions provided.

1) graph_hyp_test
    - generating a sequence of uniform sampled *graphs* under the desired set of constrains.
2) digraph_hyp_test
    - generating a sequence of uniform sampled *digraphs* under the desired set of constrains.
3) make_lcl_mst_pwf_stat
    - making a locally optimal test statistic from the edge utility and the observed network.
      The locally optimal test statistic can then be used in digraph_hpy_test.

For the API the first two functions only differs in that the interpretation of the adjacency matrix is once 
as digraph representation and once as graph representation.


    
    INPUT:
    -----------------------------------------------------------------------------------------------------    
    :param adj_m:         A numpy array containing 0 and 1s as elements, representing adjacency 
                          matrix of the digraph.
    
    :param var_dict:      A dictionary with the integer 1..n as primary Key, where n is the 
                          number of nodes, the Values are also dictionaries (with the variable 
                          names as Keys and variable values as Values). Values have to be numbers 
                          or strings.
    
    :param stat_f:        A function which maps the adj_m and var_dict to a real number 
                          ("The statistic of interest").
    
    :param test_variable: Alternative to stat_f, creating a statistic which counts arcs from 
                          one node subset into another: a triple with first element equal to a 
                          variable name, second element equal to the value of the variable 
                          for the node set where the arcs are directed from, and third element 
                          the value for the subset where the arcs are directed to.
    
    :param controls:      List of variable names for the controls used to define the cross-link 
                          matrix.
    
    :param mixing_time:   Number of runs (steps in the markov graph) before a the graph is 
                          considered a unifom random draw from the target set.
    
    :param anz_sim:       Number graphs to simulate/generate.
    
    :param show_plot:     Boolean for whether a plot is desired.
    
    
    OUTPUT:
    -----------------------------------------------------------------------------------------------------        
    graph_list:           List of random adjacency matrices with the given in- and out- degree sequences 
                          and "cross-arrow" (or cross-link) restrictions.
    
    stats_list:           List of the statistics, stat_f, evaluated for the simulated graphs.
   
    

The API for make_lcl_mst_pwf_stat:

   
    INPUT:
    :param adj_m:                A numpy array containing 0 and 1s as elements, representing
                                 adjacency matrix of the digraph.
    
    :param var_dict:             A dictionary with the integers 1..n as primary key (representing
                                 the n nodes). The values are dictionaries containing the 
                                 Variable name as keys and the values can either be numbers or be
                                 numbers or strings.
                                 
    :param controlls:            List of variable names, the number of arrows crossing the groups
                                 induced by the controls is constant in all the simulation.
                                 
    :param edge_util_function:   A function mapping the an adjency matrix to a numpy matrix, 
                                 where the entries are the corresponding utility the agent 
                                 would get from forming the edge. 

    OUTPUT:
    :param localy_optimal_stat:  A function which maps the adj_m and var_dict to a number "the
                                 locally optimal statistic for the edge utility".

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
constraints. More complex constraints can be implemented by writing a custom implementation of the *no_violation* function 
in *constraint_violation_check*. Note, that depending on the constraint the construction of the Schlaufen sequence should
not be stopped because a feasible one is found, but only due to the random stop. This in order to preserve correctness.