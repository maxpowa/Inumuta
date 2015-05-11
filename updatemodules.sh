git remote add inumuta-modules https://github.com/maxpowa/inumuta-modules.git
git fetch inumuta-modules master
git subtree pull --prefix willie/modules inumuta-modules master --squash
