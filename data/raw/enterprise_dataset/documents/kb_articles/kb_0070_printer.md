# KB-0070: Printer offline troubleshooting

Category: Printer
Audience: Service Desk and second-line support
Confidence: Medium

## Symptoms
Check printer queue, network reachability, driver version, paper status, and print spooler service.

## Resolution
1. Confirm the affected user and device.
2. Check related open tickets in the service database.
3. Compare the software version against the known-good version.
4. Apply the documented workaround.
5. Escalate to Network Team if the issue persists.

## Related SQL fields
tickets.category = "Printer"
tickets.status
tickets.priority
assets.hostname
software_versions.version
