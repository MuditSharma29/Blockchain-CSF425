authority_nodes_list = ["http://127.0.0.1:8000","http://127.0.0.1:5001"]
# crypto_keys = [{pr1,pk1},{pr2,pk2}]
# print(crypto_keys)

def add_authority(authority_id):
    print(authority_id)
    if authority_id in authority_nodes_list:
        return "Authority {} already present".format(authority_id)
    authority_nodes_list.append(authority_id)
    return "Authority {} added successfully".format(authority_id)

def remove_authority(authority_id):
    if authority_id in authority_nodes_list:
        authority_nodes_list.remove(authority_id)
        return "{} Authority removed successfully".format(authority_id)
    else:
        return "Authority {} not found".format(authority_id)

# print(remove_authority("http://127.0.0.1:5001"))
# print(authority_nodes_list)