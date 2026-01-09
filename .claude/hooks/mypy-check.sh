#!/bin/bash

# Read the hook input from stdin
input=$(cat)

# Extract the file_path from tool_input JSON
# For Edit tool: look for "file_path" field
# For Write tool: look for "file_path" field
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null)

# If file_path is empty or null, skip
if [[ -z "$file_path" || "$file_path" == "null" ]]; then
  exit 0
fi

# Check if it's a Python file
if [[ "$file_path" == *.py ]]; then
  echo "🔍 Running mypy on: $file_path"

  # Change to the directory containing the file to use pyproject.toml
  cd "$(dirname "$file_path")" || exit 0

  # Run mypy using uvx
  if uvx mypy "$(basename "$file_path")" 2>&1; then
    echo "✓ Type check passed"
  else
    echo "✗ Type check failed - please review the errors above"
    # Don't exit with error to avoid blocking the edit
  fi
fi

exit 0
