# INS LifeGuardian project scope

Consider only areas supported by the ticket or evidence; do not force every area into every review.

## Platforms

- CP Desktop and CP Web
- Portal Web
- Mobile SOS iOS and Android
- Mobile Carer iOS and Android
- Backend APIs, background services, and jobs

## Modules

- Welfare Check; Alerts and Restorals; Emergency Alarm; Notifications
- Tasks and Care Plan Tasks; Device Setup and Checklist
- Service Requests and Work Orders; Assets and Devices
- Vital Signs and Thresholds; Billing; Reports; Chat
- Roles and Permissions; Client File and Village inheritance
- Document Change Log

## Integrations and operational areas

- FCM and push, SMS, email, Twilio
- QuickBooks and billing
- Authentication and authorization
- Synchronization, jobs, queues, retries, and alert delivery
- Notification, audit, activity, document-change, and operational logs
- Privacy and sensitive-data exposure across UI, notifications, URLs, reports, exports, screenshots, and logs
- Test-data isolation, non-production recipients, cleanup, rollback, and preservation of required audit evidence

For each task, identify the affected module, platforms, backend/data, integrations, regression areas, and safety or business risk. Do not claim root cause, persistence, permissions, consumer usage, or integration behaviour without evidence.
