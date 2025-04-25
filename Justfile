mod scanner 'scanner/scanner.just'
mod diagrams 'diagrams/diagrams.just'
mod tests 'tests/tests.just'

# ------------------------------------------------------------------------------
# Prettier
# ------------------------------------------------------------------------------

# Check all files with prettier
prettier-check:
    prettier . --check

# Format all files with prettier
prettier-format:
    prettier . --check --write

# ------------------------------------------------------------------------------
# Justfile
# ------------------------------------------------------------------------------

# Format Justfile
format:
    just --fmt --unstable
    just --fmt --unstable --justfile scanner/scanner.just
    just --fmt --unstable --justfile diagrams/diagrams.just
    just --fmt --unstable --justfile tests/tests.just

# Check Justfile formatting
format-check:
    just --fmt --check --unstable
    just --fmt --check --unstable --justfile scanner/scanner.just
    just --fmt --check --unstable --justfile diagrams/diagrams.just
    just --fmt --check --unstable --justfile tests/tests.just

# ------------------------------------------------------------------------------
# Gitleaks
# ------------------------------------------------------------------------------

# Run gitleaks detection
gitleaks-detect:
    gitleaks detect --source .

# ------------------------------------------------------------------------------
# Lefthook
# ------------------------------------------------------------------------------

# Validate lefthook config
lefthook-validate:
    lefthook validate

# ------------------------------------------------------------------------------
# Zizmor
# ------------------------------------------------------------------------------

# Run zizmor checking
zizmor-check:
    zizmor .

# ------------------------------------------------------------------------------
# Pinact
# ------------------------------------------------------------------------------

# Run pinact
pinact-run:
    pinact run -c .github/other-configurations/pinact.yml

# Run pinact checking
pinact-check:
    pinact run -c .github/other-configurations/pinact.yml --verify --check

# Run pinact update
pinact-update:
    pinact run -c .github/other-configurations/pinact.yml --update

# ------------------------------------------------------------------------------
# Git Hooks
# ------------------------------------------------------------------------------

# Install pre commit hook to run on all commits
install-git-hooks:
    lefthook install -f
