import json

INFILE = "../tagging/complete_tagged.json"
OUTFILE = "products.json"

if __name__ == "__main__":
    with open(INFILE, "r") as inf:
        with open(OUTFILE, "w") as outf:
            posts = json.load(inf)
            products = {}
            for post in posts:
                organizations = post["organization"].split(";")
                if len(organizations) == 0:
                    continue
                for organization in organizations:
                    if organization.isspace() or len(organization) == 0:
                        continue
                    if organization not in products:
                        products[organization] = 0
                    products[organization] += 1
            
            products = sorted(products, key=lambda x: products[x])[::-1]
            json.dump(products, outf, indent=2)
