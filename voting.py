import authority_nodes
import math
voting_lst = []

def voting_for_authority():
	# Authority to be voted for as input
	authority_id_voting = input("Enter the id for the authority for whom voting is taking place: ")
	n = len(authority_nodes.authority_nodes_list)
	# print(n)
	for i in range(0, n):
		ele = int(input())
		voting_lst.append(ele)
	# print(voting_lst)
	remove_votes = voting_lst.count(0)
	add_votes = n - remove_votes
	# print(remove_votes)
	majority = math.floor(float(n/2)) + 1
	# print(majority)
	if remove_votes >= majority:	
		return authority_nodes.remove_authority(authority_id_voting)
	elif add_votes >= majority :
		return authority_nodes.add_authority(authority_id_voting)