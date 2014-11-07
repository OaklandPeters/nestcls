"""
@todo: Replace functools.partial with types.MethodType ... MAYBE
"""
import functools

from .treenode import TreeNodeInterface

__all__ = [
    'InnerClass',
    'TerminalMethod',
]

class InnerClass(object):
    """A class nested within another one.

    Instances of class are stored on parent ('obj'), as '_{wrapped_class_name}'
    """
    def __init__(self, wrapped_class):
        if not issubclass(wrapped_class, TreeNodeInterface):
            raise TypeError("'wrapped_class' must be a subclass of TreeNodeInterface.")
        self.wrapped_class = wrapped_class
        self.class_name = wrapped_class.__name__
        self.inst_name = '_' + self.class_name

    def __get__(self, obj, klass=None):
        if is_klass(obj, klass):
            return self.wrapped_class
        elif is_instance(obj, klass):
            #if parent is an instance, then instantiate this as well
            if not hasattr(obj, self.inst_name):
                setattr(obj, self.inst_name, self.wrapped_class.make(parent=obj))
            return getattr(obj, self.inst_name)
        else:
            raise TypeError("Unrecognized input combination.")

class TerminalMethod(object):
    def __init__(self, func):
        self.func = func
    def __get__(self, obj, klass=None):
        if is_klass(obj, klass): # ~return classmethod
            return functools.partial(
                self.func,
                klass
            )
        elif is_instance(obj, klass): # ~return instancemethod + partial-function on subject
            return functools.partial(
                self.func,
                obj,
                obj.root.subject
            )
        else:
            raise TypeError("Unrecognized input combination.")

#------------------------------------------------------------------------------
#    Local Utility Functions
#------------------------------------------------------------------------------
def is_klass(obj, klass):
    """In __get__ descriptor - were arguments passed in from a class/classmethod?"""
    return (obj is None) and (klass is not None)
def is_instance(obj, klass):
    """In __get__ descriptor - were arguments passed in from an instance/instancemethod?"""
    return (obj is not None) and (klass is not None)
