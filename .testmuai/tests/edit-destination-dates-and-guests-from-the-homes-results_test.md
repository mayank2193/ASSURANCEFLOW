---
assurance:
  id: t-11
  base: sha256:077a1896b98d78e8aaa65d37482677c78e64c6bfbe4fe1fdb00853ce619679a5
---
# Edit destination, dates, and guests from the Homes results header in place

> Prove that a guest can change any one source-named parameter family already present in the Homes results header and refresh the results in place without returning to the homepage.

## Step 1

Open {{homepage_url}} in a fresh browser session and go to the airbnb.co.in homepage search bar.

## Step 2 @verifies ac-35

On the homepage search bar, enter Hanoi in Where, set Check-in to {{initial_check_in_date}}, set Check-out to {{initial_check_out_date}}, set Who to {{initial_guest_count}}, and run Search, then assert the Homes results page opens with Hanoi, {{initial_check_in_date}}, {{initial_check_out_date}}, and {{initial_guest_count}} shown in the results header.

## Step 3

On the Homes results page for the Hanoi query, store the current results route and header query as baseline_results_header_state.

## Step 4 @verifies ac-33, ac-34, ac-35

In the results header, change Where from Hanoi to Goa and run Search from the results page, then assert the browser stays on a Homes results route instead of the homepage and the results header now shows Goa with {{initial_check_in_date}}, {{initial_check_out_date}}, and {{initial_guest_count}}.

## Step 5 @verifies ac-33, ac-34, ac-35

On the same Goa results page, change Check-in to {{edited_check_in_date}} and Check-out to {{edited_check_out_date}} from the results header and run Search there, then assert the browser stays on a Homes results route and the results header now shows Goa with {{edited_check_in_date}}, {{edited_check_out_date}}, and {{initial_guest_count}}.

## Step 6 @verifies ac-33, ac-34, ac-35

On the same Goa results page, change Who to {{edited_guest_count}} from the results header and run Search there, then assert the browser stays on a Homes results route and the results header now shows Goa with {{edited_check_in_date}}, {{edited_check_out_date}}, and {{edited_guest_count}}.
