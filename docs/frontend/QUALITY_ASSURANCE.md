# Frontend Quality Assurance

## Verification completed for Phase 5.4

| Check | Result |
| --- | --- |
| Node built-in frontend tests | Passed: 10 tests covering routes, shell landmarks, prediction presentation, and analytics evidence/chart contracts. |
| JavaScript syntax check | Passed for every module under `frontend/src/js`. |
| Diff whitespace check | Passed with `git diff --check`. |
| Browser console | No warning/error entries in the local static-preview review. |
| Route/viewport matrix | Passed: 45 route/viewport checks across mobile, tablet, laptop, desktop, and ultra-wide sizes with no unintended page-level horizontal overflow. |
| Interaction review | Passed: mobile menu open/close state, invalid/valid form feedback, chart metric selection, and dashboard unavailable-service recovery. |

## Reproduce locally

```powershell
& 'C:\Program Files\nodejs\node.exe' --test frontend/tests/*.test.js

$nodePath = 'C:\Program Files\nodejs\node.exe'
Get-ChildItem frontend/src/js -Recurse -Filter *.js | ForEach-Object {
  & $nodePath --check $_.FullName
}

git diff --check
```

Use a local static server for the browser review. Validate the browser's DOM/console and test the documented viewport matrix; do not submit real or sensitive article text during local QA.

## Release gate

Before a public deployment, repeat the browser matrix against the built, HTTPS-served artifact; run a production accessibility scan; test the deployed API error paths; and document any browser-specific limitations. These checks validate frontend quality only. They do not approve the underlying research model for production use.
