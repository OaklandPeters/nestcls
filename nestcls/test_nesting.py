"""
Test file.


@todo: Delete the earlier tests, and refactor/collapse files so decorators has only:  InnerClass, InnerClassTerminalMethod
@todo: Consider refactoring InnerClassTerminalMethod into 2 decorators: @variantmethod + @instancepartialmethod

@todo: Rename this to test_nested_class.py
@todo: See if I can merge TerminalMethod/TerminalClassMethod
@todo: See if TerminalClass can be made to remove need for TerminalClassMethod
"""
import os
import unittest

from decorators import (
    InnerClass, InnerClassTerminalMethod,
    TerminalClass, TerminalMethod
)
from treenode import TreeNode, TreeRoot





class Validator(TreeRoot):
    """Example of desired use-case"""
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        super(Validator, self).__init__(None)
    @InnerClass
    class Assert(TreeNode):
        """Primary nested class."""
        @InnerClass
        class Type(TreeNode):
            """Procedure-style nested class.
            Intended to be treated as a function."""
            @InnerClassTerminalMethod
            def __call__(self, instance, klass):
                if not isinstance(instance, klass):
                    raise TypeError("Must be {0}".format(klass.__name__))
                return instance

        @InnerClassTerminalMethod
        def IsDir(self, path):
            if not os.path.isdir(path):
                raise ValueError("'path' is not a directory.")
            return path



class InnerClassTerminalMethodTests(unittest.TestCase):
    """Nests using @InnerClass, and a special decorator for method calls."""
    def setUp(self):
        """Create nested class structure."""


        self.validator = Validator
        self.string = "aaa"
        self.good_klass = basestring
        self.bad_klass = int

    def test_classmethod(self):
        """Accessing Validator as a classmethod."""
        self.assertEqual(
            self.validator.Assert.Type(self.string, self.good_klass),
            self.string
        )
        self.assertRaises(
            TypeError,
            lambda: self.validator.Assert.Type(self.string, self.bad_klass)
        )
    def test_instancemethod(self):
        """Accessing Validator nested methods as instancemethods."""
        val = self.validator(self.string)
        self.assertEqual(
            val.Assert.Type(self.good_klass),
            self.string
        )
        self.assertRaises(
            TypeError,
            lambda: val.Assert.Type(self.bad_klass)
        )

    def test_sideterminal(self):
        self.assert_(self.validator.Assert.IsDir('/Users/'))
        self.assertRaises(
            ValueError,
            lambda: self.validator.Assert.IsDir('/NonExistant/')
        )
        val = self.validator('/Users/')
        self.assertEquals(val.Assert.IsDir(), '/Users/')
         
         
         
        val2 = self.validator('/NonExistant/') 
         
        print()
        self.assertRaises(
            ValueError,
            lambda: val2.Assert.IsDir()
        )

    def test_instance_uniqueness_problem(self):
        val1 = self.validator('aaa')
        val2 = self.validator('bbb')
        
        as1 = val1.Assert
        as2 = val2.Assert

        self.assert_(val1 != val2)
        self.assert_(as1 != as2)




if __name__ == "__main__":
    unittest.main()

    