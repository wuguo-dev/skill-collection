---
name: station-device-ui-integration
description: Integrate HTML, JSP, or tablet controls with station backend requests that operate hardware devices. Use when analyzing page interaction logic, comparing a prototype with an integrated page, mapping buttons or forms to SysUrl/SysScript, Nutz @At routes, or /json/devExec, and implementing or reviewing device-command UI calls. Excludes visual-only frontend work.
---

# Station device UI integration

Produce a traceable, safe interaction from each user control to the backend operation that ultimately drives a device. Preserve the page's intended UX while making request contracts, state transitions, and hardware effects explicit.

## Workflow

### 1. Reconstruct the interaction before editing

Read the original page, the current page, shared includes, and request helpers. For every command control, record:

| Control | Validation | Confirmation | Request | Success state | Failure state |
|---|---|---|---|---|---|

Trace event listeners and indirect callbacks, not only inline `onclick` attributes. If both a prototype and an integrated page exist, diff them and separate functional changes from compatibility, styling, and wording changes.

Completion criterion: every device-related button or form has one complete user-action-to-UI-result path, including the no-request path caused by failed validation or cancellation.

### 2. Trace the real backend route

Resolve the deployed URL, including the servlet context such as `/station`. Search for the endpoint in this order:

1. Direct controller annotations and their class-level prefixes.
2. Dynamic URL records such as `SysUrl` and the script named by the record.
3. Generic device invocation endpoints such as `/json/devExec/{device}/{method}`.
4. Reverse proxies or browser-side base URL composition.

Continue through scripts, services, and device methods until the hardware boundary is known. A URL label such as `stopTask` is not proof of electrical emergency-stop behavior.

For this repository's routing and client conventions, read [references/station-routing.md](references/station-routing.md).

Completion criterion: each request maps to a concrete controller, dynamic script, or device method; unresolved hops are named as unknown rather than inferred.

### 3. Freeze the request contract

Before changing JavaScript, write down:

- final URL after context-path expansion;
- HTTP method and content type;
- every parameter name, type, allowed value, and required/default status;
- response shape and the exact success predicate;
- login, cookie, token, role, and origin requirements;
- timeout, retry, duplicate-command, and idempotency behavior;
- whether the operation controls a live, simulated, or staging device.

Prefer evidence from backend code, stored URL/script configuration, or an existing working caller. Treat a blank UI configuration field as unknown: scripts may read `req.getParameter(...)` directly.

Completion criterion: the frontend request can be reproduced from the contract without reading the implementation again.

### 4. Implement the narrowest integration

Preserve the existing DOM, styling, validation, modal flow, focus behavior, and browser compatibility unless the request changes them.

- Reuse the project's request helper when the page already loads it.
- Match the backend's actual encoding. Use form encoding when the server reads servlet request parameters.
- Move the UI to `running`, `returning`, or `stopped` only after backend-confirmed success.
- Represent in-flight state explicitly and prevent accidental duplicate commands according to command semantics.
- Restore controls on success, business failure, network failure, and timeout.
- Surface the backend message when it is safe and useful; otherwise provide an actionable operator message.
- Keep parameter values stable and document numeric codes beside the call site.

For a fixed production command, prefer a narrow allowlisted endpoint or dynamic URL script over exposing arbitrary device method names to the browser.

### 5. Respect the hardware safety boundary

Treat device-changing requests as live operations. Static inspection, diffing, syntax checks, mocks, and staging are the default verification methods. Send a live command only when the user explicitly authorizes that exact operation and the target device/environment is known.

Require confirmation for consequential actions. Distinguish ordinary task cancellation, controlled stop, robot return, and certified emergency stop in both code and labels. Keep credentials and long-lived tokens out of page source. Preserve server-side authorization, validation, state checks, allowlists, and audit logging.

### 6. Verify both code and behavior

Use `scripts/scan_frontend_requests.py` to inventory obvious request call sites when that is faster than manual searching. Its output is a lead list, not proof of runtime behavior.

Verify, as applicable:

- correct context path and final URLs;
- exact parameter keys and values;
- confirmation and cancellation paths;
- server success, business failure, network failure, and timeout;
- rapid repeated taps and concurrent commands;
- UI state only changes after the corresponding result;
- compatibility with the target tablet/WebView;
- no unintended live hardware request occurred during testing.

Compare the final page against the source/prototype and account for every functional difference.

## Handoff

Report:

1. an interaction map from control to hardware effect;
2. the request contract for each endpoint;
3. files and lines changed or reviewed;
4. verification performed and whether it used mocks, staging, or live hardware;
5. unresolved backend or safety assumptions that require the owner to confirm.
