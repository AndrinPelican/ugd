import matplotlib.pyplot as plt
import numpy as np
from ugd.help_function.util_statistic import get_quantile, get_normalized_numb_graphs_same_as_observed


def postprocess(adj_m_original, stats_list, stat_f, var_dict, test_variable, edges_changed_per_draw, show_plot=False):
    '''
    General output postprocessing and plotting, this part is convenient for experimenting with graph.
    However it can easily be customized by using the output graph sequence of the algorithm.
    '''
    org_value = stat_f(adj_m_original, var_dict)
    quantile = get_quantile(org_value, stats_list)
    normalized_numb_graphs_same_as_observed = get_normalized_numb_graphs_same_as_observed(org_value, stats_list)


    statistic_name = stat_f.__name__
    if not (test_variable == None):
        statistic_name = 'crosslinks ' + str(test_variable[0]) + ': ' + str(test_variable[1]) + ' to ' + str(test_variable[2])

    info_dict = {
        'stat_name': statistic_name,
        'original_value': org_value,
        'normalized_numb_graphs_same_as_observed': normalized_numb_graphs_same_as_observed,
        'quantile': quantile,
    }

    annotate_string = 'Estimated H0 distribution for statistic: ' + statistic_name               + '\n' \
                    + 'Observed statistic lies at quantile: ' + '{:.4f}'.format(quantile)    + '\n' \
                    + '(of the simulated H0 distribution)'                                            + '\n' \
                    + 'Average numbers of edges changed per draw: ' + str(int(edges_changed_per_draw * 100)) + '%'

    
    #min_value = min(stats_list)
    #max_value = max(stats_list)
    #y = [0] * (int(max_value + 1) - int(min_value))
    #x = list(range(int(min_value), int(max_value + 1)))
    #for stat_val in stats_list:
    #    y[int(stat_val) - int(min_value)] += 1 / stats_list.__len__()

    #width = 1 / 1.5
    #plt.bar(x, y, width, color= "#3B7EA1")

    plt.hist(stats_list, bins='fd', density = True)
    plt.axvline(x=org_value, color="#FDB515")
    plt.title('H0 Reference Distribution')
    plt.ylabel('Frequency')
    plt.xlabel('Statistic')
    plt.gcf().subplots_adjust(bottom=0.25)
    plt.annotate(annotate_string, (0, 0), (0, -35), xycoords='axes fraction', textcoords='offset points', va='top')

    if show_plot:
        plt.show()
    else:
        plt.clf()
        plt.cla()
        plt.close()

    return plt, info_dict
