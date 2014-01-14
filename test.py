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
os.chdir(koans.State.workdir)
out = koans.cmd("echo 'baz\n*.a' > .gitignore")
print out
os.chdir("..")
out = koans.koan_4('test',[])
print out