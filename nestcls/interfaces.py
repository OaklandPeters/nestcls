import abc



class PredicateInterface(object):
    """
    Predicate classes define all actual function implementations.
        Those implementations are used by child classes - of either
        Assert/Check varieties.
    """
    __metaclass__ = abc.ABCMeta

class AssertInterface(object):
    """Flow-control logic, and abstract methods for ASSERT variety functions.
    The __call__ provided by this class should trigger the entire logic.
    """
    __metaclass__ = abc.ABCMeta

class CheckInterface(object):
    """Flow-control logic AND abstract methods for CHECK variety functions.
    The __call__ provided by this class should trigger the entire logic.
    """
    __metaclass__ = abc.ABCMeta





# This is **JUST** an idea. Actual implementation must be structured differently
class Assertion(object):
    """This is a stub of structure.
    PROBLEM: this structure only makes sense on an *instanced* class - not one that is callable as class.
    
    @todo: Make this structured to mesh with Validate, IE so that it has a `subject` - the first argument 
    @todo: Consider: having this *only* accept message. With message being generated prior - by calling function.
    
    predicate: function, returning boolean. ~filter-criteria
    """
    
    def __init__(self, predicate, subject,
                 args=tuple(), kwargs=dict(),
                 exception=TypeError, message=None,
                 name="'object'", message_factory=None):
        self.predicate = predicate
        self.subject = subject
        self.args = args
        self.kwargs = kwargs
        self.name = name
        self.exception = exception
        self.message = message # Property. Should do something sophisticated with templates and name
    def __bool__(self):
        return bool(self.predicate(*self.args, **self.kwargs))
    def __call__(self):
        if not bool(self):
            raise self.exception(self.message)