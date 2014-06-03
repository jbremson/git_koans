#python 2.6 / 2.7

__author__ = 'joelbremson'
__date__ = "1/23/14"

import getopt
import sys
import koans
from koan_support import State
import re

#Main file for git koans


def usage():
    print """

Command line arguments:

-h          print help message
-r          reset system
-k <number> jump to koan <number>
"""


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hrk:d", ["reset", "koan="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    counter = 1
    for opt, arg in opts:
        if opt in ("-h,--help"):
            usage()
            sys.exit(0)
        if opt in ("-r, --reset"):
            print "Resetting System..."
            sys_reset()
        if opt in ("-k,--koan"):
            counter = arg
            print "Starting at koan " + str(arg)

    State.set_counter(counter)
    print "Welcome to git-koans...\n"
    print """\n

Presented here are koans, or puzzles, to assist in the learning of git.

To run these you will need python and git installed.

Run the koans in this shell and do the exercises in another shell.

These koans cover basic concepts from Pro Git by Scott Chacon
(http://git-scm.com/book). See chapter 2 for assistance.
http://git-scm.com/book/en/Git-Basics .
"""

    instr = """
Some usage instructions

1. A task can be skipped by entering a tab at the prompt (debug feature).
2. The system should remember which koan you left off on (although not
   where you left off mid-koan.).
"""

    # this should store state so user doesn't have to repeat with restart.
    # iterate over koans using the symbol table
    problems = [k for k in dir(locals()['koans']) if k.startswith("koan_")]
    for problem in sorted(problems):
        out = re.search("\d(_\d)?$", problem)

        if float(out.group(0).replace("_", ".")) < State.get_counter():
            continue
        getattr(sys.modules['koans'], problem)()


