import collections
data=collections.OrderedDict()
with open("usage.log.py") as file:
    for line in file:
        parts=line.split(" ")
        if not parts[0] in data: data[parts[0]]=[]
        data[parts[0]].append(parts[2].replace("\n","").lower())
for key in data.keys():
    print(key, "Usage: ", len(data[key]), "\tUser: ", len(set(data[key])))
