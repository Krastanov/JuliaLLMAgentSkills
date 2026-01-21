#!/usr/bin/env bash
set -euo pipefail

# Build Julia package documentation
#
# Usage:
#   ./build-docs.sh [--serve] [--draft]
#
# Options:
#   --serve   Start a local server after building (requires LiveServer.jl)
#   --draft   Build in draft mode (faster, skips @example blocks)

SERVE=false
DRAFT=false

for arg in "$@"; do
    case $arg in
        --serve)
            SERVE=true
            shift
            ;;
        --draft)
            DRAFT=true
            shift
            ;;
        *)
            echo "Unknown option: $arg"
            echo "Usage: ./build-docs.sh [--serve] [--draft]"
            exit 1
            ;;
    esac
done

echo "Installing documentation dependencies..."
julia --project=docs -e '
    using Pkg
    Pkg.develop(PackageSpec(path=pwd()))
    Pkg.instantiate()'

if [ "$DRAFT" = true ]; then
    echo "Building documentation (draft mode)..."
    julia --project=docs -e '
        ENV["DOCUMENTER_DRAFT"] = "true"
        include("docs/make.jl")'
else
    echo "Building documentation..."
    julia --project=docs docs/make.jl
fi

echo "Documentation built successfully in docs/build/"

if [ "$SERVE" = true ]; then
    echo "Starting local server..."
    julia --project=docs -e '
        using Pkg
        if !haskey(Pkg.project().dependencies, "LiveServer")
            Pkg.add("LiveServer")
        end
        using LiveServer
        serve(dir="docs/build")'
else
    # Try to open in browser
    if command -v xdg-open &> /dev/null; then
        xdg-open docs/build/index.html 2>/dev/null || echo "Open docs/build/index.html in your browser"
    elif command -v open &> /dev/null; then
        open docs/build/index.html 2>/dev/null || echo "Open docs/build/index.html in your browser"
    else
        echo "Open docs/build/index.html in your browser"
    fi
fi
