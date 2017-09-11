import collections
data=collections.OrderedDict()
all_data=[]
with open("usage.log.py") as file:
    for line in file:
        parts=line.split(" ")
        if not parts[0] in data: data[parts[0]]=[]
        userid=parts[2].replace("\n","").lower()
        data[parts[0]].append(userid)
        all_data.append(userid)
for key in data.keys():
    print(key, "Usage: ", len(data[key]), "\tUser: ", len(set(data[key])))
print("Total: Usage:",len(all_data),"User:",len(set(all_data)))
