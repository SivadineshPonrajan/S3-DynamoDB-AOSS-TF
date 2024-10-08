import sys
import json
import requests
import argparse

# Command line arguments parsing
parser = argparse.ArgumentParser(description="Customer Comment Search Application")
parser.add_argument("aosshost", nargs='?', help="OpenSearch host URL")
args = parser.parse_args()

def print_usage():
    print("=====================================\n")
    print("Usage: python search_script.py [OpenSearch host URL]\n")
    print("or\n")
    print('Usage: python search-script.py "$(terraform output -raw -state=terraform/terraform.tfstate opensearch_endpoint)"\n')
    print("=====================================\n")

if args.aosshost is None:
    print_usage()
    sys.exit(1)

# OpenSearch details
aoss_host = args.aosshost
if not aoss_host.startswith("https://"):
    aoss_host = "https://" + aoss_host
aoss_index = "customer_comment"
url = f"{aoss_host}/{aoss_index}/_search"

# OpenSearch credentials
aoss_username = "admin"
aoss_password = "Batman@123"

def search_comments(search_keyword, start_from=0, page_size=10):
    query = {
        "from": start_from,  # Pagination's starting point
        "size": page_size,   # Number of results per batch
        "query": {
            "wildcard": {
                "Comment": {
                    "value": f"*{search_keyword}*"
                }
            }
        }
    }
    
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.get(url, auth=(aoss_username, aoss_password), headers=headers, data=json.dumps(query), timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: OpenSearch returned status code {response.status_code}. Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to connect to OpenSearch. Reason: {e}")
        return None

def display_results(results, start_from):
    if results and "hits" in results and "hits" in results["hits"]:
        hits = results["hits"]["hits"]
        total_hits = results["hits"]["total"]["value"]
        
        print(f"\n> {total_hits} Comments match the search keyword.\n")
        if hits:
            print("=====================================\n")
        for i, hit in enumerate(hits, start=start_from + 1):
            print(f"{i}. {hit['_source']['Comment']}\n")
        print("=====================================\n")
        return len(hits)
    else:
        print("No comments found or unexpected response structure from OpenSearch.")
        return 0

def main():
    search_keyword = input("Enter the keyword you want to search: ").strip()

    while not search_keyword:
        print("Error: Search keyword cannot be empty. Please try again.")
        search_keyword = input("Enter the keyword you want to search: ").strip()

    # Pagination setup
    start_from = 0
    page_size = 10

    while True:
        results = search_comments(search_keyword, start_from, page_size)
        fetched_results = display_results(results, start_from)

        if fetched_results < page_size:
            break # End of results

        # Ask user if they want to load more
        next_page = input("> Do you want to load more results? default='y' (y/n): ").strip().lower()
        if next_page == 'y' or next_page == '':
            pass
        else:
            break
        
        start_from += page_size

if __name__ == "__main__":
    if len(sys.argv) != 2 or args.aosshost is None:
        print_usage()
        sys.exit(1)
    main()
    