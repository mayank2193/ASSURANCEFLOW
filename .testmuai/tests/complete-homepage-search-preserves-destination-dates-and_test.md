---
assurance:
  id: t-1
  base: sha256:80cc92cd57c88524adb2607b3111558541f81a504e9b3ee950da59b84ee4237a
---
# Complete homepage search preserves destination, dates, and guests on Homes results

> Prove the complete-input flow routes from the homepage to Homes results and preserves destination, dates, and guests in the results header.

## Step 1 @verifies ac-6, ac-8

Open {{homepage_url}} in a fresh browser session and go to the airbnb.co.in homepage search bar, then assert the search fields are labeled Where, Check-in, Check-out, and Who and the call to action reads Search.

## Step 2 @verifies ac-1, ac-2, ac-3, ac-12, ac-13

On the homepage search bar, enter Hanoi in Where, set Check-in to {{check_in_date}}, set Check-out to {{check_out_date}}, set Who to {{guest_count}}, and run Search, then assert the Homes results page opens with Hanoi, {{check_in_date}}, {{check_out_date}}, and {{guest_count}} shown in the results header.
