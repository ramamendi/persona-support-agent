# API Troubleshooting Guide

## 401 Unauthorized

Possible causes:

* Invalid API key
* Expired token
* Missing Authorization header

Required header:

Authorization: Bearer YOUR_API_TOKEN

## 403 Forbidden

Possible causes:

* Insufficient permissions
* Disabled account

## 500 Internal Server Error

Steps:

1. Verify request payload format.
2. Check server logs.
3. Retry after 60 seconds.

If the issue persists, contact support.
