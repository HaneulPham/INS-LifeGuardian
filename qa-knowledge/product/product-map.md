# INS LifeGuardian Product Map

INS LifeGuardian is a live production healthcare/safety monitoring/client support platform.

## Platforms

- CP Desktop
- CP Web
- Portal Web
- Mobile SOS iOS
- Mobile SOS Android
- Mobile Carer iOS
- Mobile Carer Android
- Backend APIs
- Background jobs
- Third-party integrations

## Core Modules

| Module | Main Platform | Integration / Risk |
|---|---|---|
| Welfare Check | CP, Mobile | Schedule, reminder, escalation, check-in, notification |
| Alerts/Restorals | CP, Backend | Alarm delivery, restoral, Twilio/SMS/email, logs |
| Emergency Alarm | Mobile, Watch, Backend | FCM, SIP/Twilio, emergency escalation |
| Notifications | Mobile, Backend | FCM, SMS, email, notification logs |
| Care Plan Tasks | Mobile, CP, Carer | Schedule, occurrence, check-in, sync |
| Device Setup/Checklist | CP Desktop | Device setup steps, service request progress |
| Service Requests/Work Orders | CP Desktop | Devices/assets/client file mapping |
| Billing/Reports | CP Desktop/Web | QuickBooks, export, invoice data |
| Client File | CP Desktop/Web, Portal | Medical/client/device data, audit history |
| Assets/Devices | CP Desktop/Web | Device assignment, removal, data integrity |
| Roles/Permissions | CP/Portal | Authorization, tenant/village access |
| Document Change Log | CP/Backend | Audit trail and history tracking |

## QA Rule

When analyzing a ticket, Codex must identify:
- Impacted module
- Impacted platform
- Impacted API/backend/data
- Impacted integrations
- Regression areas
- Safety/business risk
