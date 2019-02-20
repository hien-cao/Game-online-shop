# Contribution

**Use Merge Requests!**

If, and only if, you have received verbal approval for a feature from **all other contributors**, you are allowed to skip MR.

## Git guidelines

There are four (4) types of branches to be used in this project.

1. master
2. development
3. feature/[name-of-branch]
4. hotfix/[name-of-branch]

### 1. Branch master

The `master` branch should always be left in a state that it should be ready for production. This branch is the only branch from which deployment to server is made from.

Any non- or partially functioning `features/` should be left out of the `master` branch until they are fully finished.

Only the `development` branch and `hotfix/` type branches are allowed to be merged to `master`.

### 2. Branch development

The `development` branch should always be left in a state that the application can properly start up. Normally all features will be branched from the `development` branch. If you have to branch from `master` do not name the newly made branch with prefix `feature/`, but use `hotfix/` instead.

Merging `development` to `master` is done when all authors of the group unanimously agree that it is a good time to do so.

### 3. & 4. Branches of type /feature and /hotfix

The naming convention used in both `feature/` and `hotfix/` type branches is camel-casing eg. `feature/add-readme-to-project`.

#### 3. feature/

Any branches that is not meant for fixing something that is currently broken should be named `feature/name-of-feature`.

#### 4. hotfix/

Any branches that aim to fix something that is currently broken should be named `hotfix/name-of-broken-feature`.
