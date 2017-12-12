from git import Repo, exc
import os


class GitRepo(object):
    def __init__(self, root=None, remote="origin", lazy=True):
        self.remote_name = remote
        self._root = root
        self._repo = None
        if not lazy:
            self.repo

    @property
    def repo(self):
        if self._repo is None:
            if self.remote_name is None:
                self._repo = False
            else:
                try:
                    self._repo = Repo(self._root or os.getcwd(),
                                      search_parent_directories=True)
                except exc.InvalidGitRepositoryError:
                    self._repo = False
        return self._repo

    @property
    def enabled(self):
        return self.repo

    @property
    def root(self):
        if not self.repo:
            return False
        return self.repo.git.rev_parse("--show-toplevel")

    @property
    def dirty(self):
        if not self.repo:
            return False
        return self.repo.is_dirty()

    @property
    def last_commit(self):
        if not self.repo:
            return None
        return self.repo.head.commit.hexsha

    @property
    def branch(self):
        if not self.repo:
            return None
        return self.repo.head.ref.name

    @property
    def remote(self):
        if not self.repo:
            return None
        try:
            return self.repo.remotes[self.remote_name]
        except IndexError:
            return None

    @property
    def remote_url(self):
        if not self.remote:
            return None
        return self.remote.url
    
    def get_upstream_fork_point(self):
        """Get the most recent ancestor of HEAD that occurs on an upstream
        branch.
        
        First looks at the current branch's tracking branch, if applicable. If
        that doesn't work, looks at every other branch to find the most recent
        ancestor of HEAD that occurs on a tracking branch.
        
        Returns:
            git.Commit object or None
        """
        possible_relatives = []
        try:
            active_branch = self.repo.active_branch
        except TypeError:
            pass  # detached head
        else:
            tracking_branch = active_branch.tracking_branch()
            if tracking_branch:
                possible_relatives.append(tracking_branch.commit)
        
        if not possible_relatives:
            for branch in self.repo.branches:
                tracking_branch = branch.tracking_branch()
                if tracking_branch is not None:
                    possible_relatives.append(tracking_branch.commit)
        
        head = self.repo.head
        most_recent_ancestor = None
        for possible_relative in possible_relatives:
            # at most one:
            for ancestor in self.repo.merge_base(head, possible_relative):
                if most_recent_ancestor is None:
                    most_recent_ancestor = ancestor
                elif most_recent_ancestor.is_ancestor(ancestor):
                    most_recent_ancestor = ancestor
        
        return most_recent_ancestor

    def tag(self, name, message):
        try:
            return self.repo.create_tag("wandb/" + name, message=message, force=True)
        except exc.GitCommandError:
            print("Failed to tag repository.")
            return None

    def push(self, name):
        if self.remote:
            try:
                return self.remote.push("wandb/" + name, force=True)
            except exc.GitCommandError:
                return None
