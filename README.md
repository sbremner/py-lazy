# py-lazy
A lazy loader for python modules (loads model on-access rather than on assignment). This allows a developer to program their code to leverage variables, functions or classes before they are assigned as long as they are not directly invoked. LazyObject's are dynamic and will update their value as their referenced module is updated.

Implemented with python version 3.4 (untested with other versions).

## Example Usage

```
import lazy

class Person(object):
  def __init__(self, name):
    self.name = name
    
  def print_name(self):
    print(self.name)

# Setup our lazy variable and create our Person
n = lazy.lazy('name')

# Note that using 'p = Person(name)' here would have thrown an error
p = Person(n)

# Assign a value to 'name' sometime later in the code
name = "James"

# Prints out > James
p.print_name()
```
