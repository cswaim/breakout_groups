# Workflow #

## Summary of Proposed Practices

* A structured branch naming Prod, Staging, fix/xxx, etc has not been adopted for this small project.  Use your own names or create from issue->pull request.
* Main is the Production branch and fixes are merged directly into it.
* Main branch is protected and is only updated with pull request
* Checks are only run on merge to main
* Do we want code reviews before merge?
* Issues document tasks and are linked to a pull request
* Pull requests must pass a check which runs all tests - automatically run when accessing a pull request
* The pull request will automatically close the issue
* the pull request will delete the source branch

## Intro

This document summarizes the findings from researching possible workflows for using Git.  The three git hosting providers, GitHub, BitBucket and GitLab are compared.
(see comparison section below)

There are variances depending on whether the account is a free account or paid and with the free account, features differ depending on the repo being private or public.

## GitHub Process

    1. Open an issue which describes the task to be done. This is a good way to track pending tasks.
    
    2. Create a pull request and test branch.  Link the issue if it exists.  See the Development sidebar section of the issue or pull request.
    
    3. On local computer, git pull will copy down the new branch.  Checkout the branch and make the changes.
    
    4. Commit and push the change to the Github repo
    
    5. The pull request should be set to close the issue and delete the source branch 
    
    6.  Wait for code reviews?  Last reviewer merges the pull request. 
    
    7. If the check passes - which is a run of all the pytest jobs - then squash merge the pull request. The squash merge ignores all the commit history in the source branch and just adds a single commit to the main history.


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

### Misc

#### GitLab

    - merges request instead of pull request
    - the ci/cd scripts are not as easy to use as github
    - navigation within repo is not as intuitive as gh or bb

#### Bitbucket

    - the Jira issues software will not let an existing branch be linked to a pull/issue - must create the branch with issue/pull request
    - uses bug/... fix/... naming of branches
    - Private libraries recieve warnings on checks, so invalid merges to main are allowed


#### Github

    - Private libraries recieve warnings on checks, so invalid merges to main are allowed