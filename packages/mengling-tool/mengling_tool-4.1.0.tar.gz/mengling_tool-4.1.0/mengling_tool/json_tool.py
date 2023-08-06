import json



def allValues_to_txt(datadt: dict, ifget_dt=False, ensure_ascii=False) -> str or dict:
    tempdt = dict()
    for k in datadt.keys():
        tempdt[k] = to_txt(datadt[k], ensure_ascii=ensure_ascii)
    if ifget_dt:
        return tempdt
    else:
        return to_txt(tempdt, ensure_ascii=ensure_ascii)
