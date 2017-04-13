# ps2

## Node-utils branch

### If you can read this, this is not a feature branch.

This branch is meant to hold changes that are useful for debugging purposes, not necessarily for release purposes.

To use it:

 1. Start on the branch you're developing.

 2. Run `git checkout node-utils`

 3. Run `git checkout -b <branch-name>`, where `<branch-name>` is replaced by some unused branchname.

 4. Run `git merge <development>`, where `<development>` is replaced by the name of the branch you're working on.

    - If this has many conflicts, it might be worthwhile to try `git rebase <development>`.

 5. Run the tests you need.

I do not recommend adding commits to the `<branch-name>` branch - Rather, you should write the changes you need, then checkout your original branch and commit them there.

If you do need to copy commits from `<branch-name>` back to `<development>`:

 - If you are only copying a single commit:

   1. Record the hash of the commit you are copying

   2. Run `git checkout <development>`, where `<development>` is replaced by the name of the branch you're copying to.

   3. Run `git cherry-pick <hash>`, where `<hash>` is replaced by the hash you recorded in step 1.

 - If you are copying a few commits, it might be feasible to simply cherry-pick them one at a time. In that case:

   1. Record *all* hashes of commits you are copying

   2. Run `git checkout <development>`, where `<development>` is replaced by the name of the branch you're copying to.

   3. For each hash you recorded, starting at the first one which was originally created and ending on the youngest one, run `git cherry-pick <hash>`, replacing `<hash>` with the hash of the current commit

 - If you are copying a range of commits:

   1. Record the hash of the latest commit (that one closest to HEAD) you are copying, as `<tip>`

   2. Record the hash of the ***parent of*** the first commit (the one furthest from head) which you would like to copy, as `<base>`

      - `<base>` will NOT be copied over. Be careful.

   3. Run `git rebase --onto <development> <base> <tip>`, where `<development>`, `<base>`, and `<tip>` are respectively replaced by the name of the branch you're copying to, the hash of the ***parent of*** the first commit you'd like to copy, and the hash of the last commit you'd like to copy.

   4. Confirm that the resulting state is what you want `<development>` to become.

   5. If all is correct, run `git rebase HEAD <development>`, where `<development>` is the name of the branch you're copying to.
