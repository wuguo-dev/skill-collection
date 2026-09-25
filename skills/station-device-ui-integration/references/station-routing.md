# Station routing and request conventions

Read this reference when the target is the `station` Java/Nutz application or uses the same routing conventions.

## Client base path

JSP pages commonly include:

```jsp
<%@include file="../../common/page_head.jsp" %>
```

The include loads shared JavaScript and exposes `${base}`. A call written as:

```javascript
common.ajax("${base}/addTask", data, callback);
```

normally resolves under the deployed context, for example `/station/addTask`. Confirm the actual context instead of hardcoding `/station` when deployments may rename it.

`resources/js/common.js` defines `common.ajax`. Its default behavior is:

- `POST` unless `options.type` overrides it;
- `application/x-www-form-urlencoded` unless `options.contentType` overrides it;
- jQuery serialization for ordinary objects;
- callback arguments `(json, json.data)`;
- normal callback skipped when `json.success === false` unless `callError` is enabled;
- `errorCallback` used for transport errors and, in the current implementation, business failures when supplied.

Read the current helper before relying on these details because shared code can change.

## Route pattern A: dynamic top-level URL

`MainModule` contains a wildcard route equivalent to:

```java
@At("/*")
public void api(HttpServletRequest req, HttpServletResponse resp)
```

The handler:

1. reads `req.getServletPath()`;
2. finds a `SysUrl` whose `url` matches that path;
3. applies the role configured on the `SysUrl` record;
4. executes the named `SysScript` through `SysUtil.scriptByName(...)`;
5. renders according to `SysUrl.type` (`1` is JSON in the current code).

URL-type scripts receive `req`, `resp`, and `url`, so they can read request parameters directly even when the URL administration page's parameter column is blank.

Trace a dynamic endpoint with searches such as:

```text
common.ajax("${base}/<name>"
@At("/*")
class SysUrl
scriptByName
<script function name>
req.getParameter
```

The script body may live in the database rather than the Git worktree. Inspect the URL and script administration records or an approved database snapshot when source search stops at `SysUtil.scriptByName`.

## Route pattern B: direct Nutz controller

Combine class-level and method-level `@At` values, then prefix the servlet context. For example:

```java
@At("/user")
class UserController {
    @At("/doLogin")
    public DataRes login(...) { ... }
}
```

resolves to `/station/user/doLogin` when the context is `/station`.

Check `@Filters`, class/module filters, and parameter-binding rules before treating the route as callable from a tablet.

## Route pattern C: generic device invocation

The compatibility endpoint is:

```text
POST ${base}/json/devExec/{devNo}/{methodName}
```

`devNo` can match a configured device ID or device type. The handler collects servlet request parameters into a map and calls `BaseDevice.invoke(methodName, map)`. Parameter keys must therefore match the Java method parameter names exactly, and values must be castable to those types.

Example:

```java
public void clean(boolean flag)
```

requires a form request equivalent to:

```javascript
common.ajax("${base}/json/devExec/61/clean", { flag: true }, callback);
```

This endpoint is powerful. Use it only where arbitrary device-method exposure is already part of the authorized design; otherwise add a narrow route or dynamic URL script that validates the allowed operation.

## Current inspection-page example

The `njzh/xtIndex.jsp` page demonstrates three dynamic URLs:

| Control | URL | Parameters | UI state after success |
|---|---|---|---|
| Start inspection | `${base}/addTask` | `beamName`, `beamNumber`, `departure` | `running` |
| Stop task | `${base}/stopTask` | none | `stopped` |
| Return home | `${base}/gohome` | none | `returning` |

`departure` currently uses `1` for the vehicle-head origin and `2` for the charging-room origin. Verify these codes against the current backend script before reusing them in another project.

## Safety review points

- Confirm whether a button means task stop, controlled motion stop, protective stop, or certified emergency stop.
- Confirm a command's repeat behavior before enabling retries or allowing rapid taps.
- Confirm the UI state is based on backend acknowledgement rather than only the click event.
- Confirm dynamic URL roles and authentication; CORS alone is not authorization.
- Prefer same-origin deployment for tablet pages so session and context-path behavior stay predictable.
