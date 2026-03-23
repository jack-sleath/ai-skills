# Specification: Password Reset Flow

## Overview
Users who have forgotten their password can request a reset link via email. The link expires after 30 minutes. Users must set a new password that meets complexity requirements.

## Requirements

1. A "Forgot password?" link on the login page navigates to the password reset form.
2. The reset form accepts an email address and shows a generic success message regardless of whether the email exists (to prevent email enumeration).
3. If the email exists, the system sends a password reset email containing a unique, single-use token embedded in a URL.
4. The reset token expires after 30 minutes from generation.
5. Clicking the link opens a "Set new password" form with two fields: new password and confirm password.
6. The new password must be at least 12 characters, contain at least one uppercase letter, one lowercase letter, one number, and one special character.
7. If the passwords don't match, show an inline error and do not submit.
8. If the token is expired or already used, show an error page with a link to request a new reset.
9. On successful reset, invalidate all existing sessions for that user and redirect to the login page with a success banner.
10. Rate limit: max 3 reset requests per email per hour.

## Backend Notes
- Tokens are stored as salted SHA-256 hashes in the `password_reset_tokens` table.
- The email sending is handled by an async job queue (Sidekiq).
- Existing session invalidation uses the `session_version` column on the users table.
