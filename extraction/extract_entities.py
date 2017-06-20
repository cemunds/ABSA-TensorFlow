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

                    # Not lowercased on purpose
                    product = " ".join(organization.strip().split())
                    if product not in products:
                        products[product] = 0
                    products[product] += 1
            
            products = sorted(products, key=lambda x: products[x])[::-1]
            json.dump(products, outf, indent=2)
