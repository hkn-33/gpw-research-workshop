@echo off
rem Install skills and agents into this project's Claude Code configuration.
cd /d "%~dp0.."
if not exist ".claude\commands" mkdir ".claude\commands"
if not exist ".claude\agents" mkdir ".claude\agents"
copy /Y skills\*.md .claude\commands\ >nul
copy /Y agents\*.md .claude\agents\ >nul
echo Installed skills and agents into .claude\
echo Restart your Claude Code session to pick them up.
