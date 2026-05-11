# Testing Portfolio

A collection of test automation projects built while learning QA engineering.

---

## Projects

### restful-booker — API Testing with pytest

REST API test suite against the [Restful-Booker](https://restful-booker.herokuapp.com) booking API.
Covers full CRUD, auth token handling, negative tests, schema validation with jsonschema.
Tests run automatically on every push via GitHub Actions with an HTML report generated on each run.

**Tech:** Python · pytest · requests · jsonschema · pytest-html · GitHub Actions

---

### playwright — UI End-to-End Testing

UI test suite against [Saucedemo](https://www.saucedemo.com) built with Playwright.
Covers login flows, inventory validation, cart management and full checkout flow across Chrome, Firefox and Safari.
Organised using Page Object Model for maintainability.

**Tech:** Playwright · JavaScript · GitHub Actions

---

### k6 — Performance Testing
Load and performance test suite against the Restful-Booker API.
Covers smoke, load and stress testing scenarios with thresholds.

**Tech:** k6 · JavaScript

*In progress*

---

