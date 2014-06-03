import os
import pickle
import shutil
import subprocess
import sys
from collections import deque
import re


class State:
    """Set up koan system. Check for prior use so user can continue without
    restart. This will only work if the user hasn't altered the archive state."""

    keep = {'counter': 1}
    basedir = os.path.abspath("")
    cwd = basedir

    try:

        target = os.path.abspath(".koans_state")
        f = open(target, "r")
        inval = pickle.load(f)
        keep['counter'] = inval['counter']

    except (AttributeError, IOError):
        # no prior state to return to.
        print "In exception of __init__"

        f = open(target, "w")
        pickle.dump(keep, f)
        f.close()


    @classmethod
    def abs_path(cls, dir=None):
        """Make an absolute dir path through the git_koans home dir to location 'dir' (a relative path).
Returns path string."""
        os.chdir(cls.basedir)
        if dir in [None, '']:
            out = cls.basedir
        else:
            out = os.path.abspath(dir)
        return out

    @classmethod
    def cd(cls, dir=None):
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
    def reset_counter(cls, inp=1):
        cls.keep['counter'] = inp
        cls.save_state()

    @classmethod
    def set_counter(cls, inp):
        """Set counter to int value arg."""
        cls.reset_counter(int(inp))


    @classmethod
    def save_state(cls):
        target = cls.abs_path(".koans_state")
        f = open(target, "w")
        pickle.dump(cls.keep, f)
        f.close()

    @classmethod
    def get_counter(cls):
        """Returns the value of counter."""
        return cls.keep['counter']

    @classmethod
    def load_workset(cls, workset, live_git=False):
        """Creates a git directory for 'workset' and also a 'tmp' directory for inspection.
    If live_git is True then an actual working .git is installed in the .sets/<workset> dir."""
        if live_git:
            # make this a live git dir with a .git init.
            # then clone it target dir rather than copy and init.

            dirp = os.path.join(".sets", workset)
            abs = os.path.abspath(dirp)
            os.chdir(abs)
            gitdir = os.path.join(abs, ".git")
            mitdir = os.path.join(abs, ".mit")
            shutil.rmtree(gitdir, ignore_errors=True)
            shutil.copytree(mitdir, gitdir)
            shutil.rmtree(State.abs_path(workset), ignore_errors=True)
            State.cd()

            out = cmd("git clone {0} {1}".format(os.path.join(".", ".sets", workset), workset))

        else:
            source = cls.abs_path(os.path.join(".sets", workset))
            target = cls.abs_path(workset)
            shutil.copytree(source, target)
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
    def delete_workset(cls, workset):
        """Deletes dir for 'workset' (git repo) and the tmp dir."""
        for loc in [workset, 'tmp']:
            try:
                shutil.rmtree(State.abs_path(loc))
            except OSError, e:
                pass


def sys_reset():
    print ("Resetting koans to initial state...")
    # make this safer
    State.reset_counter()
    # this should just kill all the worksets by looking in the .sets dir
    for dir in ["set_a", "tmp", "work", "k8_repo", "rollback", "clone_work", "clone_rollback", "k8"]:
        try:
            State.delete_workset(dir)
        except (OSError, TypeError) as e:
            print "Did not rm -rf {0}".format(dir)
            print "Exception msg: {0}".format(str(e))
            pass
    # work directory is something to think about
    State.cd("")
    cmd("mkdir work")
    cmd("touch " + State.abs_path("work/.empty"))


def check(loc, setup=[], test_str='', verbose=False):
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

    match = re.search(test_str, last)
    if not match == None and match.group():
        retval = True
    if test_str == '' and last == '':  # empty string is desired result case
        retval = True
    return retval


def cmd(cmd, verbose=False):
    """Calls subprocess.check_output with 'shell=True' and stderr redirection. Returns
    return val from subprocess. 'verbose' flag is a boolean. Set to true for debugging info. Short cut."""
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True);
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
    def new_fxn(*args, **kwargs):
        header = kwargs.get('header', True)
        test, answers = test_vals(*args, **kwargs)
        if header:
            print "\n\n********  Koan " + str(State.get_counter()) + "  ********\n\n"
        success = fxn(*args, **kwargs)
        if success:  # success
            print "\n\nEnlightenment Achieved!"
            State.inc_counter()
        else:  # failed
            print ("\n\nThrough failure learning is achieved. Try it again.\n\n")
            if not test:
                # this runs the caller fxn !!!
                kwargs['header']=False
                getattr(sys.modules['koans'], fxn.__name__)(**kwargs)
                #globals()[fxn.__name__](header=False)
        return success

    return new_fxn


def test_vals(*args, **kwargs):
    """Return vals in args and kwargs used for testing. Returns <bool test>,<list answers>."""
    test = 'test' in args
    answers = deque(kwargs.get('answers', []))
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
