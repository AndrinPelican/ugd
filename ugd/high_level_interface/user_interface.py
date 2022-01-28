'''User Interface with documentation '''

from ugd.high_level_interface.draw_simulations import hyp_test


def digraph_hyp_test(adj_m, var_dict=None, stat_f=None, test_variable=None, controls=None, mixing_time=None,
                     anz_sim=1000, show_plot=False, fast_mixing_time_evaluation = False):
    
    
    '''
    
    
    OVERVIEW: This function generates random digraphs with given in- and out- degree sequences 
              and "cross-arrow" (or cross-link) restrictions. Digraphs are drawn uniformly at 
              random from the set of all labeled graphs obeying the given constraints. The simulated
              digraphs are used to estimate the H0/Null distribution of a test statistic. Further 
              explanation of methods is given in the paper : “An optimal test for strategic 
              interaction in social and economic network formation between heterogeneous agents” by
              Andrin Pelican and Bryan Graham (see https://arxiv.org/abs/2009.00212).

    
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

    
    USAGE:
    -----------------------------------------------------------------------------------------------------        
    import numpy
    adj_m = numpy.zeros((4,4))
    adj_m[0,1] = 1
    adj_m[2,3] = 1
    var_dict ={
        0: {'gender': 'm'},
        1: {'gender': 'm'},
        2: {'gender': 'f'},
        3: {'gender': 'f'},
    }
    graphs, stats_list = digraph_hyp_test(adj_m = adj_m, var_dict = var_dict, 
                                          test_variable = ('gender','m','f'), 
                                          mixing_time = 10000, anz_sim = 100, show_plot=True)

    AUTHORS:
    Andrin Pelican, andrin.pelican@bluewin.ch

    '''

    return hyp_test(adj_m, var_dict, stat_f, test_variable, controls, mixing_time, anz_sim, show_plot,
                    is_directed=True,  fast_mixing_time_evaluation = fast_mixing_time_evaluation)


def graph_hyp_test(adj_m, var_dict=None, stat_f=None, test_variable=None, controls=None, mixing_time=None,
                   anz_sim=1000, show_plot=False,  fast_mixing_time_evaluation = False):
    '''
    
    
    OVERVIEW: generation of random (undirected) Graphs with a given degree sequence and 
              restrictions induced by node attributes in order to estimate the distribution 
              of a test-statistic under the H0/null Hypothesis. Further explanation is
              given in the paper: "Uniform Sampling of Graphs with Fixed Degree Sequence 
              under Partition Constraints" by Andrin Pelican.

    
    INPUT:
    -----------------------------------------------------------------------------------------------------        
    :param adj_m:         A numpy array containing 0 and 1s as elements, representing 
                          adjacency matrix of the graph
    
    :param var_dict:      A dictionary with the integers 1..n as primary Key (representing 
                          the n nodes).
                          The Values are dictionaries containing the Variable name as Keys 
                          and Values which can either be numbers or strings.
    
    :param stat_f:        A function which maps the adj_m and var_dict to a number 
                          ("The statistic of interest").
    
    :param test_variable: Alternative to stat_f, creating a statistic which counts the edges 
                          from one node-subset into another: a triple with first element equal 
                          to a variable name, second element equal to the value of the variable 
                          for the node set where the edges are from, and third element the value 
                          for the subset where the edges go.
    
    :param controls:      List of variable names for the controls used to define the cross-link 
                          matrix.
    
    :param mixing_time:   Number of runs (steps in the markov graph) before a the graph is 
                          considered a unifom random draw from the target set.
    
    :param anz_sim:       Number graphs to simulate/generate.
    
    :param show_plot:     Boolean whether a plot is desired.

    
    OUTPUT:
    -----------------------------------------------------------------------------------------------------    
    graph_list:           List of random adjacency matrices with the given degree sequence 
                          cross-link restrictions.
    
    stats_list:           List of the statistics, stat_f, evaluated for the simulated graphs.

    
    USAGE:
    -----------------------------------------------------------------------------------------------------        
    import numpy
    adj_m = numpy.zeros((4,4))
    adj_m[0,1] = 1
    adj_m[1,0] = 1
    adj_m[3,2] = 1
    adj_m[2,3] = 1
    var_dict ={
        0: {'gender': 'm'},
        1: {'gender': 'm'},
        2: {'gender': 'f'},
        3: {'gender': 'f'},
    }
    graphs, stats_list = graph_hyp_test(adj_m = adj_m, var_dict = var_dict, 
                                        test_variable= ('gender','m','f'), 
                                        mixing_time = 10000, anz_sim = 100, show_plot=True)

    AUTHORS:
    Andrin Pelican, andrin.pelican@bluewin.ch

    '''

    return hyp_test(adj_m, var_dict, stat_f, test_variable, controls, mixing_time, anz_sim, show_plot,
                    is_directed=False,  fast_mixing_time_evaluation = fast_mixing_time_evaluation)
