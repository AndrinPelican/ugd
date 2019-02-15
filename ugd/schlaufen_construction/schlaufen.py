from ugd.schlaufen_construction.schlaufen_construction import add_plain_random_schlaufe
from ugd.schlaufen_construction.di_schlaufen_construction import add_di_random_schlaufe


def add_random_schlaufe(graph, schleifen_number):
    # directs to the right Schlaufen construction function, directed and undirected,
    if graph.is_directed:
        return add_di_random_schlaufe(graph, schleifen_number)
    else:
        return add_plain_random_schlaufe(graph, schleifen_number)
