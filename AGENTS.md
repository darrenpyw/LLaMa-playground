# Agent Instructions

This is the secure source code reviewer project.

## Goal

Orchestrate multi-agent security reviewers for parallel execution.

## Rules

- Prompt user for the directory containing the source code files or filename if analyzing one single file.
- Stop on errors when reading or writing files, state 'Error found when running analysis'

## Agents

- `coordinator`
  Primary coordinator of code review agents.
- `reviewer`
  Code review specialist agent.
