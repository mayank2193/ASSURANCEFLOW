---
assurance:
  id: t-2
  base: sha256:82c31032068491b648b1ebbbfcd746e3e20a9078bba2f33b785888eb4f62ac92
---
# Homepage search without dates preserves destination and guests and allows date entry later

> Prove the partial-input flow routes with destination and guests only, preserves those inputs, and allows dates to be added later on the results page.

## Step 1 @verifies ac-6, ac-8

Open {{homepage_url}} in a fresh browser session and go to the airbnb.co.in homepage search bar, then assert the search fields are labeled Where, Check-in, Check-out, and Who and the call to action reads Search.

## Step 2 @verifies ac-1, ac-2, ac-3

On the homepage search bar, enter Goa in Where, leave Check-in and Check-out empty, set Who to {{guest_count}}, and run Search, then assert the Homes results page opens with Goa and {{guest_count}} shown in the results header.

## Step 3 @verifies ac-14

On the Homes results page for Goa, open the date-entry controls in the search header and stay on the results page, then assert Check-in and Check-out can be entered there without navigating back to the homepage.
