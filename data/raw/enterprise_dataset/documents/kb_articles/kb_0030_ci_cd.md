# KB-0030: CI pipeline failure investigation

Category: CI/CD
Audience: Service Desk and second-line support
Confidence: Medium

## Symptoms
Review runner availability, dependency cache, secret rotation, test flakiness, and recent merge requests.

## Resolution
1. Confirm the affected user and device.
2. Check related open tickets in the service database.
3. Compare the software version against the known-good version.
4. Apply the documented workaround.
5. Escalate to Identity Team if the issue persists.

## Related SQL fields
tickets.category = "CI/CD"
tickets.status
tickets.priority
assets.hostname
software_versions.version
