# Git PR Cheat Sheet



1. Add files to staging area

```bash
git add .
```

2. Commit files to local repository

```bash
git commit -m "Commit message"
```

3. Fetch the branches and their respective commits from the upstream repository.

```bash
git fetch upstream
```

4. Check out your fork's local `master` branch.

```bash
git checkout master
```

5. Merge the changes from `upstream/master` into your local `master` branch.

```bash
git merge upstream/master
```

6. Push changes to the repository branch

```bash
git push origin panel
```

7. Go to GitHub and make a pull request