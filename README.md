<p align="center">
  <img src="codeantlogo.jpg" alt="CodeAnt Logo" width="300"/>
</p>

# CodeAnt CI Scan Action

A GitHub Action to run CodeAnt CI security and code quality analysis on your repository.

## Features

- 🛡️ Automated security and code quality scanning
- 🔍 Deep code analysis and vulnerability detection
- 📊 Detailed reports and insights
- ⚡ Fast and easy integration

## Usage

### Basic Usage

Add this action to your workflow:

```yaml
name: CodeAnt CI Scan

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  codeant_scan:
    name: Run CodeAnt CI scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Run CodeAnt CI Scan
        uses: CodeAnt-AI/codeant-ci-scan-action@v0.0.1
        with:
          access_token: ${{ secrets.ACCESS_TOKEN_GITHUB }}
```

### Advanced Usage

Customize the scan with additional options:

```yaml
- name: Run CodeAnt CI Scan
  uses: CodeAnt-AI/codeant-ci-scan-action@v0.0.1
  with:
    access_token: ${{ secrets.ACCESS_TOKEN_GITHUB }}
    api_base: 'https://api.codeant.ai'
    include_paths: 'src/,lib/'
    exclude_paths: 'test/,docs/'
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `access_token` | CodeAnt access token (PAT or repository token) | Yes | - |
| `api_base` | CodeAnt API base URL | No | `https://api.codeant.ai` |
| `include_paths` | Comma-separated paths to include in scan | No | `''` (all files) |
| `exclude_paths` | Comma-separated paths to exclude from scan | No | `''` (none) |

## Setup

### 1. Get Your CodeAnt Access Token

1. Sign up or log in to [CodeAnt](https://codeant.ai)
2. Navigate to your account settings
3. Generate a new access token
4. Copy the token

### 2. Add Token to GitHub Secrets

1. Go to your repository's Settings
2. Navigate to Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `ACCESS_TOKEN_GITHUB`
5. Value: Paste your CodeAnt access token
6. Click "Add secret"

### 3. Create Workflow File

Create `.github/workflows/codeant-scan.yml` in your repository with the usage example above.

## Supported Events

This action works with any GitHub event that provides commit information:

- `push`
- `pull_request`
- `workflow_dispatch`
- `schedule`

## Example Workflows

### Scan on Push and Pull Request

```yaml
name: CodeAnt CI Scan

on:
  push:
    branches: [ "main", "develop" ]
  pull_request:
    branches: [ "main" ]

jobs:
  codeant_scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: CodeAnt-AI/codeant-ci-scan-action@v0.0.1
        with:
          access_token: ${{ secrets.ACCESS_TOKEN_GITHUB }}
```

### Scheduled Daily Scan

```yaml
name: Daily CodeAnt Scan

on:
  schedule:
    - cron: '0 2 * * *'  # Run at 2 AM UTC daily

jobs:
  codeant_scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: CodeAnt-AI/codeant-ci-scan-action@v0.0.1
        with:
          access_token: ${{ secrets.ACCESS_TOKEN_GITHUB }}
```

### Scan Specific Directories

```yaml
- uses: CodeAnt-AI/codeant-ci-scan-action@v0.0.1
  with:
    access_token: ${{ secrets.ACCESS_TOKEN_GITHUB }}
    include_paths: 'src/,backend/'
    exclude_paths: 'src/tests/,backend/vendor/'
```

## Troubleshooting

### Authentication Errors

- Ensure your `ACCESS_TOKEN_GITHUB` is correctly set in repository secrets
- Verify the token hasn't expired
- Check that the token has the necessary permissions

### Scan Failures

- Verify your repository is accessible
- Check that the API base URL is correct
- Review the action logs for specific error messages

## Support

- 📧 Email: chinmay@codeant.ai
- 📚 Documentation: [https://docs.codeant.ai](https://docs.codeant.ai)
- 🐛 Issues: [GitHub Issues](https://github.com/CodeAnt-AI/codeant-ci-scan-action/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## About CodeAnt

CodeAnt provides automated code analysis and security scanning to help developers build secure, high-quality software. Visit [codeant.ai](https://codeant.ai) to learn more.
