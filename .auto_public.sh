git checkout master &&
git pull &&
git checkout no_pdf_included && 
git merge master -m "new functions and fixes" && 
git pull &&
git push &&
git add . &&
git commit -m "new functions and fixes" -a && 
git push && 
git fetch &&
git checkout master && 
git merge no_pdf_included --no-commit --no-ff  no_pdf_included -m "new functions and fixes" && 
git pull &&
git push &&
git fetch &&
git checkout master 