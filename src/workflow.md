# Workflow #

## Summary of Accepted Practices

* A structured brance naming Prod, Staging, fix/xxx, etc has not been adopted for this small project.  Main is the Production branch and fixes are merged directly into it.
* Main branch is protected and is only updated with pull request
* Issues document tasks and are linked to a pull request
* Pull requests must pass a check which runs all tests

## Intro

This document summarizes the findings from researching possible workflows for using Git.  The three git hosting providers, GitHub, BitBucket and GitLab are compared.

There are variances depending on whether the account is a free account or paid and with the free account, features differ depending on the repo being private or public.

## Comparison 
* Pr - private
* Pu - public
* checkmark is implemented
* W - warning only 


|                  | GitHub   | BitBucket | GitLab   |
|------------------|:--------:|:---------:|:-------:|
|                  | PR - PU| PR - PU | PR - PU |
| Protected Branch | W - ✔   | W - ✔  | ✔ - ✔ |
| Issues           | ✔- ✔ | use Jira  | ✔ - ✔ |
| Pull Requests    | ✔ - ✔ | ✔ - ✔ | ✔  - ✔ |
| Status Check     | W - ✔ | W -  ✔ |   ✔ - ✔ |