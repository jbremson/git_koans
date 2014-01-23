#!python

__author__ = 'joelbremson'
__date__ = "1/13/14"

"""How to write a koan.

1. Start the koan with the @koan decorator. This will print a header for you and keep track of the koan state.
2. Name your koan 'koan_<int>' where <int> is the sequence number of your koan.
3. Do your work in the koan and clean up so that cwd is in the right place when you exit.
4. If the koan is passed return True, otherwise return False.

To start fresh rm the .koan_state file in ./git_koans  .
"""

import os
import pickle
import subprocess
import re
from collections import deque
import distutils.dir_util
import shutil

#Test file for git koans

class State:
    """Set up koan system. Check for prior use so user can continue without
    restart. This will only work if the user hasn't altered the archive state."""

    keep = {'counter':1}
    basedir = os.path.abspath("")
    cwd = basedir


    try:

        target = os.path.abspath(".koans_state")
        f = open(target,"r")
        inval = pickle.load(f)
        keep['counter'] = inval['counter']

    except (AttributeError,IOError):
        # no prior state to return to.
        print "In exception of __init__"

        f = open(target,"w")
        pickle.dump(keep,f)
        f.close()


    @classmethod
    def abs_path(cls,dir=None):
        """Make an absolute dir path through the git_koans home dir to location 'dir' (a relative path).
Returns path string."""
        os.chdir(cls.basedir)
        if dir in [None,'']:
            out = cls.basedir
        else:
            out = os.path.abspath(dir)
        return out

    @classmethod
    def cd(cls,dir=None):
        """Change dir to 'dir', relative to the koans home dir. If dir is left blank
        , cd to git_koans home dir."""
        target = cls.abs_path(dir)
        cls.cwd = target
        os.chdir(target)

    @classmethod
    def inc_counter(cls):
        cls.keep['counter'] += 1
        cls.save_state()

    @classmethod
    def reset_counter(cls):
        cls.keep['counter'] = 1
        cls.save_state()

    @classmethod
    def save_state(cls):
        target = cls.abs_path(".koans_state")
        f = open(target,"w")
        pickle.dump(cls.keep,f)
        f.close()

    @classmethod
    def get_counter(cls):
        """Returns the value of counter."""
        return cls.keep['counter']

    @classmethod
    def load_workset(cls,workset):
        """Creates a git directory for 'workset' and also a 'tmp' directory for inspection."""
        source = cls.abs_path(".sets/" + workset)
        target = cls.abs_path(workset)
        shutil.copytree(source,target)
        State.cd(workset)
        out = cmd("mv .mit .git")
        out = cmd("git init")

        try:
            os.rmdir(cls.abs_path('tmp'))
        except OSError:
            pass
        State.cd()
        out = cmd("mkdir tmp")

    @classmethod
    def delete_workset(cls,workset):
        """Deletes dir for 'workset' (git repo) and the tmp dir."""
        for loc in [workset,'tmp']:
            shutil.rmtree(State.abs_path(loc),ignore_errors=True)








def sys_reset():
    print ("Resetting koans to initial state...")
    # make this safer
    work = State.abs_path("work/")
    cmd("rm -rf " + work)
    State.reset_counter()
    for dir in ["set_a","tmp","work","rollback","clone_work"]:
        try:
            cmd("rm -rf " + State.cd(dir))
        except (OSError,TypeError):
            pass
    # work directory is something to think about
    cmd("mkdir " + work)
    cmd("touch " + State.abs_path("work/.empty"))

def check(loc,setup=[],test_str='', verbose=False):
    """Check a result in location 'loc' (relative to State.basedir). Run shell commands
    in setup array. Check for test string 'test_str'. Returns boolean."""

    last = ""
    retval = False
    State.cd(loc)
    for instruction in setup:
        out = cmd(instruction)
        last = out
        if verbose:
            print instruction
            print out

    match = re.search(test_str,last)
    if not match == None and match.group():
        retval = True
    return retval


def cmd(cmd,verbose=False):
    """Calls subprocess.check_output with 'shell=True' and stderr redirection. Returns
    return val from subprocess. 'verbose' flag is a boolean. Set to true for debugging info. Short cut."""
    proc = subprocess.Popen([cmd],stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True);
    out = ""
    while True:
        line = proc.stdout.readline()
        if verbose:
            print line
        if line != '':
            out += " " + line.rstrip()
        else:
            break
    return out
    #return subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False);

def koan(fxn):
    """Prints koan header and increments state counter (given the koan is passed)."""
    def new_fxn(*args,**kwargs):
        header = kwargs.get('header',True)
        test,answers = test_vals(*args,**kwargs)
        if header:
            print "\n\n********  Koan " + str(State.get_counter()) + "  ********\n\n"
        success = fxn(*args,**kwargs)
        if success: # success
            print "\n\nEnlightenment Achieved!"
            State.inc_counter()
        else: # failed
            print ("\n\nThrough failure learning is achieved. Try it again.\n\n")
            if not test:
                # this runs the caller fxn !!!
                globals()[fxn.__name__](header=False)
        return success
    return new_fxn

def test_vals(*args, **kwargs):
    """Return vals in args and kwargs used for testing. Returns <bool test>,<list answers>."""
    test = 'test' in args
    answers = deque(kwargs.get('answers',[]))
    return test, answers

def git_set_tree(repo):
     #git --git-dir=/Users/joelbremson/code/git_koans/.git --work-tree=./git_koans/ status "
    """Set the working repo to 'repo'. This is assumed to sit in the dir under /git_koans. Always.

This is required because there are a lot of git repos potentially floating about in the workspace."""
    target = State.abs_path(repo)
    out = cmd("git config --git_dir " + target)
    print out


def pause():
    """Prints 'Press 'Enter' when ready' and takes an input. Returns input string."""
    val = raw_input("Press 'Enter' when ready.")
    return val
    

@koan
def koan_1(*args,**kwargs):
    """Init the first repo."""
    retval = False
    test,answers = test_vals(*args,**kwargs)
    State.cd()
    if test:
        cmd_ret = cmd(answers.popleft())
    else:
        dirp = State.abs_path("work")
        out =  raw_input("""
Koan 1: In another shell, init a repository in {0}
Press Enter when done.""".format(dirp))
        print out
        if out == "\t":
            State.cd(dirp)
            out = cmd("git init")
            print out
            State.cd()
        cmd_ret = cmd(out)

    # check to see if there is a .git dir in work...

    if(os.path.isdir(State.abs_path("work/.git"))):
        State.cd("work")
        out = cmd("touch .gitconfig") # make sure git commands run in this dir point to this git repo
        retval = True
        State.cd()
    return retval

@koan
def koan_2(*args,**kwargs):
    """Add a file."""
    test,answers = test_vals(*args,**kwargs)
    ret_val = False
    final =  State.cwd.split("/")[-1]
    if not final == "work":
        State.cd("work")
    if test:
        out = answers.popleft()
        cmd(out)
    else:
        out = raw_input("Koan 2: Now create a file called 'foo' to the work repo. Press Enter when done.")
        if out == "\t":
            State.cd("work")
            out = "touch foo"
        ret = cmd(out)

    State.cd("work")
    if os.path.isfile("foo"):
        if test:
            out = answers.popleft()
        else:
            print """
You have now created what git calls an 'untracked file'. Next we will make it
tracked by officially adding it to the repository.\n\n"""
            out = raw_input("\n\n Add the file to git (hint: git add --help) and press Enter.")
        if out == "\t":
            out = "git add foo"
            print out
        ret = cmd(out)
        git_status = cmd("git status")
        out = re.search("new file:\s+foo",git_status)

        try:
            if out.group():
                ret_val = True
                print """
The file has been added. It is now a 'tracked file.' The add command does
more than just add to the repo though, as we will see later."""
                print "\n\nNext we will learn about basic commits.\n\n"
                State.cd()
        except AttributeError:
            State.cd()
            pass
    return ret_val

@koan
def koan_3(*args,**kwargs):
    """Commit file."""
    test,answers = test_vals(*args,**kwargs)
    State.cd()
    ret_val = False
    State.cd("work")
    if test:
        out = answers.popleft()
    else:
        out = raw_input("Now commit your changes with the 'git commit -m' command.\n "+
"Also, you will need to add a message to your commit. Enter when done.")
        if out == "\t":
            out = "git commit -m 'x'"
            print out
    rv = cmd(out)
    State.cd('')
    shutil.rmtree(State.abs_path('tmp'),ignore_errors=True)
    dirp = State.abs_path("tmp")
    out = cmd("git clone -l work " + dirp)
    State.cd('tmp')
    print "State.cwd = " + State.cwd
    print "getcwd = " + os.getcwd()
    try:
        fd = open('foo','r')
        print  "opened dir"
        ret_val = True
    except IOError, eio:
        print "IO Error " + str(eio)
        pass # file not found.
    #State.delete_workset('tmp')
    State.cd()
    return ret_val

@koan
def koan_4(*args,**kwargs):
    """.gitignore koan."""
    test,answers=test_vals(*args,**kwargs)
    retval = False

    print """\n
This koan is about the '.gitignore' file feature. Sometimes you have files
you don't want git to ever track.\n\n.In your /work repo create a .gitignore
file that does 1) ignores files called 'baz' and 2) ignores any files that
match *.a ."""
    State.cd("work")
    if not test:
        out = raw_input("Press Enter key when you are done.")
        if out == "\t":
            cmd("echo 'baz\n*.a' > .gitignore")

    out = cmd("echo 'text' > baz")
    out = cmd("echo 'text' > dfsdf.a")

    out = cmd("git add baz" )
    match1 = re.search(".*ignored.*baz",out)
    print out


    out = cmd("git add dfsdf.a" )
    match2 = re.search(".*ignored.*dfsdf.a",out)
    print out
    try:
        if match1.group():
            print "\n\nFile 'baz' ignored."
        if match2.group():
            print "File 'dfsdf.a ignored.\n\n"
        retval = True
        print "*** Koan Success! ***\n"
    except AttributeError:
        out = cmd("git status")
        print out
        out = cmd("git reset HEAD baz")
        print out
        out = cmd("git reset HEAD dfsdf.a")
        print out
        out = cmd("git status")
        print out
        pass

    State.cd() # return to base working dir
    return retval

@koan
def koan_5(*args,**kwargs):
    """This koan is a small puzzle in which the user is asked to figure out which file has been
        modified since staging. The answer can be found with 'status'."""

    test,answers = test_vals(*args,**kwargs)
    answers = list(answers)
    workset = "set_a"


    retval = False

    # this koan will work with set_a.zip
    # tasks include
    # file b1 is in the directory but will not commit why? (fix .gitignore
    # remove file d1.o from the directory and make sure that .o files are not committed.
    # finally, resolve a staging issue with a1 */


    # pull the dir from sets/set_a and stage it where the user can access it.

    if test:
        State.delete_workset(workset)


    if not os.path.isdir(State.abs_path(workset)):
        State.load_workset(workset)
    print """
Create files called 'a1','b1', and 'c1' in the /set_a directory. Make sure
that no *.o files are allowed. Watch for a commit problem (hint: observe your
status.)"""


    # wait for user input

    if test:
        State.cd(workset)
        for item in answers:
            print item
            out = cmd(item)
        State.cd()
    else:
        out = raw_input("Press Enter key when you are ready for your work to be checked.")
        if out == "\t": # debugging hack - remove this later
            answers=["echo '*.o' > .gitignore","git add a1 b1 c1 .gitignore","git commit -m 'test commit'"]
            State.cd(workset)
            for item in answers:
                print item
                out = cmd(item)
            State.cd()
        # run code to pass test.

    # test - clone the dir after the user commits. Should find
    # a1, b1, c1 with no d1.o

    #
    State.cd()
    out = cmd("rm -rf " + State.abs_path("tmp"))
    print "rm -rf tmp " + out
    out = cmd("git clone -l "+ workset + " " + State.abs_path("tmp"))
    add_problem = False
    for elem in ['a1','b1','c1']:
        if not os.path.isfile(State.abs_path("tmp/"+elem)):
            print "Problem: file " + elem + " not found."
            add_problem = True

    State.cd("tmp")
    cmd("touch d1.o")
    out = cmd("git add d1.o")
    o_problem = False
    if out == None: # if out is empty than then the add was allowed.
        o_problem = True  # since the add was allowed signal a problem
    else:
        print out + "**\n\n"

    if not o_problem and not add_problem:
        retval=True
    #clean up
    # delete the set_a working directory to clean
    State.cd()

    return retval

@koan
def koan_6(*args,**kwargs):
    retval = False
    print """
In this koan we will work on moving about on the commit path. The 'rollback'
directory has two files and five commits. Using the commands 'log','tags',
and 'checkout' you will need to move the state of the branch to different
points in the commit history."""

    test,answers = test_vals(*args,**kwargs)
    workset = 'rollback'

    if test:
        State.delete_workset(workset)

    if not os.path.isdir(State.abs_path(workset)):
        State.load_workset(workset)

    dirp = State.abs_path("rollback")
    print """
In the other shell go to dir 'rollback' and try the 'git log' command. Notice
the long hash strings in the log. These are the commit identifiers. They name
your commits in git. You can refer to the commits using the first 6 characters
of the hash string. Check it out now. (hint: git log --pretty=oneline)\n\n """

    if not test:
        out = pause()
        print "\n"

    print """

I was working on two songs, one about a girl named mary, called 'mary' and one
about a boat, called 'row'. I stepped away and my cat got on the computer and
made some changes. See if you can get them back to the pre-cat state.

Use the 'checkout' and commit hash identifiers  to modify the repo back to the
pre-cat final commit."""

    if not test:
        out = pause()

    if test or out == "\t":
        State.cd('rollback')
        out = cmd('git checkout 0a1366')
        State.cd()
    # check that mary song has no meows in it.
    State.cd(workset)
    out = cmd("git status")
    print "git status - " + out
    match = re.search("# HEAD detached at 0a1366f",out)
    if not match == None and match.group():
        # next level
        print "Yes! My songs are back. Kitty is foiled again.!\n"
        print "\nNotice that the log only has 3 entries now, not 5."
        out = pause()
        retval = True
        print """
But commit identifier hashes can be hard to remember. We can also use tags. Try
the 'git tag' command. Then move the state to the second commit using the tag
name as the commit identifier.\n """
        if not test:
            out = pause()

        if test or out == "\t":
            out = cmd("git checkout v0.2")
            State.cd()
            State.cd('tmp')
            print "base cwd : " + State.cwd
        out = cmd("git status")
        print out
        match = re.search("# HEAD detached at v0.2",out)
        if not match == None and match.group():
            print "Good. You can use the tag. Now, restore the repo to its final (5th) commit state."
            print "(hint - the last commit is tagged 'master')"
            out = pause()
            if out == "\t" or test:
                State.cd(workset)
                out = cmd('git checkout master')
                State.cd('tmp')

            out = cmd("git log --pretty=oneline | head -1")
            print "git - " + out

            match = re.search("e808d7",out)
            if match.group():
                print "Yes! All is restored. Complete!\n"
                retval = True
            else:
                print "Not quite. Try again."
        else:
            print "Not quite. Try again."
    else:
        #failed to move to right place
        print "The songs are not quite right still. Try again."


    return retval


@koan
def koan_7(*args,**kwargs):
    """git clone, push, pull."""
    test,answers = test_vals(*args,**kwargs)
    State.delete_workset('rollback')
    State.load_workset('rollback')
    retval = False
    print """Core operations: clone, push, pull."""
    print """
Now we will learn the core operations of git: clone, push, and pull. Clone creates
a copy of the latest commited version of the repository. Push pushes your changes
back to the master repository. Pull pulls in changes that have happened in the master
repo.

Start by using clone to make a copy of your the 'rollback' repo. Clone into a new repo
called 'clone_rollback'."""

    State.cd('rollback')
    out = cmd("git checkout HEAD")
    out = cmd("git status")
    print out

    out = pause()
    if test or out == "\t":
        State.cd()
        out = cmd("git clone rollback clone_rollback")

    ok = check('clone_rollback',['git status'],'# On branch master')

    if ok:
        print """
Work repo cloned. Now cd to the clone_work directory and add a new file called
''zipper' (using git add and git commit). """

        out = pause()
        if test or out =="\t":
            State.cd('clone_rollback')
            out = cmd("echo zipper file > zipper")
            out = cmd("git add zipper")
            out = cmd("git commit -m 'Added zipper file.'")


            print """
Now that you've added the 'zipper' file use 'git push' command to push your
change to the master repo in './rollback'. """



    print "Exiting 7"
    return True

if __name__ == "__main__":
    print "Welcome to git-koans...\n"
    print """\n
These koans cover the basic concepts from Pro Git by Scott Chacon
(http://git-scm.com/book). See chapter 2 for assistance.
http://git-scm.com/book/en/Git-Basics ."""


    if State.get_counter()==1 or raw_input("reset?")=="y":
        sys_reset()
    else:
        print "\n\nContinuing from koan " + str(State.get_counter()) + "\n\n"


    # this should store state so user doesn't have to repeat with restart.
    # iterate over koans using the symbol table
    koans = [k for k in dir() if 'koan_' in k]

    for koan in sorted(koans):
        out = re.search("\d+$",koan)
        
        if int(out.group(0)) < State.get_counter():
            continue
        locals()[koan]()


    #git --git-dir=/Users/joelbremson/code/git_koans/.git --work-tree=./git_koans/ status


