# KB-0103: CRM slow performance checklist

Category: CRM
Audience: Service Desk and second-line support
Confidence: Medium

## Symptoms
Investigate browser cache, API latency, database locks, recent releases, and user-specific permission rules.

## Resolution
1. Confirm the affected user and device.
2. Check related open tickets in the service database.
3. Compare the software version against the known-good version.
4. Apply the documented workaround.
5. Escalate to Identity Team if the issue persists.

## Related SQL fields
tickets.category = "CRM"
tickets.status
tickets.priority
assets.hostname
software_versions.version
