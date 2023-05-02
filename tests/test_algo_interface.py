from src import config as cfg

def test_algo_interface():
    algorithm_class = 'AlgoInterface'
    algorithm_file = 'algo_interface'
    executable_run = cfg.build_algorithm(algorithm_file, algorithm_class)

    event = executable_run()
    assert event
