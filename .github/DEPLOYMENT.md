# CI/CD Deployment Guide

This repository is configured with a comprehensive CI/CD pipeline using GitHub Actions.

## Quick Setup

### 1. Enable Branch Protection
Go to **Settings > Branches** and add rules for `main`:
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Include administrators

### 2. Enable Security Features
Go to **Settings > Code security and analysis**:
- Dependency graph
- Dependabot alerts
- Dependabot security updates
- Code scanning (CodeQL)
- Secret scanning

### 3. Configure PyPI Publishing
Go to **Settings > Environments** and create a `pypi` environment:
- Add a trusted publisher on PyPI for this repository
- The release workflow uses OIDC token authentication (no API key needed)

## Workflows Overview

| Workflow | Triggers | Purpose |
|----------|----------|---------|
| **CI** | Push/PR to `main`/`develop` | Code quality, build verification, security |
| **Release** | Git tags (`v*`) | Build, create GitHub release, publish to PyPI |
| **CodeQL** | Push/PR + weekly | Advanced security scanning |
| **Dependabot** | Weekly | Automated dependency updates |

## CI Pipeline

### On Pull Request / Push
1. **Code Quality**: ruff linting and format checking
2. **Build**: Package build, verification, and installation test
3. **Security**: Bandit code security scanning

## Creating a Release

1. Update version in `pyproject.toml`
2. Commit and push changes
3. Create and push a tag:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```
4. GitHub Actions will automatically:
   - Build the package
   - Create a GitHub release with installation instructions
   - Publish to PyPI

## Local Testing

Simulate CI checks locally:
```bash
# Install dev dependencies
uv sync --dev

# Code quality
uv run ruff check src/
uv run ruff format --check src/

# Build
uv build

# Test the server starts
uv run robot-mcp --help
```

## Troubleshooting

### Release Creation Fails
1. Ensure version number in `pyproject.toml` is incremented
2. Check that the git tag follows the `v*` pattern (e.g., v0.1.0)
3. Verify package builds successfully locally with `uv build`

### Code Quality Failures
Run locally to reproduce and fix:
```bash
uv run ruff check src/    # Show linting issues
uv run ruff format src/   # Auto-format code
```
