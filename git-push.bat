cd /d "%~dp0"
git add .
set d=%date%
set t=%time:~0,8%
git commit -m "%d%-%t: =0%"
git push origin master -f
pause