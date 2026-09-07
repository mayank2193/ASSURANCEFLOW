---
mode: testing
max_steps: 30
timeout: 300
variables: {}
---

# Refine search results using the Filters control on the results page

## Step 1
Perform a search from the homepage with "Goa, India" and "2 adults", leaving dates empty.
Get the initial number of results displayed and save as {{initial_results_count}}.
Apply a maximum price that is lower than the default in the 'Price range' filter.
Verify the number of listings displayed is reduced from the initial count.
Verify the **Filters** button indicates that a filter is active.
