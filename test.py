#!python

import koans
import os
print "Hello Koan Test"
koans.sys_reset()
out = koans.koan_1('test',answers=['git init ./work'])
print out
out = koans.koan_2('test',answers=['touch foo','git add foo --verbose'])

print out
out = koans.koan_3('test',answers=['git status']) # Failure test - wrong answers
out = koans.koan_3('test',answers=['git commit -m "test"'])
print out
koans.State.cd('work')
out = koans.cmd("echo 'baz\n*.a' > .gitignore")
print out
koans.State.cd()
out = koans.koan_4('test',[])
#koan 5 fail test
print "koan 5 fail test is "
out = koans.koan_5('test',answers=["echo '*.o' > .gitignore",'git add c1 ',"git commit -m 'test commit from test.py'"])
print out
# koan 5 success test
print "koan 5 success test is "
out = koans.koan_5('test',answers=["echo '*.o' > .gitignore","git add a1 b1 c1 .gitignore","git commit -m 'test commit'"])
print out
out = koans.koan_6('test',answers=[])
print out
out = koans.koan_7('test',answers=[])
out = koans.koan_8('test',answers=[])
