import authority_nodes
import math


def voting_for_authority(authority_id_voting, voting_lst):
    # Authority to be voted for as input
    n = len(authority_nodes.authority_nodes_list)
    # print(voting_lst)
    remove_votes = voting_lst.count(0)
    add_votes = n - remove_votes
    # print(remove_votes)
    majority = math.floor(float(n / 2)) + 1
    # print(majority)
    if authority_id_voting == "http://127.0.0.1:8000":
        return "Cannot remove the CORE authority member."
    elif n > 1 and remove_votes >= majority:
        return authority_nodes.remove_authority(authority_id_voting)
    elif n <= 1 and remove_votes >= majority:
        return "Cannot remove the ONLY remaining authority member."
    elif add_votes >= majority:
        return authority_nodes.add_authority(authority_id_voting)
