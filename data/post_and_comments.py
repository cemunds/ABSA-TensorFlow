infile = 'out_pandc.txt'  # use data.py to extract post_id, post_text, comment_id and comment_message
outfile = 'pretty_posts.txt'

post_id = -1

with open(outfile, 'w') as fout:
    print("Writing to {}".format(outfile))
    with open(infile, 'r') as fin:
        for line in fin.readlines():
            pid, ptxt, cid, cmsg = line.split("\t")
            if pid != post_id:  # New Post starts
                post_id = pid
                fout.write("".join(['#' for _ in range(30)]))
                fout.write("\n"+ptxt+"\n\n")
            else:
                fout.write("\t"+cmsg+"\n")


