# Development Plan and Suggested Commit Timeline

This is a realistic development plan for building the project gradually across multiple sessions.

## Phase 1 - Project Setup

- Create Flask project folder structure
- Add basic app configuration
- Set up SQLite database path
- Add requirements file

## Phase 2 - Database Design

- Add customer model
- Add service model
- Add subscription model
- Add invoice and payment models
- Add renewal model
- Add seed data for demo records

## Phase 3 - Core Features

- Implement customer listing and search
- Add customer create and edit forms
- Add customer profile page
- Add service management page
- Add subscription assignment flow

## Phase 4 - Billing

- Add invoice calculation helper
- Add invoice generation from subscription
- Add invoice history page
- Add payment recording workflow
- Fix invoice status after payment

## Phase 5 - Renewal System

- Add upcoming renewal query
- Add expired subscription query
- Add renewal reminder form
- Add renew and generate invoice workflow

## Phase 6 - Dashboard

- Add dashboard statistics
- Add recent payments section
- Add expiring plans section
- Add monthly revenue chart

## Phase 7 - Machine Learning

- Create sample subscription dataset
- Train Random Forest renewal model
- Train Logistic Regression churn model
- Add prediction form
- Add renewal probability and churn risk display
- Add simple revenue forecast

## Phase 8 - UI Improvements

- Improve dashboard spacing
- Add responsive layouts
- Clean customer and invoice tables
- Make pages screenshot friendly
- Keep white and blue visual theme consistent

## Phase 9 - Testing and Fixes

- Test customer CRUD flow
- Test invoice generation
- Test renewal invoice flow
- Fix calculation and display edge cases
- Validate forms better

## Phase 10 - Documentation

- Write README
- Add setup steps
- Add screenshots section
- Add future improvements and learning outcomes

## Suggested Commit Schedule

### Day 1

- 09:35 AM - Initial project setup
- 10:20 AM - Added Flask configuration and folder structure
- 11:40 AM - Added SQLAlchemy database setup

### Day 2

- 03:10 PM - Created customer and service models
- 04:35 PM - Added subscription model and relationships
- 06:05 PM - Added invoice, payment, and renewal models

### Day 3

- 09:50 AM - Added sample seed data for local demo
- 11:25 AM - Implemented customer listing and search
- 02:15 PM - Added customer add and edit forms
- 04:00 PM - Built customer profile page

### Day 4

- 10:05 AM - Added service management module
- 12:00 PM - Added subscription assignment workflow
- 03:30 PM - Improved customer profile subscription view

### Day 5

- 09:25 AM - Added invoice calculation helper
- 11:10 AM - Implemented invoice generation functionality
- 02:20 PM - Added invoice history table
- 04:45 PM - Integrated payment tracking

### Day 6

- 10:30 AM - Built renewal management module
- 12:40 PM - Added expiry tracking helpers
- 03:15 PM - Added renewal invoice generation

### Day 7

- 09:45 AM - Added dashboard analytics cards
- 11:35 AM - Added recent payments and expiring plans sections
- 02:10 PM - Integrated monthly revenue chart

### Day 8

- 10:00 AM - Created sample subscription dataset
- 12:25 PM - Trained renewal prediction model
- 03:05 PM - Implemented churn prediction workflow

### Day 9

- 09:40 AM - Added prediction dashboard page
- 11:15 AM - Added revenue forecasting display
- 02:30 PM - Improved UI consistency across pages
- 05:00 PM - Added mobile responsive layout fixes

### Day 10

- 09:10 AM - Fixed invoice calculation display issues
- 10:50 AM - Added form validation improvements
- 12:35 PM - Updated project documentation
- 02:45 PM - Added screenshots folder notes
- 04:20 PM - Final cleanup for portfolio use

## Suggested Commit Messages

1. Initial project setup
2. Added Flask configuration and base folders
3. Added database configuration
4. Created customer and service models
5. Added subscription model relationships
6. Created invoice payment and renewal models
7. Added sample seed data for demo
8. Implemented customer listing and search
9. Added customer create and edit forms
10. Built customer profile page
11. Added service management module
12. Added subscription assignment workflow
13. Added invoice calculation helper
14. Implemented invoice generation functionality
15. Added invoice history page
16. Integrated payment tracking
17. Built renewal management module
18. Added expiry tracking improvements
19. Added renewal invoice generation
20. Added dashboard analytics
21. Integrated monthly revenue chart
22. Created sample subscription dataset
23. Trained renewal prediction model
24. Implemented churn prediction workflow
25. Added prediction dashboard page
26. Improved UI consistency across pages
27. Added mobile responsiveness
28. Fixed invoice calculation issues
29. Added form validation improvements
30. Updated project documentation
31. Added screenshots section and final cleanup
