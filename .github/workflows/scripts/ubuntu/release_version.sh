#!/bin/bash
RELEASE_TYPE=$1
VERSION_OVERRIDE=$2
BETA=$3

LATEST_VERSION=$(gh release list --limit 1 --json tagName | jq -r '.[] | .tagName' | sed 's/^v//')

if [[ -z "$LATEST_VERSION" ]]; then
LATEST_VERSION="0.1.0"
fi

IFS='.' read -r MAJOR MINOR PATCH <<< "$LATEST_VERSION"

case "$RELEASE_TYPE" in
  "Major (x.0.0)")
    MAJOR=$((MAJOR + 1))
    MINOR=0
    PATCH=0
    ;;
  "Minor (0.x.0)")
    MINOR=$((MINOR + 1))
    PATCH=0
    ;;
  "Patch (0.0.x)")
    PATCH=$((PATCH + 1))
    ;;
esac

VERSION="${MAJOR}.${MINOR}.${PATCH}"

if [[ -n "$VERSION_OVERRIDE" ]]; then
LATEST_VERSION="$VERSION_OVERRIDE"
fi

if [[ "$BETA" == "true" ]]; then
  VERSION="${VERSION}b"
fi

echo "release_version=$VERSION" >> $GITHUB_OUTPUT