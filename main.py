import networkx as nx
import Diffusion as lfm

distance_factor = 0.5
delta = 3

machine_out_file = open("output", "w")

LFD = lfm.Diffusion("network", "week_user_artist_count", "user_artist_totalistening_periodlength")
actions = LFD.get_action_list()

for act in actions:
    asg = LFD.build_action_subgraph(act, delta)
    leaders = LFD.compute_action_leaders(asg)

    for l in leaders:
        l_t = nx.dfs_tree(asg, l)
        tribe = l_t.nodes()

        frontier = []
        for l_n in l_t.nodes():
            if l_t.out_degree(l_n) == 0:
                frontier.append(l_n)

        depth = LFD.compute_max_depth(l_t, l, frontier)
        mean_depth = float(depth) / len(frontier)
        width = LFD.compute_width(l_t, l)
        l_strength = LFD.compute_level_strength(l_t,l,distance_factor,act)

        machine_out_file.write(
            "%d::%d::%d::%1.9f::%1.9f::%1.9f::%1.9f\n" \
            % (act, l, len(tribe), depth, mean_depth, width, l_strength))

machine_out_file.flush()
machine_out_file.close()

print "Finished"
