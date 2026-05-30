import subprocess, json
cases = [
  ("git reset --hard", True), ("git reset --hard HEAD~1", True),
  ("git clean -fd", True), ("git checkout -- file.py", True), ("git restore .", True),
  ("git stash drop", True), ("git push --force origin main", True), ("git push -f", True),
  ("git branch -D feature", True), ("git rebase -i HEAD~3", True),
  ("rm -rf /tmp/x", True), ("rm -fr build", True), ("rm -rf ~/something", True), ("rm -r foo/*", True),
  ("bash -c 'rm -rf /x'", True), ("python3 -c \"import os; os.system('rm -rf x')\"", True),
  ("git checkout main", False), ("git checkout -b reconcile/x", False), ("git switch -c foo", False),
  ("git status", False), ("git add -A", False), ("git commit -m 'x'", False),
  ("git push origin feature", False), ("git push --force-with-lease origin feature", False),
  ("ls -la", False), ("python3 -c 'print(1)'", False), ("rm file.txt", False),
  ("grep -r foo .", False), ("uv run pytest", False), ("gh pr merge 3 --squash", False),
]
hook = ".claude/hooks/deny-destructive.js"
fails=0
for cmd, expect in cases:
    inp = json.dumps({"tool_name":"Bash","tool_input":{"command":cmd}})
    r = subprocess.run(["node", hook], input=inp, capture_output=True, text=True)
    blocked = (r.returncode == 2)
    ok = (blocked == expect)
    if not ok: fails+=1
    print(f"{'PASS' if ok else 'FAIL '} block={str(blocked):5} expect={str(expect):5} {cmd}")
print(f"\n{fails} failures / {len(cases)} cases")
