import collections
data=collections.OrderedDict()
all_data=[]
with open("../usage.log") as file:
    for line in file:
        parts=line.split(" ")
        if len(parts)==3: parts=["1.0"]+parts
        if not parts[1] in data: data[parts[1]]={}
        userid=parts[3].replace("\n","").lower()
        date=parts[1]
        version=parts[0]
        if not version in data[date]: data[date][version]=[]
        data[date][version].append(userid)
        all_data.append(userid)
for key in data.keys():
    total_day=[]
    print(key, end="\t")
    for version in data[key].keys():
        total_day+=data[key][version]
        print(version, "Usage: {:=4} User: {:=4}".format(len(data[key][version]), len(set(data[key][version]))),end="\t")
    print("Total: Usage: {:=4} User: {:=4}".format(len(total_day), len(set(total_day))))
print("Total: Usage:",len(all_data),"User:",len(set(all_data)))
