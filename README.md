# Webots Eel simulation

At this point this is mostly experimental. Needs more experiments and a lot of cleaning up.

## Get started

To resolve libraries in VSCode:
1. In project root `mkdir .vscode`.
1. `touch .vscode/settings.json`.
1. Add this:
  ```json
  {
    "python.autoComplete.extraPaths": ["/usr/local/webots/lib/controller/python"],
    "python.analysis.extraPaths": ["/usr/local/webots/lib/controller/python"],
    "python.analysis.typeCheckingMode": "basic"
  }
  ```

To try things out:
1. Open Webots.
1. Open world: `alen_test_3`.
1. This should get you going.
