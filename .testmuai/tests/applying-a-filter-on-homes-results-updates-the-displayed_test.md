---
assurance:
  id: t-3
  base: sha256:51124daffb94af9f4af6a9c1c92f4961ae060a6e6615a0e0ac6681c861d86d38
---
# Applying a filter on Homes results updates the displayed results

> Prove the results page exposes Filters and updates results after a filter is applied.

## Step 1

Open {{homepage_url}}, run a Homes search for Hanoi with Check-in {{check_in_date}}, Check-out {{check_out_date}}, and Who {{guest_count}}, and land on the Homes results page.

## Step 2

On the Homes results page for Hanoi, store the current visible results signature as baseline_results_signature.

## Step 3 @verifies ac-4, ac-15

Open Filters on the Homes results page, apply {{filter_name}} = {{filter_value}}, and update the search, then assert the Filters control is available and the visible results differ from baseline_results_signature after the filter is applied.
