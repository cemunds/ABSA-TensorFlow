import os
subdir = 'Tesco'
outfile = 'out.txt'
filter = None

def define_filter(line):
    headers = []
    for idx, h in enumerate(line.split()):
        print("{} {}".format(idx+1, h))
    print("Enter indices that should be included in the result file:")
    indices = input()
    return [int(ele)-1 for ele in indices if ele.isdigit()]


for root, directory, filenames in os.walk(subdir):
    with open(outfile, 'w') as fout:
        for filename in filenames:
            if '.tab' in filename and 'comments' in filename:
                fullfilename = os.path.join(root, filename)
                print("Processing file {}".format(fullfilename))
                with open(fullfilename, 'r') as fin:
                    for idx, line in enumerate(fin.readlines()):
                        if filter is None:
                            filter = define_filter(line)
                            print("Writing to file {}".format(outfile))
                        else:
                            line = line.split("\t")
                            result = []
                            for f in filter:
                                result.append(line[f])
                            fout.write("\t".join(result))
                            fout.write("\n")


                            
                        
