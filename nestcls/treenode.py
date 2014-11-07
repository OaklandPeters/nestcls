"""
Instanced classes to be inherited from in the nested class structure.
"""
import abc

__all__ = [
    'TreeNode',
    'TreeNodeInterface',
    'TreeRoot',
]

class TreeNodeInterface(object):
    """Defines aspects of TreeNode objects, which should be used by outside code."""
    __metaclass__ = abc.ABCMeta
    make = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
    root = abc.abstractproperty(lambda self: NotImplemented)
    subject = abc.abstractproperty(lambda self: NotImplemented)
    parent = abc.abstractproperty(lambda self: NotImplemented)


class TreeNode(TreeNodeInterface):
    """Non-instanceable by default. __new__ directs to __call__.
        IE TreeNode(...) --> function call, not instantiation
    HOWEVER - it can still be instanced via TreeNode.make
    """
    def __new__(cls, *args, **kwargs):
        return cls.__call__(*args, **kwargs)
    def __init__(self, parent=None):
        self._parent = parent

    @classmethod
    def make(cls, parent=None):
        """Alternate constructor, bypassing cls.__new__."""
        self = object.__new__(cls)
        self.__init__(parent=parent)
        return self

    @property
    def root(self):
        """Find the root of the tree. This should usually be an instance of TreeRoot."""
        if self.parent is None:
            return self
        else:
            assert(isinstance(self.parent, TreeNode))
            return self.parent.root
    @property
    def subject(self):
        """Retreives subject argument from root."""
        return self.root.subject
    @property
    def parent(self):
        """Outer containing class. Made a property to satisfy TreeNodeInterface."""
        return self._parent
    @parent.setter
    def parent(self, value):
        """Basic setter."""
        self._parent = value

class TreeRoot(TreeNode):
    """Actually instance-able version of TreeNode."""
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)
    def __init__(self, subject):
        self._subject = subject
        #set self.parent = None
        super(TreeRoot, self).__init__(None)
    @property
    def subject(self):
        return self._subject
    @subject.setter
    def subject(self, value): #pylint: disable=arguments-differ
        self._subject = value
