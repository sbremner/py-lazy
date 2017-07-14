import inspect
import numbers

class LazyObject(object):
    def __init__(self, module=None, modulename=None):
        self.module = module
        
        if not self.module:
            self.module = inspect.getmodule(inspect.stack()[1][0])
            
        self.modulename = modulename
        
    @property
    def object(self):
        return self.resolve()
        
    def __repr__(self):
        return self.object.__repr__()
        
    def __str__(self):
        return self.object.__str__()

    def __hash__(self):
        return self.object.__hash__()
      
    def __bool__(self):
        return self.object.__bool__()
      
    def __getattr__(self, key):            
        if hasattr(self.object, key):
            return getattr(self.object, key, None)
            
        return getattr(self, key, None)

    def __eq__(self, other):
        # Resolve other if it is a lazy object
        if isinstance(other, LazyObject):
            other = other.resolve()
        
        # Types and values should be the same
        return type(self.object) == type(other) and self.object == other
        
    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if not isinstance(self.object, numbers.Number):
            raise TypeError("{0} is not a Number".format(self.object))
            
        if not isinstance(other, numbers.Number):
            raise TypeError("{0} is not a Number".format(other))
        
        return self.object + other
        
    def __sub__(self, other):
        if not isinstance(self.object, numbers.Number):
            raise TypeError("{0} is not a Number".format(self.object))
            
        if not isinstance(other, numbers.Number):
            raise TypeError("{0} is not a Number".format(other))
        
        return self.object - other
        
    def __mul__(self, other):
        if not isinstance(self.object, numbers.Number):
            raise TypeError("{0} is not a Number".format(self.object))
            
        if not isinstance(other, numbers.Number):
            raise TypeError("{0} is not a Number".format(other))
        
        return self.object * other
    
    def __div__(self, other):
        if not isinstance(self.object, numbers.Number):
            raise TypeError("{0} is not a Number".format(self.object))
            
        if not isinstance(other, numbers.Number):
            raise TypeError("{0} is not a Number".format(other))
        
        return self.object / other
    
    # If our lazy object happens to be a function
    # or class, we can call it directly
    def __call__(self, *args):
        f = self.resolve()
        
        if not inspect.isfunction(f) and not inspect.isclass(f):
            raise TypeError('LazyObject is not callable: {0}'.format(f))

        return f(*args)
        
    def resolve(self, default=None):
        return getattr(self.module, self.modulename, default)


# Utility function to import the module and get back our LazyObject
def lazy(modulename):
    stack = inspect.stack()[1]   
    frame = stack[0]
        
    mod = inspect.getmodule(frame)
    return LazyObject(module=mod, modulename=modulename)