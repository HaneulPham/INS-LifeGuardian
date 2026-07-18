# INS Test Case Style Example

## Good Expected Result Format

**Verify after step 4:**
- The dropdown opens successfully.
- Billing is displayed as a selectable Type.
- Billing appears exactly once.
- Billing is not disabled or visually unavailable.
- No blank, duplicate, or malformed Type value is displayed.

## Good Expected Integration Format

**Verify after step 7:**
- CP backend saves the selected Type value.
- Reopen API returns the saved value correctly.
- No duplicate record is created.
- No FCM, SMS, email, Twilio call, or alert escalation is triggered for this configuration-only update.
