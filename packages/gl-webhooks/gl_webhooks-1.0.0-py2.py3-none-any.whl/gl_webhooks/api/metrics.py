"""
/api/metrics endpoint
"""


def get(**_kwargs):
    """/api/metrics endpoint"""
    # Not returning anything is actually enough to at least have an up{job} metric
    return """
# HELP gl_webhooks_service_status Static value to imply service is up
# TYPE gl_webhooks_service_status gauge
gl_webhooks_service_status 1
"""
