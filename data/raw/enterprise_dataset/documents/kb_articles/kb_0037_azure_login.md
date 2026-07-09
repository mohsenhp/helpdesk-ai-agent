# KB-0037: Azure SSO conditional access troubleshooting

Category: Azure Login
Audience: Service Desk and second-line support
Confidence: Medium

## Symptoms
If users cannot log in, review conditional access policies, MFA status, device compliance, and sign-in risk events.

## Resolution
1. Confirm the affected user and device.
2. Check related open tickets in the service database.
3. Compare the software version against the known-good version.
4. Apply the documented workaround.
5. Escalate to Platform Team if the issue persists.

## Related SQL fields
tickets.category = "Azure Login"
tickets.status
tickets.priority
assets.hostname
software_versions.version
