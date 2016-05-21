#!/bin/bash
# This file may not be moved as it uses relative paths!
#
# Purpose:
#   Set environment variables for cloud-base analysis.
#
# Usage:
#   $ source config.sh

# Include clb package to PYTHONPATH.
SCRIPTS_PATH="$(readlink -f .)"
export PYTHONPATH="${SCRIPTS_PATH}:${PYTHONPATH}"
