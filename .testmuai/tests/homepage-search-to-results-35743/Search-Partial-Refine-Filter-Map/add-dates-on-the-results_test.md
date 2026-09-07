---
mode: testing
max_steps: 30
timeout: 300
variables: {}
---

# Add dates on the results page after a partial search and verify results update

## Step 1
Perform a search from the homepage with "Goa, India" and "2 adults", leaving dates empty. On the results page, add a valid check-in date in the upcoming month and a valid check-out date that is at least 5 days after the check-in date, then apply the dates with the **Search** button. Verify the search header now displays the selected dates. Verify the listings on the page now show total price or per-night price information.
