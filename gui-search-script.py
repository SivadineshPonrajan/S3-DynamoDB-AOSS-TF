import json
import requests
import streamlit as st
import sys
import argparse

# Command line arguments parsing
parser = argparse.ArgumentParser(description="Customer Comment Search Application")
parser.add_argument("aosshost", help="OpenSearch host URL")
args = parser.parse_args()

aoss_host = args.aosshost
if not aoss_host.startswith("https://"):
    aoss_host = "https://" + aoss_host
aoss_index = "customer_comment"
url = f"{aoss_host}/{aoss_index}/_search"

def check_connection(username, password):
    try:
        r = requests.get(aoss_host, auth=(username, password), timeout=10)
        return r.status_code == 200
    except requests.exceptions.RequestException:
        return False

def search_comments(search_keyword, username, password, start_from=0, page_size=50):
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
        r = requests.get(url, auth=(username, password), headers=headers, data=json.dumps(query), timeout=10)
        if r.status_code == 200:
            return r.json()
        else:
            st.error(f"Error: OpenSearch returned status code {r.status_code}. Response: {r.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error: Failed to connect to OpenSearch. Reason: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
    return None

st.title("Customer Comment Search")

# Session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.password = None

if not st.session_state.logged_in:
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if check_connection(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.password = password
                st.rerun()
            else:
                st.error("Login failed. Please check your credentials or the host URL.")

# Search functionality
if st.session_state.logged_in:
    # logout button - aligned to the right
    _, c1 = st.columns([5, 1])
    with c1:
        if st.button("Logout"):
            logout()
            st.rerun()

    search_keyword = st.text_input("Enter the keyword you want to search:")

    def do_search():
        if not search_keyword.strip():
            st.error("Search keyword cannot be empty.")
        else:
            # Pagination - Recursive fetch
            all_results = []
            start_from = 0
            page_size = 10

            while True:
                results = search_comments(search_keyword, st.session_state.username, st.session_state.password, start_from, page_size)
                
                if results and "hits" in results and "hits" in results["hits"]:
                    hits = results["hits"]["hits"]
                    all_results.extend(hits)
                    if len(hits) < page_size:
                        break
                    start_from += page_size  # Move to the next batch
                else:
                    st.error("Unexpected response structure from OpenSearch.")
                    break

            total_hits = len(all_results)
            st.write(f"**{total_hits} Comments match the search keyword - {search_keyword}**")
            
            if total_hits == 0:
                st.info("No comments found.")
            else:
                for i, hit in enumerate(all_results, start=1):
                    st.write(f"{i}. {hit['_source']['Comment']}")

    # Trigger search on button click
    if st.button("Search"):
        do_search()

    # Trigger search on Enter 
    if search_keyword and search_keyword != st.session_state.get('last_search', ''):
        st.session_state.last_search = search_keyword
        do_search()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: streamlit run main.py [OpenSearch host URL]")
        sys.exit(1)
