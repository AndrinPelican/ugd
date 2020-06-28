import matplotlib.pyplot as plt
from ugd.help_function.util_statistic import get_quantile, get_normalized_numb_graphs_same_as_observed


def postprocess(adj_m_original, stats_list, stat_f, var_dict, test_variable, edges_changed_per_draw, show_polt=False):
    '''
    General output postprocessing and plotting, this part is convenient for experimenting with graph
    However can be easily customized by using the output graph sequence of the algorithm.
    '''
    org_value = stat_f(adj_m_original, var_dict)
    quantile = get_quantile(org_value, stats_list)
    normalized_numb_graphs_same_as_observed = get_normalized_numb_graphs_same_as_observed(org_value, stats_list)


    statisitc_name = stat_f.__name__
    if not (test_variable == None):
        statisitc_name = 'crosslinks ' + str(test_variable[0]) + ': ' + str(test_variable[1]) + ' to ' + str(test_variable[2])

    info_dict = {
        'stat_name': statisitc_name,
        'original_value': org_value,
        'normalized_numb_graphs_same_as_observed': normalized_numb_graphs_same_as_observed,
        'quantile': quantile,
    }

    annotate_string = 'Distribution estimate of the test statistic:   ' + statisitc_name + '\n' \
                      + 'The observed value lies in quantile:            ' + str(quantile) + '\n' \
                      + 'Average changed edges per draw:              ' + str(int(edges_changed_per_draw * 100)) + '%'

    min_value = min(stats_list)
    max_value = max(stats_list)
    y = [0] * (int(max_value + 1) - int(min_value))
    x = list(range(int(min_value), int(max_value + 1)))
    for stat_val in stats_list:
        y[int(stat_val) - int(min_value)] += 1 / stats_list.__len__()

    width = 1 / 1.5
    plt.bar(x, y, width, color="blue")
    plt.axvline(x=org_value, color='red')
    plt.title('Distribution')
    plt.ylabel('Probability')
    plt.xlabel('Values')
    plt.gcf().subplots_adjust(bottom=0.25)
    plt.annotate(annotate_string, (0, 0), (0, -35), xycoords='axes fraction', textcoords='offset points', va='top')

    if show_polt:
        plt.show()

    return plt, info_dict
