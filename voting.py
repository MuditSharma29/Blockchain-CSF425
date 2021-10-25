from authority_nodes import authority_nodes
voting_lst = []
 
# Authority to be voted for as input
authority_id_voting = input("Enter the id for the authority for whom voting is taking place  : ")
n = len(authority_nodes_list)
 
for i in range(0, n):
	ele = int(input())
	voting_lst.append(ele)

remove_votes = voting_lst.count(0)
add_votes = n - remove_votes
majority = math.floor(float(len(authority_nodes_list)/2)) + 1

for i in range(0,n):
	if authority_id_voting == (i in authority_nodes_list):
		bool id = True
if id == True:
	if remove_votes > majority :
		remove_authority(authority_id)	
	elif add_votes > majority :
		add_authority(authority_id)
