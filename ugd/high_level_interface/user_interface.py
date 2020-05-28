'''User Interface with documentation '''

from ugd.high_level_interface.draw_simulations import hyp_test


def digraph_hyp_test(adj_m, var_dict=None, stat_f=None, test_variable=None, controls=None, mixing_time=None,
                     anz_sim=1000, show_polt=False, fast_mixing_time_evaluation = False):
    '''
    PURPUSE: generation of random Digraphs which a given degree sequence and "crossarrow" restrictions, in order to estimate
             the distribution of a test statistic under the 0 Hypotheses. Further explanation on methods is given in
             paper : Testing Strategic Interaction in Networks

    INPUT:
    :param adj_m:         A numpy array containing 0 and 1s as elements, representing ajdancy matrix of the Digraph
    :param var_dict:      A dictionary with the integer 1..n as primary key, where n is the number of nodes,
                          the Values are dictionaries as well with the variable names as key and the variable value as
                          value the values have to be numbers or strings
    :param stat_f:        A function which maps the adj_m and var_dict to a number "The statistic of interest".
    :param test_variable: Alternative to stat_f, creating a statistic which counts arf form a node subsets into another:
                          a triple with first element variable name, second the value of the variable for the set where
                          the arcs leave and third the value of the subset where the arrow go to
    :param controls:      List of variable names of controls
    :param mixing_time:   Number of runs (steps in the markov graph) before a the graph is considered random
    :param anz_sim:       Number of simulations
    :param show_polt:     Boolean whether a plot is desired
    :return:
    graph_list:           List of random adjacency matrices with the given degree sequence and the cross arrows
    stats_list:           List of the statistics stat_f evaluated for the random graphs

    USAGE:
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
    graphs, stats_list = digraph_hyp_test(adj_m=adj_m, var_dict = var_dict, test_variable= ('gender','m','f'),mixing_time=10000, anz_sim=100, show_polt=True)

    AUTORS:
    Andrin Pelican, andrin.pelican@unisg.ch

    '''

    return hyp_test(adj_m, var_dict, stat_f, test_variable, controls, mixing_time, anz_sim, show_polt,
                    is_directed=True,  fast_mixing_time_evaluation = fast_mixing_time_evaluation)


def graph_hyp_test(adj_m, var_dict=None, stat_f=None, test_variable=None, controls=None, mixing_time=None,
                   anz_sim=1000, show_polt=False,  fast_mixing_time_evaluation = False):
    '''
    PURPUSE: generation of random Graphs with a given degree sequence and restrictions induced by the node-attributes
             in order to estimate the distribution of a test-statistic under the 0 Hypotheses.Further explanation on
             methods is given in paper:
             Uniform Sampling of Graphs with Fixed Degree Sequence under Partition Constraints

    INPUT:
    :param adj_m:         A numpy array containing 0 and 1s as elements, representing adjacency matrix of the graph
    :param var_dict:      A dictionary with the integers 1..n as primary key (representing the n nodes).
                          The values are dictionaries containing the Variable name as keys and the values can either be
                          numbers or strings.
    :param stat_f:        A function which maps the adj_m and var_dict to a number "the statistic of interest".
    :param test_variable: Alternative to stat_f, creating a statistic which counts the arrows form a node-subset into
                          another. It is a triple with first element variable name, second the value of the variable for
                          the set where the arrows leave and third the value of the subset where the arrow go to.
    :param controls:      List of variable names, the number of arrows crossing the groups induced by the controls is
                          constant in all the simulation.
    :param mixing_time:   Number of runs (steps in the markov graph) before a the graph is considered random
    :param anz_sim:       Number of simulations
    :param show_polt:     Boolean whether a plot is desired

    OUTPUT:
    :return:
    graph_list:           List of random adjacency matrices with the given degree sequence and arrows between the controls
    stats_list:           List of the statistics stat_f evaluated for the random graphs

    USAGE:
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
    graphs, stats_list = graph_hyp_test(adj_m=adj_m, var_dict = var_dict, test_variable= ('gender','m','f'),mixing_time=10000, anz_sim=100, show_polt=True)

    AUTORS:
    Andrin Pelican, andrin.pelican@bluewin.ch

    '''

    return hyp_test(adj_m, var_dict, stat_f, test_variable, controls, mixing_time, anz_sim, show_polt,
                    is_directed=False,  fast_mixing_time_evaluation = fast_mixing_time_evaluation)
