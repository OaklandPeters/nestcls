"""
Test file, also containing a skeleton of the structure for Validator.
"""
import os
import unittest

from nestcls.decorators import InnerClass, TerminalMethod
from nestcls.treenode import TreeNode, TreeRoot


class Validator(TreeRoot):
    """Example of desired use-case"""
    @InnerClass
    class Assert(TreeNode):
        """Primary nested class."""
        @InnerClass
        class Type(TreeNode):
            """Procedure-style nested class.
            Intended to be treated as a function."""
            @TerminalMethod
            def __call__(self, instance, klass):
                if not isinstance(instance, klass):
                    raise TypeError("Must be {0}".format(klass.__name__))
                return instance

        @TerminalMethod
        def IsDir(self, path): #pylint: disable=no-self-use, invalid-name
            """Standard terminal method. Contrasts with Type (procedure-style)."""
            if not os.path.isdir(path):
                raise ValueError("'path' is not a directory.")
            return path



class NestingTests(unittest.TestCase):
    """Nests using @InnerClass, and a special decorator for method calls."""
    def setUp(self):
        """Create nested class structure."""
        self.string = "aaa"
        self.good_klass = basestring
        self.bad_klass = int

    def test_classmethod(self):
        """Accessing Validator as a classmethod."""
        self.assertEqual(
            Validator.Assert.Type(self.string, self.good_klass),
            self.string
        )
        self.assertRaises(
            TypeError,
            lambda: Validator.Assert.Type(self.string, self.bad_klass)
        )
    def test_instancemethod(self):
        """Accessing Validator nested methods as instancemethods."""
        val = Validator(self.string)
        self.assertEqual(
            val.Assert.Type(self.good_klass),
            self.string
        )
        self.assertRaises(
            TypeError,
            lambda: val.Assert.Type(self.bad_klass)
        )

    def test_terminalmethod(self):
        """Test a terminal method, NOT a procedural-style function-class."""
        self.assert_(Validator.Assert.IsDir('/Users/')) #pylint: disable=no-value-for-parameter
        self.assertRaises(
            ValueError,
            lambda: Validator.Assert.IsDir('/NonExistant/') #pylint: disable=no-value-for-parameter
        )
        val = Validator('/Users/')
        self.assertEquals(val.Assert.IsDir(), '/Users/') #pylint: disable=no-value-for-parameter

        val2 = Validator('/NonExistant/')
        self.assertRaises(
            ValueError,
            lambda: val2.Assert.IsDir() #pylint: disable=no-value-for-parameter, unnecessary-lambda
        )

    def test_instance_uniqueness(self):
        """Used to check for a previously encountered instance-uniqueness problem."""
        val1 = Validator('aaa')
        val2 = Validator('bbb')

        as1 = val1.Assert
        as2 = val2.Assert

        self.assert_(val1 != val2)
        self.assert_(as1 != as2)




if __name__ == "__main__":
    unittest.main()

    