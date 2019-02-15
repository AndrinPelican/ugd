import numpy as np


adj_m_1 = np.zeros((4, 4))
adj_m_1[0, 1] = 1
adj_m_1[1, 0] = 1
adj_m_1[3, 2] = 1
adj_m_1[2, 3] = 1
var_dict_1 = {
    0: {'gender': 'm'},
    1: {'gender': 'm'},
    2: {'gender': 'f'},
    3: {'gender': 'f'},
}


adj_m_2 = np.zeros((6, 6))
adj_m_2[0, 1] = 1
adj_m_2[1, 0] = 1
adj_m_2[1, 2] = 1
adj_m_2[2, 1] = 1
adj_m_2[2, 0] = 1
adj_m_2[0, 2] = 1
adj_m_2[3, 4] = 1
adj_m_2[4, 3] = 1
adj_m_2[4, 5] = 1
adj_m_2[5, 4] = 1
adj_m_2[5, 3] = 1
adj_m_2[3, 5] = 1

var_dict_2 = {
    0: {'gender': 'm'},
    1: {'gender': 'm'},
    2: {'gender': 'f'},
    3: {'gender': 'f'},
    4: {'gender': 'f'},
    5: {'gender': 'f'},
}

