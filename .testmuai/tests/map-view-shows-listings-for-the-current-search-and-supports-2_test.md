---
assurance:
  id: t-9
  base: sha256:f267aeffab4b879f0813dfb7d28adb4c9d327c9b5da62cf29f53f280fdf9bf30
---
# Map view shows listings for the current search and supports location-based refinement

> Prove the results page exposes the Map and supports location-based refinement for the current search.

## Step 1

Open {{start_url}} on airbnb.co.in, run a Homes search for Hanoi with Check-in {{check_in_date}}, Check-out {{check_out_date}}, and Who {{guest_count}}, and land on the Homes results page.

## Step 2 @verifies ac-28, ac-23

On the Homes results page for Hanoi, open the Map view and assert the page exposes a Map control and shows listings on the map for the current search.

## Step 3 @verifies ac-24

Within the Map view for the Hanoi search, move the viewport to {{map_refinement_target}} and use the map's available refresh behavior for the new area, then assert the map continues the search in location-based refinement mode for that new visible area.
