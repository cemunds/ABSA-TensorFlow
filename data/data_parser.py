import os
import json
subdir = 'Tesco'
outfile = 'out.json'
filter = None
filter_names = None

def define_filter(line):
    global filter, filter_names
    headers = []
    names = []
    for idx, h in enumerate(line.split()):
        names.append(h)
        print("{} {}".format(idx+1, h))
    print("Enter indices that should be included in the result file:")
    indices = input()
    indices = indices.split()
    filter, filter_names = [], []
    for ind in indices:
        if ind.isdigit():
            i = int(ind)-1
            filter.append(i)
            filter_names.append(names[i])


for root, directory, filenames in os.walk(subdir):
    with open(outfile, 'w') as fout:
        for filename in filenames:
            if '.tab' in filename and 'fullstats' in filename:
                fullfilename = os.path.join(root, filename)
                print("Processing file {}".format(fullfilename))
                with open(fullfilename, 'r') as fin:
                    for idx, line in enumerate(fin.readlines()):
                        if filter is None:
                            define_filter(line)
                            print("Writing to file {}".format(outfile))
                        else:
                            if idx == 0:
                                continue
                            line = line.split("\t")
                            result = {}
                            for i, f in enumerate(filter):
                                result[filter_names[i]] = line[f]
                            json.dump(result, fout, indent=2)


                            
                        
