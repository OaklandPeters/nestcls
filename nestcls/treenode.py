"""
Instanced classes to be inherited from in the nested class structure.
"""

__all__ = ['TreeRoot', 'TreeNode']

class TreeNode(object):
    """Non-instanceable by default. __new__ directs to __call__.
        IE TreeNode(...) --> function call, not instantiation
    HOWEVER - it can still be instanced via TreeNode.make
    """
    def __new__(cls, *args, **kwargs):
        return cls.__call__(*args, **kwargs)
    def __init__(self, parent=None):
        self.parent = parent
    
    @classmethod
    def make(cls, parent=None):
        self = object.__new__(cls)
        self.__init__(parent=parent)
        return self
    
    @property
    def root(self):
        if self.parent is None:
            return self
        else:
            assert(isinstance(self.parent, TreeNode))
            return self.parent.root




class TreeRoot(TreeNode):
    """Actually instance-able version of TreeNode."""
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)
    @property
    def root(self):
        return self
