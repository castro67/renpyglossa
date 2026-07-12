# Copyright (c) Alejandro Castro García
# SPDX-License-Identifier: MIT

# Because the Python deque type in the collections module is not revertible,
# I need to define something that works similarly

init python:
    class Deque:
        def __init__(self, iterable=None, maxlen=None):
            self.__head = None
            self.__tail = None
            self.__length = 0
            self.__maxlen = maxlen
            if iterable is not None:
                for item in iterable:
                    self.append(item)
        
        @property
        def maxlen(self):
            return self.__maxlen
        
        def append(self, item, /):
            o = {
                "prev": None,
                "next": None,
                "v": item
            }
            if self.__tail is None:
                self.__tail = o
                self.__head = o
            else:
                self.__tail["next"] = o
                o["prev"] = self.__tail
                self.__tail = o
            self.__length += 1
            if self.__maxlen is not None and self.__length > self.__maxlen:
                self.popleft()
    
        def appendleft(self, item, /):
            o = {
                "prev": None,
                "next": None,
                "v": item
            }
            if self.__head is None:
                self.__tail = o
                self.__head = o
            else:
                self.__head["prev"] = o
                o["next"] = self.__head
                self.__head = o
            self.__length += 1
            if self.__maxlen is not None and self.__length > self.__maxlen:
                self.pop()
    
        def clear(self):
            self.__head = None
            self.__tail = None
            self.__length = 0
        
        def pop(self):
            if self.__tail is None:
                raise IndexError
            o = self.__tail
            self.__tail = self.__tail["prev"]
            if  self.__tail is None:
                self.__head = None
            else:
                self.__tail["next"] = None
            self.__length -= 1
            return o["v"]
        
        def popleft(self):
            if self.__head is None:
                raise IndexError
            o = self.__head
            self.__head = self.__head["next"]
            if  self.__head is None:
                self.__tail = None
            else:
                self.__head["prev"] = None
            self.__length -= 1
            return o["v"]
        
        def __len__(self):
            return self.__length
        
        def __getitem__(self, index):
            if self.__length < 1 or index < 0 or index > self.__length - 1:
                raise IndexError
            if index > self.__length / 2:
                n = self.__length - 1
                o = self.__tail
                while n > index:
                    o = o["prev"]
                    n -= 1
                return o["v"]
            else:
                n = 0
                o = self.__head
                while n < index:
                    o = o["next"]
                    n += 1
                return o["v"]
        
        def __repr__(self):
            s = "[";
            o = self.__head
            sep = ""
            while o is not None:
                s += sep + str(o["v"])
                o = o["next"]
                sep = ", "
            s += "]"
            return s
