# KB-0008: Email delivery delay investigation

Category: Email
Audience: Service Desk and second-line support
Confidence: Medium

## Symptoms
Review mail queue, SPF/DKIM/DMARC status, transport rules, and mailbox quota.

## Resolution
1. Confirm the affected user and device.
2. Check related open tickets in the service database.
3. Compare the software version against the known-good version.
4. Apply the documented workaround.
5. Escalate to Platform Team if the issue persists.

## Related SQL fields
tickets.category = "Email"
tickets.status
tickets.priority
assets.hostname
software_versions.version
