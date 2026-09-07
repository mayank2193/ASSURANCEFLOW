---
assurance:
  id: t-6
  base: sha256:ae4644b362355a66874cc6c943d8b46d962e4a6390900eed2d09f17866fd9b96
---
# Keyboard navigation reaches homepage search and results refinement controls in order

> Prove the homepage search fields and CTA are reachable in order by Tab and the results-page Filters and Map controls are keyboard-accessible with visible focus indication.

## Step 1 @verifies ac-6, ac-8, ac-9

Open {{homepage_url}} on airbnb.co.in and, using keyboard navigation on the homepage search bar, move focus through the search controls until the Search button is reached, then assert the focus order is Where, Check-in, Check-out, Who, and Search.

## Step 2

Still using the web UI, complete a Homes search for Hanoi with Check-in {{check_in_date}}, Check-out {{check_out_date}}, and Who {{guest_count}}, and land on the Homes results page.

## Step 3 @verifies ac-4, ac-5, ac-10, ac-11

On the Homes results page, navigate by keyboard to the refinement controls, then assert the Filters and Map controls are keyboard-accessible and each shows a visible focus indicator when focused.
