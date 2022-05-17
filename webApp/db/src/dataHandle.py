def concat_employes(employes:str):
    new_employes = employes
    for employe in new_employes:
        indexs = [new_employes.index(_employe) for _employe in new_employes if employe[0] in _employe]
        if len(indexs) > 1 :
            services = [new_employes[idx][6] for idx in indexs]
            [new_employes.pop(idx) for idx in reversed(indexs[1:])]
            new_employes[indexs[0]] = list(new_employes[indexs[0]])
            new_employes[indexs[0]][6] = services
            new_employes[indexs[0]] = tuple(new_employes[indexs[0]])
    return new_employes

def convert_employe_service_in_list(employe):
    new_employe = list(employe[0])
    new_employe[6] = [new_employe[6]]
    return tuple(new_employe)