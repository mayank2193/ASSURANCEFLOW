---
assurance:
  id: t-5
  base: sha256:c35d84e527dae7e5952c4468cce116032c55b5cff4e1bfc967286d10cd05cd80
---
# Search parameters can be edited from the results header without returning home

> Prove search parameters remain visible and editable on the results page so the guest can refresh results without returning to the homepage.

## Step 1

Open {{homepage_url}}, run a Homes search for Hanoi with Check-in {{check_in_date}}, Check-out {{check_out_date}}, and Who {{guest_count}}, and land on the Homes results page.

## Step 2 @verifies ac-2, ac-3, ac-7, ac-18, ac-19, ac-20

On the Homes results page header for the Hanoi search, open the existing search summary and assert the destination, date, and guest controls are visible with the labels Where, Check-in, Check-out, and Who, with Hanoi and {{guest_count}} shown, and each control is editable.

## Step 3

On the same results page, store the current visible results signature as baseline_header_results.

## Step 4 @verifies ac-21

In the results header, change Where to Goa, set Check-in to {{edited_check_in_date}}, set Check-out to {{edited_check_out_date}}, set Who to {{edited_guest_count}}, and run Search from the results page, then assert the results refresh on the results page for Goa without returning to the homepage.
