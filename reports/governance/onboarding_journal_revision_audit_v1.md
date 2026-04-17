# Onboarding & Journal Revision Audit v1

_Generated: 2026-04-17T04:55:46.663078+00:00_

## Onboarding unification check
- governance_index_read_order_count: 0
- onboarding_read_order_count: 0
- overlap_count: 0
- jaccard_similarity: 0.000
- missing_read_order_paths_on_disk: 0

## Onboarding time estimate
- quick_path_minutes (30s per document): 0.0
- standard_path_minutes (60s per document): 0.0
- deep_path_minutes (105s per document): 0.0

## Journal revision audit
- components_with_versioned_streams: 8
- stale_write_violations: 0
- historical_marker_violations: 0

## Journal rows
### scale-radio-autoswitch
- active_stream: `journals/scale-radio-autoswitch/stream_v1.md`
- older_streams: `-`
- stale_write_violation: `false`
- historical_marker_missing: `-`

### scale-radio-bridge
- active_stream: `journals/scale-radio-bridge/stream_v1.md`
- older_streams: `-`
- stale_write_violation: `false`
- historical_marker_missing: `-`

### scale-radio-faceplate
- active_stream: `journals/scale-radio-faceplate/stream_v1.md`
- older_streams: `-`
- stale_write_violation: `false`
- historical_marker_missing: `-`

### scale-radio-fun-line
- active_stream: `journals/scale-radio-fun-line/stream_v1.md`
- older_streams: `-`
- stale_write_violation: `false`
- historical_marker_missing: `-`

### scale-radio-hardware
- active_stream: `journals/scale-radio-hardware/stream_v1.md`
- older_streams: `-`
- stale_write_violation: `false`
- historical_marker_missing: `-`

### scale-radio-starter
- active_stream: `journals/scale-radio-starter/stream_v1.md`
- older_streams: `-`
- stale_write_violation: `false`
- historical_marker_missing: `-`

### scale-radio-tuner
- active_stream: `journals/scale-radio-tuner/stream_v2.md`
- older_streams: `journals/scale-radio-tuner/stream_v1.md`
- stale_write_violation: `false`
- historical_marker_missing: `-`

### system-integration-normalization
- active_stream: `journals/system-integration-normalization/stream_v6.md`
- older_streams: `journals/system-integration-normalization/stream_v1.md, journals/system-integration-normalization/stream_v2.md, journals/system-integration-normalization/stream_v3.md, journals/system-integration-normalization/stream_v4.md, journals/system-integration-normalization/stream_v5.md`
- stale_write_violation: `false`
- historical_marker_missing: `-`

## Executed logic
1. parse read-order lists in governance index + onboarding docs
2. compute overlap/unification and path existence
3. estimate onboarding time using quick/standard/deep model
4. audit journal stream revision discipline via git last-commit timestamps and historical markers
