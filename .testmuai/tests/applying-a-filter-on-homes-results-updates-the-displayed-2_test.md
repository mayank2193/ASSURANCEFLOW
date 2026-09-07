---
assurance:
  id: t-8
  base: sha256:27231802f71933be6f73e0931932ec2ebf02b46c2f05c7f31a4de3f154de1e9e
---
# Applying a filter on Homes results updates the displayed results

> Prove the results page exposes Filters and updates results after a filter is applied.

## Step 1

Open {{start_url}} on airbnb.co.in, run a Homes search for Hanoi with Check-in {{check_in_date}}, Check-out {{check_out_date}}, and Who {{guest_count}}, and land on the Homes results page.

## Step 2

On the Homes results page for Hanoi, store the current visible results signature as baseline_results_signature.

## Step 3 @verifies ac-27, ac-22

Open Filters on the Homes results page, apply {{filter_name}} = {{filter_value}}, and update the search, then assert the Filters control is available and the visible results differ from baseline_results_signature after the filter is applied.
