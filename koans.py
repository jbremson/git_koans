from koan_support import *


"""How to write a koan.

1.  Start the koan with the @koan decorator. This will print a header for you
    and keep track of the koan state.
2.  Name your koan 'koan_<int>_<opt>' where <int> is the sequence number of
    your koan and <opt> is an optional secondary identifier. For example,
    koan_3, koan_3_1, koan_3_3, will appear in the order implied by 3, 3.1, 3.3.
3.  Do your work in the koan and clean up so that cwd is in the right place
    when you exit.
4.  If the koan is passed return True, otherwise return False.

To start fresh rm the .koan_state file in ./git_koans.
"""


@koan
def koan_1(*args, **kwargs):
    """Init the first repo."""
    retval = False
    test, answers = test_vals(*args, **kwargs)
    State.cd()
    if test:
        cmd_ret = cmd(answers.popleft())
    else:
        dirp = State.abs_path("work")
        out = raw_input("""
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

    if (os.path.isdir(State.abs_path("work/.git"))):
        State.cd("work")
        out = cmd("touch .gitconfig")  # make sure git commands run in this dir point to this git repo
        retval = True
        State.cd()
    return retval


@koan
def koan_2(*args, **kwargs):
    """Add a file."""
    test, answers = test_vals(*args, **kwargs)
    ret_val = False
    final = State.cwd.split(os.sep)[-1]
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
        ret = cmd(out)
        git_status = cmd("git status")
        out = re.search("new file:\s+foo", git_status)

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
def koan_3(*args, **kwargs):
    """Commit file."""
    test, answers = test_vals(*args, **kwargs)
    State.cd()
    ret_val = False
    State.cd("work")
    if test:
        out = answers.popleft()
    else:
        out = raw_input("Now commit your changes with the 'git commit -m' command.\n " +
                        "Also, you will need to add a message to your commit. Enter when done.")
        if out == "\t":
            out = "git commit -m 'x'"
    rv = cmd(out)
    State.cd('')
    shutil.rmtree(State.abs_path('tmp'), ignore_errors=True)
    dirp = State.abs_path("tmp")
    out = cmd("git clone -l work " + dirp)
    State.cd('tmp')
    try:
        fd = open('foo', 'r')
        ret_val = True
    except IOError, eio:
        print "IO Error " + str(eio)
        pass  # file not found.
    #State.delete_workset('tmp')
    State.cd()
    return ret_val


@koan
def koan_4(*args, **kwargs):
    """.gitignore koan."""
    test, answers = test_vals(*args, **kwargs)
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

    out = cmd("git add baz")
    match1 = re.search(".*ignored.*baz", out)

    out = cmd("git add dfsdf.a")
    match2 = re.search(".*ignored.*dfsdf.a", out)
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

    State.cd()  # return to base working dir
    return retval


@koan
def koan_4_9(*args, **kwargs):
    """This koan is about using the git config features. Set name, email, aliases, ???"""

    test, answers = test_vals(*args, **kwargs)
    retval = False
    workset = "rollback"
    State.load_workset(workset)

    print """
Git is managed with the 'config' command. Your git installation should have
your name and email address already set. Let's check now.

To check your name setting (in another shell):

git config --get user.name

"""
    if not test:
        out = pause()
    print """

To change or add your name:

git config --global --add user.name 'Your Name'

"""
    if not test:
        out = pause()
    print """
There are three layers to the git config system: system, global, and local.
The system layer applies to all users. It is usually managed by a system admin-
-istrator. Leave it alone unless you know what you're doing.Git will, by de-
-fault, choose the value for a configuration variable first in local, next in
global, and finally in system. This allows a great degree of flexibility in
how the system is configured.

We will now go through a demonstration of how these layers work.

Type the following lines:
git config --local -add user.name "local user level"
git config --global -add user.name "system user level"
"""
    if not test:
        out = pause()
    print """
Now let's access the values.

Try:

git config --get user.name
git config --local --get user.name

    """
    if not test:
        out = pause()
    print """

Notice that your default user.name with --get is "local user level,"
and that you can also specify that you want the local value.

You can see this value written in the file .git/config .

Now we will unset the local user.name:

git config --local --unset user.name
"""

    if not test:
        out = pause()
    print """"

Next try,
git config --get user.name
git config --global user.name

Notice that they are the same.

The global config variables are written to the ~/.gitconfig file."""

    if not test:
        out = pause()
    print """
That's all.
"""
    retval = True
    return retval


@koan
def koan_5(*args, **kwargs):
    """This koan is a small puzzle in which the user is asked to figure out
    which file has been modified since staging. The answer can be found with 'status'."""

    test, answers = test_vals(*args, **kwargs)
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
        State.load_workset(workset, live_git=True)
    print """

There are some files that you do not want git to track, object files for
example. The '.gitignore' file tells git which files to ignore.

Here you will edit the .gitignore file to the meet the koan objectives.
There are two objectives:

1) Accept files with names that do not end with '.o'.
2) Reject files with names that end with '.o'.

Begin with the first objective by adding and committing the files 'a1','b1' and 'c1'
to the repo. Use the 'set_a' directory. Don't force any commits.

Try it first without editing the .gitignore file.
"""

    if not test:
        out = pause()
    print """
The file 'b1' should have been rejected. Now edit the .gitignore file and
remove the line with b1 on it. You can verify it by trying to checkout
the file with 'git checkout b1'.

Hint: Don't forget to add b1.
"""
    if not test:
        out = pause()
    print """
Now add an entry to ignore files with names ending with .o. (hint: *.o).

"""
    # wait for user input

    if test:
        State.cd(workset)
        for item in answers:
            print item
            out = cmd(item)
        State.cd()
    else:
        out = pause()
        if out == "\t":  # debugging hack - remove this later
            answers = ["echo '*.o' > .gitignore", "git add a1 b1 c1 .gitignore", "git commit -m 'test commit'"]
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
    out = cmd("git clone -l " + workset + " " + State.abs_path("tmp"))
    add_problem = False
    for elem in ['a1', 'b1', 'c1']:
        if not os.path.isfile(State.abs_path("tmp/" + elem)):
            print "Problem: file " + elem + " not found."
            add_problem = True

    State.cd("tmp")
    cmd("touch d1.o")
    out = cmd("git add d1.o")
    o_problem = False
    if out == None:  # if out is empty than then the add was allowed.
        o_problem = True  # since the add was allowed signal a problem
    else:
        print out + "**\n\n"

    if not o_problem and not add_problem:
        retval = True
    #clean up
    # delete the set_a working directory to clean
    State.cd()

    return retval


@koan
def koan_6(*args, **kwargs):
    retval = False
    print """
In this koan we will work on moving about on the commit path. The 'rollback'
directory has two files and five commits. Using the commands 'log','tags',
and 'checkout' you will need to move the state of the branch to different
points in the commit history."""

    test, answers = test_vals(*args, **kwargs)
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
    match = re.search("# HEAD detached at 0a1366f", out)
    if not match == None and match.group():
        # next level
        print "Yes! My songs are back. Kitty is foiled again.!\n"
        print "\nNotice that the log only has 3 entries now, not 5."
        if not test:
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
        match = re.search("# HEAD detached at v0.2", out)
        if not match == None and match.group():
            print "Good. You can use the tag. Now, restore the repo to its final (5th) commit state."
            print "(hint - the last commit is tagged 'master')"
            if not test:
                out = pause()
            if out == "\t" or test:
                State.cd(workset)
                out = cmd('git checkout master')
                State.cd('tmp')

            out = cmd("git log --pretty=oneline | head -1")
            print "git - " + out

            match = re.search("e808d7", out)
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
def koan_7(*args, **kwargs):
    """git clone, push, pull."""
    test, answers = test_vals(*args, **kwargs)
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
    out = cmd("git checkout head")
    out = cmd("git status")
    print out

    if not test:
        out = pause()
    if test or out == "\t":
        State.cd()
        out = cmd("git clone rollback clone_rollback")

    ok = check('clone_rollback', ['git status'], '# On branch master')

    if ok:
        print """
Work repo cloned. Now cd to the clone_work directory and add a new file called
''zipper' (using git add and git commit). """

        if not test:
            out = pause()
        if test or out == "\t":
            State.cd('clone_rollback')
            out = cmd("echo zipper file > zipper")
            out = cmd("git add zipper")
            out = cmd("git commit -m 'Added zipper file.'")

        ok = check('clone_rollback', ['git checkout zipper'], '', verbose=True)

        print """
Good. Now that you've added the 'zipper' file use 'git push' command to push your
change to the master repo in './rollback'. """

        State.cd("rollback")
        out = cmd("git checkout head")

        if not test:
            out = pause()
        if test or out == "\t":
            State.cd("clone_rollback")
            out = cmd("git push")

        ok = check('rollback', ['git checkout master', 'git checkout zipper'], '', True)

        if not test:
            out = pause()

    print """

Koan complete!

Now you have seen the clone, push, pull workflow for git. This is a git approach
you might use for working on your own repo, say on github. In more complex git
workflows with multiple developers and branches you will probably use a differ-
ent sort of workflow. We will cover that later."""

    return True


@koan
def koan_8(*args, **kwargs):
    """Merge mac, linux, and windows branches together into a single master."""

    # 1/26/ the k8 repo is a mess. Need to simplify it and make it work right.
    sys_reset()
    workset = 'k8'
    test, answers = test_vals(*args, **kwargs)

    State.load_workset(workset, live_git=True)
    State.cd(workset)

    out = cmd("git checkout -b master remotes/origin/master")
    print """
In git, when you want to start on a new code fork, while leaving the other
changes intact, you create a branch. After you are happy with your changes
you may bring the branched code back into the master repo line.

This koan is a repo that has already been branched and must have its changes
integrated.

The workset is in the k8 directory. Open that in another shell now.
"""
    if not test:
        out = pause()

    print """
Now, cd into the k8 dir and inspect the repo. Try three commands:

git branch -a (show all branches in the repo)
git branch ( show checked out branches  and active branch (*)
gitk       (gitk is visual tool for inspecting a repo).

"""
    if not test:
        out = pause()
    print """
You should be on the master branch ('git branch' to check). You  should see
two files: code and README.

Read the branch log ('git log') and check its status ('git status').

Now checkout the 'fixup' branch with 'git checkout fixup'.

Inspect the directory. The README file is not part of the fixup branch. It
should be gone.

Read the branch log ('git log') and check its status ('git status'). Note that
it is different than for the master branch.

"""

    if not test:
        out = pause()
    print """
Make a change to the 'code' file (doesn't matter what it is). Stage the changes
with 'git add' and commit them with 'git commit'.
"""

    if not test:
        out = pause()
    print """
Now switch back to the master branch ('git checkout ...') . Inspect the 'code'
file one last time to verify that it is different than the one in the 'fixup'
branch.
"""

    if not test:
        out = pause()
    print """
Now we are going to use the 'rebase' command to integrate the fixup changes
into master. The command to use is: git rebase fixup.

Depending on what changes you made to the files git will either do a simple
'fast forward' merge, which means that master had not changed since the
fixup branch was made, or it will ask you to merge the files. To do this
you will have to open 'code' in and edit the changes (get rid of the git
insertions e.g. >>>>>>, in the process), and then do 'git rebase --continue'.

"""
    if not test:
        out = pause()
    print """
Now let's get rid of the local fixup branch because we don't need it
anymore. Use 'git branch -D fixup', which tells git to delete the branch."""

    if not test:
        out = pause()
    print """
Another thing the rebase command is good for is fixing up the commit log.

Frequent commits are a good thing in local repos, but checking in a bunch
of tiny commits into the a master branch is generally not a good idea.

Git allows you to edit your commit record with 'git rebase -i <commit hash>'.

Now, using the log (git log) choose the commit 4 steps back from the final
one ('git rebase -i a32df3' for example). You will then be met with a dialog
asking you to edit the commit record. Leave the first line as 'pick' and
change the others to 'squash'.

You will now have a chance to reword the commit log for your edited commit.

"""

    if not test:
        out = pause()
    print """

Now check the log again. You should see the changes you made reflected in the
log. That's it!
"""
    return True


def test_fxn():
    print "Test function ran: success!!!"
