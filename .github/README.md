# GitHub Actions & Dependabot Configuration

This directory contains GitHub Actions workflows and Dependabot configuration for automated dependency management and testing.

## Workflows

### 1. CI (`ci.yml`)
- **Triggers**: Push to main/master, Pull requests
- **Purpose**: Runs comprehensive testing and linting
- **Features**:
  - Tests across multiple Python versions (3.8-3.12)
  - Uses Poetry for dependency management
  - Runs pytest for testing
  - Performs code linting with flake8 and black
  - Caches dependencies for faster builds

### 2. Dependabot Auto-Merge (`dependabot-auto-merge.yml`)
- **Triggers**: Pull requests from Dependabot
- **Purpose**: Automatically merges dependency updates when tests pass
- **Security Features**:
  - Only runs on PRs from `dependabot[bot]`
  - Waits for CI tests to complete successfully
  - Different behavior based on update type:
    - **Patch/Minor updates**: Auto-merge when tests pass
    - **Major updates**: Require manual review (adds comment)
  - Provides clear feedback via PR comments

### 3. Auto Assign (`auto-assign.yml`)
- **Triggers**: New issues and pull requests
- **Purpose**: Automatically assigns issues and PRs to maintainers

### 4. Proof HTML (`proof-html.yml`)
- **Triggers**: Push events and manual dispatch
- **Purpose**: Validates HTML files in the repository

## Dependabot Configuration

The `dependabot.yml` file configures automatic dependency updates for:
- **Python packages** (pip/poetry)
- **GitHub Actions**
- **npm packages** (if present)

### Update Schedule
- **Frequency**: Weekly (Mondays at 9:00 AM)
- **Limits**: 10 open PRs for Python, 5 for others
- **Auto-assignment**: PRs are assigned to `Surfer12`
- **Labels**: Automatically tagged with relevant labels

## Security Considerations

1. **Limited Permissions**: Workflows use minimal required permissions
2. **Bot Verification**: Auto-merge only works for official Dependabot
3. **Test Requirements**: All updates must pass CI before merging
4. **Manual Review**: Major version updates require human approval
5. **Timeout Protection**: CI waits have 30-minute timeouts

## Usage

1. **Automatic**: Dependabot will create PRs weekly
2. **Manual**: You can trigger dependency updates via GitHub UI
3. **Monitoring**: Check the Actions tab for workflow status
4. **Customization**: Modify schedules and limits in `dependabot.yml`

## Troubleshooting

- **Failed Auto-merge**: Check CI logs for test failures
- **Missing Permissions**: Ensure repository settings allow Actions
- **Dependabot Issues**: Check Dependabot tab in repository settings