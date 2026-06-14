from pitchmind_db.audit_progress import progress_channel, publish_audit_progress


def test_progress_channel_format():
    assert progress_channel("abc-123") == "audit:progress:abc-123"


def test_publish_audit_progress_no_redis_does_not_raise():
    publish_audit_progress("audit-1", status="running", query_results_count=2)
