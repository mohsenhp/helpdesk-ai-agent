# KB-0094: VPN connection fails after Windows update

Category: VPN
Audience: Service Desk and second-line support
Confidence: High

## Symptoms
Users may experience failed tunnel negotiation after a Windows update. Check client version, reset network adapter, clear cached credentials, and verify split tunneling policy.

## Resolution
1. Confirm the affected user and device.
2. Check related open tickets in the service database.
3. Compare the software version against the known-good version.
4. Apply the documented workaround.
5. Escalate to Identity Team if the issue persists.

## Related SQL fields
tickets.category = "VPN"
tickets.status
tickets.priority
assets.hostname
software_versions.version
