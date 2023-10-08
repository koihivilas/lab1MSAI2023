class Stats:
    max_fringe_size = 0
    visited_nodes = 0
    path_length = 0
    iterations = 0

    def reset_stats():
        Stats.max_fringe_size = 0
        Stats.visited_nodes = 0
        Stats.path_length = 0
        Stats.iterations = 0