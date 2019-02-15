import pytest
import numpy as np
from ugd import graph_hyp_test
from test.test_resources.plain_graph_integration import adj_m_1, var_dict_1


def test_empty_graph():
    adj_m = np.zeros((4, 4))
    with pytest.raises(ValueError) as e_info:
        _ = graph_hyp_test(adj_m=adj_m, var_dict=var_dict_1, test_variable=('gender', 'm', 'f'),
                                            mixing_time=100, anz_sim=100, show_polt=False)


def test_only_matrix():
    _ = graph_hyp_test(adj_m_1, mixing_time=10)
    # should not rise an error
    assert True


def test_spelling_error():
    with pytest.raises(ValueError) as e_info:
        _ = graph_hyp_test(adj_m=adj_m_1, var_dict=var_dict_1, test_variable=('genderr', 'm', 'f'))


def test_no_node_with_testvalue():
    with pytest.raises(ValueError) as e_info:
        _ = graph_hyp_test(adj_m=adj_m_1, var_dict=var_dict_1, test_variable=('gender', 'male', 'f'))


def test_no_node_with_testvalue2():
    with pytest.raises(ValueError) as e_info:
        _ = graph_hyp_test(adj_m=adj_m_1, var_dict=var_dict_1, test_variable=('gender', 'm', 'female'))


def test__with_only_stat():
    _ = graph_hyp_test(adj_m=adj_m_1, stat_f=my_stat, mixing_time=10)
    assert True


def test__with_only_stat_and_vardict():
    _ = graph_hyp_test(adj_m=adj_m_1, var_dict=var_dict_1, stat_f=my_stat, mixing_time=10)
    assert True


def test_controlls_in_vardict():
    _ = graph_hyp_test(adj_m=adj_m_1, var_dict=var_dict_1,
                                        stat_f=my_stat, mixing_time=10)
    assert True


def test_with_control_misspeled():
    with pytest.raises(ValueError) as e_info:
        _ = graph_hyp_test(adj_m=adj_m_1, var_dict=var_dict_1, controls=['genderr'], mixing_time=10)


def test_matrix_with_vardict():
    _ = graph_hyp_test(adj_m_1, var_dict=var_dict_1, mixing_time=10)
    assert True


def my_stat(adm, var_dict):
    return 5
