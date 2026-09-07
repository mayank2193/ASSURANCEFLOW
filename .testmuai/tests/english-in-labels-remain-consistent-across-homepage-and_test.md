---
assurance:
  id: t-7
  base: sha256:4a8a4e4b99c5bc10f21ece436bb8b32c84a0bfad79d5875886d6a57d28c3e309
---
# English-IN labels remain consistent across homepage and results search controls

> Prove the journey keeps the labels Where, Check-in, Check-out, Who, and Search across the homepage and results pages.

## Step 1 @verifies ac-6, ac-8

Open {{homepage_url}} on airbnb.co.in and go to the homepage search bar, then assert the homepage labels read Where, Check-in, Check-out, and Who and the call to action reads Search.

## Step 2 @verifies ac-7

From the homepage, run a Homes search for Goa with Who set to {{guest_count}} and no dates, and land on the results page search header, then assert the results-page search controls still use the labels Where, Check-in, Check-out, and Who.
