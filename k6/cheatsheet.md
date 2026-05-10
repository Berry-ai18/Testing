# k6 Cheat Sheet

---

## Basic Script Structure

```javascript
import http from 'k6/http'
import { check, sleep } from 'k6'

export const options = {
    vus: 10,           // number of virtual users
    duration: '30s',   // how long to run
}

export default function () {
    // this runs repeatedly for each virtual user
    const res = http.get('https://example.com')
    check(res, {
        'status is 200': (r) => r.status === 200,
    })
    sleep(1)  // wait 1 second between requests
}
```

---

## HTTP Requests

```javascript
// GET
const res = http.get('https://example.com/api/users')

// POST with JSON body
const res = http.post('https://example.com/api/users',
    JSON.stringify({ name: 'John', age: 30 }),
    { headers: { 'Content-Type': 'application/json' } }
)

// PUT
const res = http.put('https://example.com/api/users/1',
    JSON.stringify({ name: 'John' }),
    { headers: { 'Content-Type': 'application/json' } }
)

// DELETE
const res = http.del('https://example.com/api/users/1')

// With headers
const res = http.get('https://example.com/api/users', {
    headers: { 'Cookie': 'token=abc123' }
})
```

---

## Checks (like assertions)

```javascript
check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
    'body contains bookingid': (r) => r.body.includes('bookingid'),
    'content type is json': (r) => r.headers['Content-Type'].includes('application/json'),
})
```

---

## Options — Test Types

```javascript
// Smoke test — 1 user, quick check everything works
export const options = {
    vus: 1,
    duration: '10s',
}

// Load test — normal expected traffic
export const options = {
    vus: 50,
    duration: '1m',
}

// Stress test — find the breaking point
export const options = {
    stages: [
        { duration: '30s', target: 50 },    // ramp up to 50 users
        { duration: '1m', target: 100 },    // ramp up to 100 users
        { duration: '30s', target: 0 },     // ramp down
    ],
}

// Spike test — sudden burst
export const options = {
    stages: [
        { duration: '10s', target: 100 },   // sudden spike
        { duration: '1m', target: 100 },    // stay at 100
        { duration: '10s', target: 0 },     // drop
    ],
}
```

---

## Thresholds (fail the test if these are not met)

```javascript
export const options = {
    vus: 50,
    duration: '1m',
    thresholds: {
        http_req_duration: ['p95<500'],     // 95% of requests under 500ms
        http_req_failed: ['rate<0.01'],     // less than 1% failure rate
        checks: ['rate>0.99'],              // more than 99% checks pass
    },
}
```

---

## Key Metrics to Know

| Metric | What it means |
|--------|--------------|
| `http_req_duration` | How long requests take |
| `http_req_failed` | % of failed requests |
| `http_reqs` | Total number of requests |
| `vus` | Current number of virtual users |
| `p95` | 95% of requests completed within this time |
| `p99` | 99% of requests completed within this time |

---

## Commands

```bash
k6 run load_test.js                        # run the test
k6 run --vus 10 --duration 30s script.js   # override options from CLI
k6 run --out json=results.json script.js   # save results to file
```

---

## Smoke vs Load vs Stress vs Spike

| Type | VUs | Purpose |
|------|-----|---------|
| Smoke | 1 | Verify script works, no errors |
| Load | Normal expected | Check performance under normal traffic |
| Stress | Above normal | Find breaking point |
| Spike | Sudden burst | Check behaviour under sudden traffic surge |
