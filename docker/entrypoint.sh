#!/bin/bash
set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "Checking required environment variables..."

# List of required environment variables
required_vars=(
    "APP_AUTH__RW_X_API_KEY"
    "APP_AUTH__RO_X_API_KEY"
    "APP_DB__HOST"
    "APP_DB__PORT"
    "APP_DB__DATABASE"
    "APP_DB__USER"
    "APP_DB__PASSWORD"
)

missing_vars=()

# Check each required variable
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
        echo -e "${RED}✗${NC} $var is not set"
    else
        echo -e "${GREEN}✓${NC} $var is set"
    fi
done

# Exit if any variables are missing
if [ ${#missing_vars[@]} -ne 0 ]; then
    echo ""
    echo -e "${RED}Error: Missing required environment variables:${NC}"
    for var in "${missing_vars[@]}"; do
        echo "  - $var"
    done
    exit 1
fi

echo -e "${GREEN}All required environment variables are set!${NC}"
echo "Starting application..."

# Execute the main command
exec "$@"
