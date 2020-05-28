'''
Controlls sequence of all the steps used for a call of the graph_hyp_test function
'''
from ugd.help_function.graph_creation import generate_graph, graph_to_adj_m
from ugd.high_level_interface.output_processing import postprocess
from ugd.high_level_interface.time_mixing_evaluation import evaluate_mixing_time
from ugd.high_level_interface.validation import validate_input, parse_input
from ugd.markov_walk.markov_walk import markov_walk


def hyp_test(adj_m, var_dict, stat_f, test_variable, controlls, mixing_time, anz_sim, show_polt, is_directed, fast_mixing_time_evaluation):
    ''' contains the actual flow of the procedure,'''

    '1) validation and input substitution'
    validate_input(adj_m, anz_sim, mixing_time, var_dict, stat_f, controlls, test_variable, is_directed)
    stat_f, nodesetpartition = parse_input(stat_f, test_variable, controlls, var_dict, adj_m)

    '2) parse graph, into shape for simulation'
    graph = generate_graph(adj_m, nodesetpartition, is_directed)

    '3) determine mixing time, and mixing "amount" '
    mixing_time, edges_changed_per_draw = evaluate_mixing_time(graph, mixing_time, anz_sim, fast_mixing_time_evaluation)

    '4) generating the random graphs under the constraints'
    graphs, stats_list = gen_draws(graph, var_dict=var_dict, stat_f=stat_f, anz_sim=anz_sim, mixing_time=mixing_time)

    '5) post processing, estimating the distribution, plotting'
    plt, info_dict = postprocess(adj_m_original=adj_m, stats_list=stats_list, var_dict=var_dict, stat_f=stat_f,
                                 show_polt=show_polt, test_variable=test_variable,
                                 edges_changed_per_draw=edges_changed_per_draw)

    return {'graph_list': graphs, 'stat_list': stats_list, 'plot': plt, 'info_dict': info_dict}


def gen_draws(graph, mixing_time, anz_sim, var_dict, stat_f):
    'iteratively generating anz_sim random sample graphs'
    graph_list = []
    stat_list = []
    for i in range(anz_sim):
        # a random draw
        graph = markov_walk(graph, mixing_time)
        graph_list.append(graph_to_adj_m(graph))
        adj_m_generated = graph_to_adj_m(graph)
        stat_list.append(stat_f(adj_m_generated, var_dict))

    return graph_list, stat_list
