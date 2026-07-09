# KB-0064: Laptop overheating and fan noise

Category: Laptop
Audience: Service Desk and second-line support
Confidence: Medium

## Symptoms
Inspect CPU usage, firmware version, blocked vents, battery health, and endpoint scanning schedule.

## Resolution
1. Confirm the affected user and device.
2. Check related open tickets in the service database.
3. Compare the software version against the known-good version.
4. Apply the documented workaround.
5. Escalate to Network Team if the issue persists.

## Related SQL fields
tickets.category = "Laptop"
tickets.status
tickets.priority
assets.hostname
software_versions.version
