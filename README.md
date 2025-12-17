# ledger-system-account
A ledger sustem for managing accounts

A Django-based ledger system for managing financial accounts and transactional entries.

The application supports creating and maintaining debit and credit records, along with basic reporting and search functionality. It is designed to handle structured financial data with correctness and consistency as a priority.

## Features
- Add new ledger entries with debit and credit details
- Edit and update existing transaction records
- Search and filter entries by:
  - Financial year
  - Month
  - From date / To date
- Manage transactional data stored in a relational database

## Tech Stack
- Backend: Python, Django
- Frontend: HTML, CSS
- Database: PostgreSQL

## Notes
This project focuses on backend logic, data validation, and database interactions. Some early design decisions (especially around querying and data access patterns) could be improved as data volume grows.
