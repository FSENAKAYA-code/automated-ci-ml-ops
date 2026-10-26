# Domain implementation notes

GitHub Actions runs tests, lint, a synthetic train/validation/test job, and uploads a JSON metrics artifact. Docker packages the local workflow. The publish helper requires a clean tree and an explicit confirmation flag; CI never pushes automatically.
