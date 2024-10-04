
# Social Auth Application with Secure Authentication and Authorization

This project implements a secure social auth management application using FastAPI, featuring OAuth2 authentication, JWT-based session management, role-based access control, CSRF protection, input validation, and more. The application follows best practices in line with OWASP security standards.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies and Packages](#technologies-and-packages)
- [Setup Instructions](#setup-instructions)
- [Implementation Details](#implementation-details)
  - [Step 1: OAuth Integration](#step-1-oauth-integration)
  - [Step 2: JWT Authentication](#step-2-jwt-authentication)
  - [Step 3: Secure Token Handling](#step-3-secure-token-handling)
  - [Step 4: Authorization Middleware](#step-4-authorization-middleware)
  - [Step 5: CSRF Protection](#step-5-csrf-protection)
  - [Step 6: Input Validation and Rate Limiting](#step-6-input-validation-and-rate-limiting)
  - [Step 7: Security Testing](#step-7-security-testing)
- [OWASP Compliance](#owasp-compliance)
- [Recommendations](#recommendations)
- [License](#license)

## Overview
This application provides social auth with secure user authentication and role-based access control. It uses Google OAuth2 for user authentication and JWTs for session management. The application also incorporates several security features, including CSRF protection, rate limiting, and input validation, to mitigate common web application vulnerabilities.

## Features
- User authentication using Google OAuth2.
- JWT-based session management with access and refresh tokens.
- Role-based access control (admin, user).
- CSRF protection using HTTP-only cookies.
- Rate limiting for sensitive endpoints.
- Input validation using Pydantic models.
- Comprehensive unit tests for authentication and authorization flows.

## Technologies and Packages
- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- **Authlib**: Used for OAuth2 integration.
- **PyJWT**: For generating and verifying JSON Web Tokens (JWTs).
- **SQLAlchemy**: For database ORM.
- **Pydantic**: For data validation and settings management.
- **SlowAPI**: For rate limiting.
- **pip-audit / safety**: For auditing Python packages for known vulnerabilities.

## Setup Instructions

### Prerequisites
- Python 3.7+
- pip for installing dependencies

### Installation
1. **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/student-crud-app.git
    ```
2. **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\ctivate
    ```
3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**
    - Create a `.env` file in the root directory and add the necessary environment variables:
      ```env
      SECRET_KEY=your-secret-key
      ALGORITHM=HS256
      ACCESS_TOKEN_EXPIRE_MINUTES=30
      GOOGLE_CLIENT_ID=your-google-client-id
      GOOGLE_CLIENT_SECRET=your-google-client-secret
      OAUTH_REDIRECT_URI=http://127.0.0.1:8000/api/v1/oauth/callback
      ```

5. **Run the Application**
    ```bash
    uvicorn app.main:app --reload
    ```

6. **Access the Application**
    - Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000)/docs to access the API documentation via Swagger UI.

## Implementation Details

### Step 1: OAuth Integration
- Implemented Google OAuth2 for user login using the `authlib` library.
- Defined `/login/google` and `/callback` routes for initiating the OAuth2 flow and processing the callback.

### Step 2: JWT Authentication
- Used `PyJWT` to generate and verify JWTs for user sessions.
- Embedded user roles in JWTs to support role-based access control.
- Implemented token expiration for both access and refresh tokens.

### Step 3: Secure Token Handling
- **Initial Setup**: Tokens were stored in HTTP-only cookies for secure client-side storage.
- **Current Setup**: Switched to sending tokens in the JSON response for demonstration purposes.
- Implemented token expiration and refresh mechanisms.

### Step 4: Authorization Middleware
- Added `role` field in the user model to support different roles (admin, user).
- Implemented middleware to extract and verify JWTs, enforcing role-based access control based on the user's role.
- Protected routes based on user roles using the `require_role` dependency.

### Step 5: CSRF Protection
- Implemented CSRF protection using HTTP-only cookies to store CSRF tokens.
- Validated CSRF tokens in middleware to secure sensitive operations, particularly the OAuth flow.

### Step 6: Input Validation and Rate Limiting
- Used Pydantic models for input validation, ensuring only valid data is processed.
- Implemented rate limiting with `slowapi` to restrict the number of requests to critical endpoints, mitigating brute-force attacks.

### Step 7: Security Testing
- **Unit Tests**: Created test cases using `pytest` for authentication flows, token validation, and protected routes.
- **Vulnerability Scanning**: Used `pip-audit` and `safety` to identify known vulnerabilities in installed packages. Addressed vulnerabilities by replacing `python-jose` with `PyJWT`.

## OWASP Compliance
The application complies with several OWASP standards, including:

- **A01:2021 – Broken Access Control**: Implemented role-based access control using JWTs.
- **A02:2021 – Cryptographic Failures**: Used strong cryptographic algorithms (HS256) for JWT generation and token expiration.
- **A03:2021 – Injection**: Ensured input validation using Pydantic models to mitigate injection attacks.
- **A05:2021 – Security Misconfiguration**: Implemented CSRF protection and rate limiting.
- **A07:2021 – Identification and Authentication Failures**: Secured OAuth flows and token expiration mechanisms.
- **A08:2021 – Software and Data Integrity Failures**: Regularly audited dependencies for known vulnerabilities.

## Recommendations
- **Stress/Load Testing**:
  - Use `Locust` to simulate concurrent users and stress-test the application. This will help identify performance bottlenecks and ensure scalability.
- **Vulnerability Testing**:
  - Use `OWASP ZAP` and `Nikto` for vulnerability testing. These tools can help identify security misconfigurations, SQL injection points, and other vulnerabilities.

