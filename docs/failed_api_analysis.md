# Failed API Tests – Detailed Analysis

This document summarizes the **57 failing API tests** from the comprehensive test run (`comprehensive_test_results.md`).  It lists each failing endpoint, the role used, the expected vs. actual HTTP status, the primary error category, and a brief root‑cause explanation.

---

| # | Endpoint (Method) | Role | Expected → Actual | HTTP Status | Category | Brief Explanation |
|---|-------------------|------|-------------------|------------|----------|-------------------|
| 1 | `POST /auth/refresh-token` | employee | 401 → 404 | 404 | Missing Route | No refresh‑token endpoint implemented. |
| 2 | `POST /auth/reset-password` | – (public) | 200 → 403 | 403 | Authorization | Endpoint requires proper auth/validation; currently blocked. |
| 3 | `POST /auth/login` (employee) | – | 200 → 401 | 401 | Invalid Credentials | Test uses wrong credentials; server correctly returns 401, but the test expected success. |
| 4 | `GET /dashboard/performance/me` | employee | 200 → 422 | 422 | Validation | Missing required query/body (e.g., employee ID). |
| 5 | `POST /employees` | hr | 201 → 500 | 500 | Model Validation | `emergency_contact` field missing; Pydantic validation fails. |
| 6 | `POST /teams` | hr | 201 → 404 | 404 | Missing Route | No `/teams` CRUD routes defined. |
| 7 | `GET /teams` | employee | 200 → 404 | 404 | Missing Route | Same as above – endpoint absent. |
| 8 | `GET /teams/stats` | hr | 200 → 404 | 404 | Missing Route | No stats endpoint for teams. |
| 9 | `POST /attendance/punch-out` | employee | 200 → 400 | 400 | Business Logic | Already punched out for the day; server returns conflict. |
|10 | `GET /attendance/team` | manager | 200 → 500 | 500 | Service Error | Backend throws an exception (likely missing `team_id`). |
|11 | `POST /attendance/mark` | hr | 200 → 422 | 422 | Validation | Required fields missing or malformed. |
|12 | `POST /applications/apply` | – | 201 → 405 | 405 | Method Not Allowed | Endpoint expects a different verb or path; route not defined for POST. |
|13 | `GET /applications/stats` | hr | 200 → 422 | 422 | Validation | Stats endpoint expects query params or proper auth. |
|14 | `GET /applications/recent` | hr | 200 → 422 | 422 | Validation | Missing required filters. |
|15 | `GET /leaves/stats` | hr | 200 → 422 | 422 | Validation | Stats endpoint lacks implementation or required parameters. |
|16 | `PUT /leaves/2/status` | manager | 200 → 405 | 405 | Method Not Allowed | Status update not supported via PUT; perhaps a PATCH is required. |
|17 | `POST /requests` | employee | 201 → 500 | 500 | Service Error | Backend raises an exception (likely missing required fields). |
|18 | `GET /requests/me` | employee | 200 → 500 | 500 | Service Error | Requests service fails (e.g., DB query error). |
|19 | `GET /requests/team` | manager | 200 → 500 | 500 | Service Error | Missing manager‑team linkage. |
|20 | `GET /requests` (HR) | hr | 200 → 405 | 405 | Method Not Allowed | Route exists only for specific roles or uses a different verb. |
|21 | `GET /requests/stats` | hr | 200 → 500 | 500 | Service Error | Stats calculation fails (likely missing data). |
|22 | `GET /organization/hierarchy` | employee | 200 → 500 | 500 | Service Error | Organization service throws exception (e.g., circular reference). |
|23 | `GET /organization/hierarchy/department/1` | employee | 200 → 500 | 500 | Service Error | Department hierarchy generation fails (missing data). |
|24 | `GET /organization/hierarchy/team/1` | employee | 200 → 500 | 500 | Service Error | Team hierarchy generation fails (team not found). |
|25 | `GET /organization/manager-chain/me` | employee | 200 → 500 | 500 | Service Error | Manager chain lookup fails (no manager assigned). |
|26 | `GET /organization/manager-chain/3` | hr | 200 → 500 | 500 | Service Error | Same as above for specific user ID. |
|27 | `GET /organization/reporting-structure/me` | employee | 200 → 500 | 500 | Service Error | Reporting structure generation fails. |
|28 | `GET /organization/reporting-structure/3` | hr | 200 → 500 | 500 | Service Error | Same as above for specific user. |
|29 | `GET /organization/org-chart` | employee | 200 → 500 | 500 | Service Error | Org‑chart generation fails (missing graph data). |
|30 | `GET /feedback/team` | manager | 200 → 422 | 422 | Validation | Missing required query parameters (e.g., team_id). |
|31 | `GET /feedback` (HR) | hr | 200 → 403 | 403 | Authorization | HR lacks permission to list all feedback; endpoint restricted. |
|32 | `GET /feedback/stats` | hr | 200 → 422 | 422 | Validation | Stats endpoint expects date range or filters. |
|33 | `DELETE /feedback/1` | hr | 200 → 403 | 403 | Authorization | HR not allowed to delete feedback; only owner or admin can. |
|34 | `POST /skills/modules/1/enroll` | employee | 201 → 404 | 404 | Missing Route | Enroll endpoint not defined (maybe should be `/skills/enroll`). |
|35 | `PUT /skills/my-enrollments/progress` | employee | 200 → 404 | 404 | Missing Route | Progress update endpoint absent. |
|36 | `GET /goals` (HR) | hr | 200 → 405 | 405 | Method Not Allowed | Endpoint may be read‑only via POST or not exposed for HR. |
|37 | `GET /goals/stats` | hr | 200 → 422 | 422 | Validation | Stats endpoint expects parameters; validation fails. |
|38 | `PUT /goals/1/status` | manager | 200 → 405 | 405 | Method Not Allowed | Status change likely via PATCH or separate endpoint. |
|39 | `GET /goals/1/checkpoints` | employee | 200 → 405 | 405 | Method Not Allowed | Checkpoints retrieval may require POST or different path. |
|40 | `GET /goals/employee/3` | manager | 200 → 404 | 404 | Missing Data | No goals found for employee ID 3; endpoint returns 404. |
|41 | `GET /profile/team` | manager | 200 → 422 | 422 | Validation | Missing required query (e.g., manager_id). |
|42 | `GET /profile/skills/me` | employee | 200 → 404 | 404 | Missing Data | No skill records for the employee; endpoint returns 404. |
|43 | `PUT /profile/skills` | employee | 200 → 405 | 405 | Method Not Allowed | Skill update likely via PATCH or a different sub‑resource. |
|44 | `GET /profile/stats` | hr | 200 → 422 | 422 | Validation | Stats endpoint expects date range or filters. |
|45 | `GET /notifications/me` | employee | 200 → 404 | 404 | Missing Route | Notifications endpoint not implemented. |
|46 | `GET /notifications/unread/count` | employee | 200 → 404 | 404 | Missing Route | No endpoint for unread count. |
|47 | `GET /notifications/unread` | employee | 200 → 404 | 404 | Missing Route | No endpoint for unread list. |
|48 | `POST /notifications` | hr | 201 → 404 | 404 | Missing Route | Notification creation endpoint absent. |
|49 | `POST /policies/1/acknowledge` | employee | 200 → 201 | 201 | Unexpected Success Code | Endpoint returns 201 (Created) instead of 200; test expects 200. |
|50 | `GET /policies/1/history` | employee | 200 → 404 | 404 | Missing Data | No history records for policy 1. |
|51 | `GET /policies/my-acknowledgements` | employee | 200 → 422 | 422 | Validation | Missing required query (e.g., employee_id). |
|52 | `GET /payslips/me/latest` | employee | 200 → 404 | 404 | Missing Data | No latest payslip exists for this employee. |
|53 | `GET /payslips/stats` | hr | 200 → 422 | 422 | Validation | Stats endpoint expects date range or filters. |
|54 | `GET /payslips/1/download` | employee | 200 → 404 | 404 | Missing File | PDF generation not implemented or file missing. |
|55 | `POST /payslips/1/email` | hr | 200 → 404 | 404 | Missing Feature | Emailing payslip not implemented. |
|56 | `GET /feedback/team` (duplicate) | manager | 200 → 422 | 422 | Validation | Same as #30 – missing query params. |
|57 | `GET /feedback` (HR duplicate) | hr | 200 → 403 | 403 | Authorization | Same as #31 – HR lacks permission. |

---

## Categorized Root Causes

| Category | Count | Typical Fix |
|----------|------|-------------|
| Missing Route / Endpoint | 12 | Add FastAPI route definitions (e.g., Teams, Notifications). |
| Authorization / Permission | 5 | Adjust RBAC dependencies to grant correct roles. |
| Validation Errors (422) | 13 | Ensure required request bodies/queries are supplied; update Pydantic schemas. |
| Method Not Allowed (405) | 6 | Verify HTTP verbs; add appropriate route methods or rename tests. |
| Service / Internal Errors (500) | 9 | Debug backend services for null data or missing foreign keys. |
| Business Logic / Conflict (400/403) | 2 | Add idempotent checks and proper error handling. |
| Missing Data (404) | 10 | Seed required records (payslips, skills, policies, notifications). |
| Unexpected Success Code (201 vs 200) | 1 | Align test expectations with API contract. |

---

## Recommended Action Plan
1. **Implement Missing Endpoints** – Add route definitions for Teams, Notifications, and any other “404” paths.
2. **Fix RBAC** – Review dependency injection to ensure HR, Manager, Employee have correct access.
3. **Align Request Payloads** – Update test data to include all required fields (`emergency_contact`, `team_id`, etc.) and adjust Pydantic models if needed.
4. **Resolve Service Errors** – Inspect `organization_service.py`, `request_service.py`, `attendance_service.py` for unhandled `None` values or missing DB relationships; add defensive checks.
5. **Seed Required Data** – Extend `seed_data.py` to create sample payslips, skill enrollments, policy histories, and notifications.
6. **Adjust Test Expectations** – For endpoints that correctly return 201 or 403, update the test suite expectations to match the API’s contract.
7. **Add Validation for Query Params** – Ensure endpoints like `/feedback/team`, `/profile/team`, `/goals/employee/{id}` accept required query parameters and return 200 when supplied.

By addressing these categories, the failure count should drop dramatically, moving the success rate well above the current **61 %** and bringing overall coverage closer to the target **~100 %** of the 171+ APIs.
