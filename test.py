#!python

import main
import os
from koans import *
from koan_support import *

print "Hello Koan Test"
sys_reset()
out = koan_1('test', answers=['git init ./work'])
print out
out = koan_2('test', answers=['touch foo', 'git add foo --verbose'])

print out
out = koan_3('test', answers=['git status'])  # Failure test - wrong answers
out = koan_3('test', answers=['git commit -m "test"'])
print out
State.cd('work')
out = cmd("echo 'baz\n*.a' > .gitignore")
print out
State.cd()
out = koan_4('test', [])
#koan 5 fail test
print "koan 5 fail test is "
out = koan_5('test',
                   answers=["echo '*.o' > .gitignore", 'git add c1 ', "git commit -m 'test commit from test.py'"])
print out
# koan 5 success test
print "koan 5 success test is "
out = koan_5('test',
                   answers=["echo '*.o' > .gitignore", "git add a1 b1 c1 .gitignore", "git commit -m 'test commit'"])
print out
out = koan_6('test', answers=[])
print out
out = koan_7('test', answers=[])
out = koan_8('test', answers=[])
