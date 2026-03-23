# Idea: Neighbourhood Tool Library

A web app where people in a local neighbourhood can list tools and equipment they own and are willing to lend out. Other neighbours can browse, request to borrow items, and coordinate pickup/return.

## What the user has told us so far

- **Problem:** People buy expensive tools (drills, pressure washers, ladders) they use once or twice a year. Neighbours could share instead.
- **Target users:** Residents in a single neighbourhood or apartment complex (~50-500 people).
- **Type:** Web app, mobile-friendly but not a native app.
- **Scale:** Small community tool — start with one neighbourhood, maybe expand later.
- **Key features for MVP:**
  - List an item with photo, description, and availability
  - Browse and search items nearby
  - Request to borrow (sends notification to owner)
  - Simple messaging between borrower and owner
  - Track who has what (basic lending ledger)
- **Auth:** Yes, email-based signup with neighbourhood verification (e.g. invite code).
- **Data:** Item listings, user profiles, borrow requests, messages.
- **External services:** Image upload (S3 or similar), email notifications.
- **Tech preferences:** Python/Django for backend, plain HTML+HTMX for frontend, PostgreSQL, deploy on Railway or Fly.io.
- **Constraints:** Must work on mobile browsers. No native app needed.
