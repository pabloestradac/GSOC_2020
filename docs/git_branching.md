## Git Branching Cheat Sheet

This document has basic commands to manage branches on Github. It is based on the site [Git Branching - Branch Management](https://git-scm.com/book/en/v2/Git-Branching-Branch-Management).



1. Create a new branch called `testing`: 

```bash
git branch testing
```

2. Switch to the new `testing` branch:

```bash
git checkout testing
```

3. Create a new branch and switch to it at the same time:

```bash
git checkout -b testing
```

4. Run your tests, make sure the hotfix is what you want, and finally merge the `hotfix` branch back into your `master` branch to deploy to production.

```bash
git checkout master
git merge hotfix
```

5. Synchronize your work with a given remote:

```bash
git fetch <remote>
```

6. See what tracking branches you have set up:

```bash
git fetch --all; git branch -vv
```

7. Delete a branch:

```bash
git branch -d testing
```

8. Take all the changes that were committed on `master` and replay them on `experiment`:

```bash
git checkout experiment
$ git rebase master
```

9. Fetch a branch on someone else's fork on GitHub (from [here](https://stackoverflow.com/questions/9153598/how-do-i-fetch-a-branch-on-someone-elses-fork-on-github/37686809#37686809)).

```bash
git remote add theirusername git@github.com:theirusername/reponame.git
git fetch theirusername
git checkout -b mynamefortheirbranch theirusername/theirbranch
```

