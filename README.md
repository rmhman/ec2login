# EC2 Login Utility

Interactive AWS EC2 instance selector with SSM Session Manager integration. Quickly browse and connect to running EC2 instances using fzf.

## Features

- 🎯 **Interactive Selection**: Use `fzf` for fast, intuitive instance selection
- 🌍 **Multi-Region Support**: Switch between `use1` (default) and `use2` regions
- 🏷️ **Smart Display**: Shows instance Name tags when available; falls back to Instance-ID for unnamed instances
- 🔐 **Profile Management**: Automatically prompts for AWS profile if `AWS_PROFILE` is not set
- 🔌 **SSM Session Manager**: Direct connection via AWS Session Manager
- ♻️ **Environment Preservation**: Maintains `AWS_PROFILE` environment variable after connection

## Requirements

- **Python**: 3.7+
- **pipx**: Installs Python CLI tools in isolated environments (install via `brew install pipx` on macOS)
- **AWS CLI**: v2 (for SSM Session Manager)
- **fzf**: Fuzzy finder (install via `brew install fzf` on macOS)
- **boto3**: Python AWS SDK
- **AWS Credentials**: Configured in `~/.aws/credentials` and `~/.aws/config`

## Installation

### Quick Install (Recommended)

```bash
pipx install -e /Users/ross/repos/awstools/ec2login
```

This will:

1. Install boto3 dependency automatically in an isolated environment
2. Create an `ec2login` command available in your PATH
3. Link to the source code (changes are reflected immediately)

### Install in Edit/Development Mode

If you want to modify the code and have changes take effect immediately:

```bash
cd /Users/ross/repos/awstools/ec2login
pipx install -e .
```

### Install from PyPI (when published)

```bash
pipx install ec2login
```

## Usage

### Basic Usage (defaults to use1 region)

```bash
ec2login
```

### Switch to use2 Region

```bash
ec2login --region use2
```

### With AWS Profile Pre-Set

```bash
AWS_PROFILE=dev-frontoffice-pu ec2login
```

### Workflow

1. **Run**: Type `ec2login` (or `ec2login --region use2`)
2. **Select Profile** (if not already set): Enter the number of your AWS profile
3. **Wait**: Script fetches running instances
4. **Select Instance**: Use fzf to search and select an instance
   - Type to filter by name or ID
   - Press Enter to connect
   - Press Esc or Ctrl+C to cancel
5. **Connected**: You'll be in an SSM session on the selected instance
6. **Disconnect**: Exit the session with `exit` or Ctrl+D

## Examples

### List Instances in use1 and Connect

```bash
$ ec2login
Using profile: dev-frontoffice-pu
Fetching instances from region use1...
# fzf opens with instances
# Select "web-server-01 | i-061eb3edfc915c5d3"
# Connects to instance
```

### List Instances in use2

```bash
$ ec2login --region use2
Using profile: dev-frontoffice-pu
Fetching instances from region use2...
# fzf opens with instances from use2
```

### With Pre-Set Profile

```bash
$ AWS_PROFILE=production ec2login
Using profile: production
Fetching instances from region use1...
```

## Instance Display Format

Instances are displayed as: `{Display Name} | {Instance-ID}`

- **Named Instances**: Shows the Name tag (e.g., `web-server-01 | i-061eb3edfc915c5d3`)
- **Unnamed Instances**: Shows only Instance-ID (e.g., `i-061eb3edfc915c5d3 | i-061eb3edfc915c5d3`)

## Troubleshooting

### Error: "boto3 is not installed"

```bash
pipx install -e /Users/ross/repos/awstools/ec2login --force
```

### Error: "fzf is not installed"

Install fzf:

- **macOS**: `brew install fzf`
- **Ubuntu/Debian**: `sudo apt-get install fzf`
- **Other**: See [fzf installation guide](https://github.com/junegunn/fzf#installation)

### Error: "AWS CLI is not installed"

Install AWS CLI v2 from: <https://aws.amazon.com/cli/>

### Error: "No running instances found"

- Verify you have running instances in the selected region
- Check your AWS profile credentials: `aws sts get-caller-identity --profile {profile}`

### Error: "Permission denied" connecting to instance

The EC2 instance must have:

- IAM role with SSM Session Manager permissions
- SSM agent running (default on Amazon Linux 2, ECS-optimized AMIs)

## Environment Variables

- `AWS_PROFILE`: Pre-select AWS profile (no prompt if set)
- `AWS_REGION`: Alternative to `--region` flag (flag takes precedence)

## Uninstall

```bash
pipx uninstall ec2login
```

## Contributing

Suggestions and issues welcome!

## License

MIT
