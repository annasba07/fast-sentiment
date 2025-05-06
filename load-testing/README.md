# Load Testing for Sentiment Analysis API

This directory contains tools for load testing the Sentiment Analysis API using k6, a modern load testing tool.

## Prerequisites

- [k6](https://k6.io/docs/getting-started/installation/) installed on your machine
- API deployed and accessible (either locally or in the cloud)

## Running Load Tests

### Basic Load Test

To run the default load test against a local API:

```bash
k6 run --summary-trend-stats "min,avg,med,max,p(90),p(95),p(99)" load.js
```

### Load Test Against Deployed API

To test against a deployed API:

```bash
k6 run --summary-trend-stats "min,avg,med,max,p(90),p(95),p(99)" -e API_URL=https://your-api-domain.com load.js
```

### Custom Test Parameters

You can modify test parameters:

```bash
# Run with 20 virtual users instead of default 10
k6 run --summary-trend-stats "min,avg,med,max,p(90),p(95),p(99)" -e API_URL=https://your-api-domain.com -e VUS=20 load.js
```

## Test Scenarios

The load test simulates user traffic with the following characteristics:

1. **Ramp-up period**: 30 seconds to gradually increase from 0 to the target number of virtual users
2. **Sustained load**: 5 minutes of continuous traffic at peak load
3. **Ramp-down period**: 30 seconds to gradually decrease traffic to 0

## Caching Test

The test script includes a cache testing strategy:
- 95% of requests use fixed, predictable text inputs (should be cached)
- 5% of requests use randomized text inputs (should bypass cache)

This design tests both the caching efficiency and the model's performance with varied inputs.

## Performance Requirements

The API should satisfy these performance metrics:

- **Response time**: p99 latency under 2 seconds
- **Error rate**: Less than 1% failed requests
- **Throughput**: Should handle at least 10 requests per second (with 10 concurrent users)
- **Cache efficiency**: At least 95% cache hit rate

## Analyzing Results

After running the tests, k6 will display a summary of performance metrics, including:

- HTTP request duration statistics
- Request rate (throughput)
- Error rate
- Virtual user metrics

Look for the p99 latency metric to ensure it meets the 2-second requirement.

## Visualizing Test Results

For a more detailed analysis, you can output the test results to a format suitable for visualization:

```bash
k6 run --out json=results.json load.js
```

This JSON file can be imported into visualization tools like Grafana for more detailed analysis.