# Leader Detect
The Three Dimensions of Social Prominence

Leader Detect is an algorithm that takes as input a social network and a table of actions performed by the people in the social networks and returns for each action the list of leaders and some statistics of their “tribe”, i.e. the set of people they influenced. This algorithm comes from the paper “The Three Dimensions of Social Prominence”, published at the International Conference of Social Informatics.

  main.py: The main Python script for running the leader extraction.
  Diffusion.py: The Python class implementing the ExtractLeader procedure and the calculation of Width, Depth and Strength.

For your convenience, the repository also includes a sample dataset ready for being analyzed. It is extracted from Last.fm and it is the same used in the paper:

  network: The social graph extracted from Last.Fm. It contains two space-separated columns with the ids of two nodes, connected if they are friend in the Last.Fm social graph. The graph is unweighted and undirected.
  week_user_artist_count: The main action table used by the ExtractLeader procedure. It has 4 columns separated by the token “::” (without quotes). The first column is the timestamp (week id) of the action; the second column is the user id (correspondent to the nodes id in the file “network”); the third column is the artist id and the fourth column contains the number of listenings made by the user of that particular artist in that particular period.
  user_artist_totalistening_periodlength: The complementary action table for the calculation of the Strength measure. It has 4 columns separated by the token “::” (without quotes). The first column is the user id; the second column is the artist id; the third column is the total number of listenings that the user made of the artist and the fourth column is the length of the period in which the user listened to the artist (last week minus first week).
  artist_tag_id: A dictionary with three columns separated by the token “::” (without quotes). The first column is the artist name, the second column is its majority tag (music genre) and the third column is its id to cross the information with the action table in the file “week_user_artist_count”.

The repository also includes an extra files:

  netstats.py: A Python script to calculate the topology values for all the nodes in the network. It takes as input the “network” file present in the package.
Instructions:

To run the algorithm simply put all the files in the same folder and type in the command shell:

 python main.py 
NB: File paths are hard coded in main.py, as well as the parameters values (delta and beta, the damping factor). To use the algorithm for your purposes simply use the same filename and/or modify them from the sources as well as the parameters.

# File(s) Format:

The output file has 7 columns, separated by the token “::” (without quotes).

Column #1: The action id (the artist).
Column #2: The leader id.
Column #3: The size of the leader’s tribe (for the corresponding action).
Column #4: Maximum Depth of the leader’s tribe (for the corresponding action).
Column #5: Average Depth of the leader’s tribe (for the corresponding action) – This is what we used instead of the Maximum Depth for our experiments.
Column #6: Width of the leader’s tribe (for the corresponding action).
Column #7: Strength of the leader’s tribe (for the corresponding action).

If you want to calculate network topology measures with the same format that we used in the paper, you can run the network statistics script. Simply put all the files in the same folder and type in the command shell:

 python netstats.py 
Please note that the script will take time to calculate all the values of the Betweennes and Closeness Centrality. Moreover, the script is tuned to calculate an approximate value of the Betweennes, for time constraints. The output file has 5 columns, separated by the token “::” (without quotes):

Column #1: The node id.
Column #2: The node’s local clustering coefficient.
Column #3: The average neighbors’ degree of the node.
Column #4: The node’s approximate betweenness centrality.
Column #5: The node’s closeness centrality.
