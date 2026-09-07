---
assurance:
  id: t-12
  base: sha256:b57e9879ebb4868fda5df6b0b5c6f73d67e129904a9961b5f5ea2f6f231e156f
---
# Add dates from the Homes results header after a no-dates search

> Prove that a guest who reached Homes results with destination and guests only can add valid dates later from the results header and stay on the results page.

## Step 1

Open {{homepage_url}} in a fresh browser session and go to the airbnb.co.in homepage search bar.

## Step 2 @verifies ac-35

On the homepage search bar, enter Goa in Where, leave Check-in and Check-out empty, set Who to {{guest_count_no_dates}}, and run Search, then assert the Homes results page opens with Goa and {{guest_count_no_dates}} shown in the results header.

## Step 3

On the Homes results page for the Goa no-dates query, store the current results route and header query as baseline_no_dates_results_state.

## Step 4 @verifies ac-33, ac-35, ac-36

In the results header on that results page, enter Check-in {{added_check_in_date}} and Check-out {{added_check_out_date}} and run Search there, then assert the browser stays on a Homes results route instead of the homepage and the results header now shows Goa, {{added_check_in_date}}, {{added_check_out_date}}, and {{guest_count_no_dates}}.
