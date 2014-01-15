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
out = koans.koan_5('test',[])
print out