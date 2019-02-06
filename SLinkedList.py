# Linked list class and support classes.
#


class ListNode(object):
    '''Represents an item on a linked list.

    There are two attributes, one to hold the value stored in
    the list, the next "points" to the next node on the list.
    The last node on the list always has its link set to some
    "sentinel" value, such as None in Python or null in Java.
    '''
    def __init__(self, value = None):
        '''Construct a list node.'''
        self.value = value
        self.link = None

class SinglyLinkedList(object):
    '''Class that defines a relatively simple linked list, with a
    single link leading from a predecessor node to a successor node.

    Implements several methods, modeled on those in the standard
    list() class. In addition, implements a "prepend()" method that
    illustrates adding an element to the beginning of a list.

    Methods of the standard list class that we do not implement include:
    clear(), copy(), extend(), __add__(), __mul__(), reverse(), and sort().
    '''
    def __init__(self, iterable = None):
        '''Creates a new list, initialized to the contents of 
        'iterable'.'''
        self.head = None
        if iterable != None:
            previous = None
            for value in iterable:
                newnode = ListNode(value)
                if previous == None:
                    self.head = newnode
                else:
                    previous.link = newnode
                previous = newnode
        if iterable:
            self.size = len(iterable)
        else:
            self.size = 0

    def prepend(self, value):
        '''Add an element to the beginning of the list.'''
        node = ListNode(value)
        node.link = self.head
        self.head = node
        self.size += 1

    def get(self, index):
        '''Get the value stored at a particular index
        of the linked list.'''
        count = 0
        node = self.head
        while node != None:
            if count == index:
                return node.value
            node = node.link
            count += 1
        raise IndexError('list index out of range')

    def count(self, value):
        '''Count the number of list nodes with values equal to the
        'value'.'''
        count = 0
        node = self.head
        while node != None:
            if node.value == value:
                count += 1
            node = node.link
        return count

    def index(self, value):
        '''Return the index of the first list element that matches
        the given 'value'.'''
        count = 0
        node = self.head
        while node != None:
            if node.value == value:
                return count
            count += 1
            node = node.link
        raise ValueError('Value ' + str(value) + ' not found.')
            
    def append(self, value):
        '''Add an element to the end of the linked list.
        '''
        self.size += 1
        node = self.head
        if node == None:    # Empty list
            self.head = ListNode(value)
        else:
            while node.link != None:
                node = node.link
            node.link = ListNode(value)
        

    def insert(self, index, value):
        '''Add an element at a particular index of a linked
        list.'''
        self.size += 1
        newnode = ListNode(value)
        node = self.head
        if index == 0:
            newnode.link = self.head
            self.head = newnode
        else:
            count = 1
            while node.link != None and count < index:
                node = node.link
                count += 1
            newnode.link = node.link
            node.link = newnode
        
        
    def remove(self, value):
        '''Remove the first element that matches 'value' from the list.'''
        self.size -= 1
        previous = None
        node = self.head
        while node != None and node.value != value:
            previous = node
            node = node.link
        if node == None:
            raise ValueError('Value ' + str(value) + ' not found.')
        elif previous != None:
            previous.link = node.link
        else:
            self.head = node.link
        

    def pop(self, index = -1):
        '''Removes an node from the list based on a given
        index. If the index is -1, the last node on list is
        removed. Returns the value associated with the deleted
        node.'''
        count = 0
        previous = None
        node = self.head
        self.size -= 1
        if index >= 0:
            while node != None and count != index:
                count += 1
                previous = node
                node = node.link
        else:
            while node != None and node.link != None:
                previous = node
                node = node.link
        if node == None:
            raise ValueError('Position ' + str(index) + ' not found.')
        
        if previous != None:
            previous.link = node.link
        else:
            self.head = node.link

        return node.value
        

    def __bool__(self):
        '''Returns True if the list is non-empty.'''
        return self.head != None

    def __len__(self):
        '''Returns the total number of nodes on the list.'''
        if not self:
            return 0
        return self.size
        
       

    def __str__(self):
        '''Convert a linked list to a string representation.
        '''
        node = self.head
        r = '['
        while node != None:
            r += str(node.value)
            if node.link != None: # If not at the end,
                r += ', '         #  add a comma and space.
            node = node.link
        r += ']'
        return r

    def __eq__(self, other):
        '''Compare two linked lists for equality.
        '''
        node1 = self.head
        node2 = other.head
        while node1 != None and node2 != None:
            if node1.value != node2.value:
                return False
            node1 = node1.link
            node2 = node2.link
        return node1 == None and node2 == None

    def __iter__(self):
        '''Implement Python iteration.'''
        return ListIter(self.head)
    
    def clear(self):
        self.size = 0
        for node in self:
            self.remove(node)
        return self
        

    def copy(self):
        new = SinglyLinkedList()
        for node in self:
            new.append(node)
        return new

    def __gt__(self,other):
        if len(self) != len(other):
            return len(self) > len(other)
        else:
            for i in range(len(self)):
                if self.get(i) == other.get(i):
                    continue
                else:
                    return self.get(i) > other.get(i)
            return False

    def extend(self, iterable):
        self.size += len(iterable)
        for item in iterable:
            self.append(item)
        return self
        
        
    def reverse(self):
        for i in range(1,len(self)):
            self.prepend(self.get(i))
            self.pop(i+1)   
        return self


class ListIter(object):
    '''Class that represents a list iterator.'''
    def __init__(self, head):
        '''Initialize the iterator.'''
        self.cursor = head
    def __next__(self):
        '''Advance to the next item in the iterator.'''
        if self.cursor != None:
            result = self.cursor
            self.cursor = result.link
            return result.value
        raise StopIteration()

### Testing code ###

if __name__ == "__main__":
    print("Testing the SinglyLinkedList class.")
    r = SinglyLinkedList()
    r.prepend(5)
    r.prepend(100)
    print(r)
    assert str(r) == "[100, 5]"
    assert r.get(0) == 100
    assert r.get(1) == 5
    
    s = SinglyLinkedList(range(1, 11))
    print(s)
    for x in s:
        assert s.index(x) == x - 1

    for i in range(10, 0, -1):
        assert s.index(i) == i - 1
        assert s.get(i - 1) == i
        
    s.remove(9)
    assert len(s) == 9
    assert s.count(9) == 0
    s.pop(1) # remove second node
    assert len(s) == 8
    assert s.get(1) == 3
    s.pop()
    assert len(s) == 7
    assert s.get(6) == 8
    assert s.pop(0) == 1
    assert s.get(0) == 3
    s.remove(3)
    assert len(s) == 5
    assert s.get(0) == 4
    s.remove(8)
    assert len(s) == 4
    assert s.get(0) == 4

    t = SinglyLinkedList()
    assert str(t) == "[]"
    assert len(t) == 0
    try:
        t.pop()
    except ValueError as ex:
        pass
    else:
        assert False
    try:
        t.index(10)
    except ValueError as ex:
        pass
    else:
        assert False
    t.append(10)
    t.append(21)
    t.append(19)
    assert t.index(10) == 0
    assert t.index(21) == 1
    assert str(t) == "[10, 21, 19]"
    t.insert(100, 55)
    t.insert(1, 1)
    t.insert(5, 8)
    t.insert(1, 21)
    assert t.count(21) == 2
    assert t.count(22) == 0
    print(t)
    try:
        print(t.index(22))
    except ValueError as ex:
        pass
    else:
        assert False

    while t:
        t.pop()

    x1 = SinglyLinkedList()
    x1.append(5)
    x1.append(10)
    x2 = SinglyLinkedList()
    x2.append(5)
    x2.append(10)
    assert x1 == x2
    x2.append(8)
    assert x1 != x2
    x1.append(8)
    assert x1 == x2
    x1.append(5)
    assert x1 != x2
    x1.pop()
    assert x1 == x2

    # Performance check. Compare the time taken for
    # many calls to insert() and len() (remember that
    # calling len() on a SinglyLinkedList() will call
    # the __len__() method defined above.
    #
    def performance(x):
        import time
        start = time.time()
        for i in range(100000):
            x.insert(0, i)
        elapsed = time.time() - start
        print('insert(): {:.5f} sec.'.format(elapsed))
        start = time.time()
        for i in range(1000):
            t = len(x)
        elapsed = time.time() - start
        print('len() {:.5f} sec.'.format(elapsed))

    print("Performance of Python list()")
    performance(list())
    print("Performance of SinglyLinkedList()")
    performance(SinglyLinkedList())
