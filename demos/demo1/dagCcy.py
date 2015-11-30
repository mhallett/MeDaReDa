# dagCcy.py

class DAG(object): # functionality
    '''''Base DAG'''
    __shared_state = {}  # would be nice to use a collections.OrderedDict()
    def __init__(self):
        self.__dict__ = self.__shared_state

    def setValue(self,n,v):
        if v == n.value:
            return

        # build the DAG
        n.value = v
        for u in n.usedby:
           new_value = None
           try:
              new_value = u.calc()
           except:
               pass # leave value as None # Could set as error string ??
           self.setValue(u,new_value)

    def pp(self): # must be over ridden by a borg
        # use doc string on class
        print self.__doc__
        for k, v in self.__dict__ .items():
            if type(v) == type(Node()):
                print k,
                v.pp()

    def ppInputs(self):
        print self.__doc__, ' Inputs'
        print 'Override in local class'

    def ppOutputs(self):
        print self.__doc__, ' Outputs'
        for k, v in self.__dict__ .items():
            if type(v) == type(Node()):
                if v.usedby == []:
                    print k,
                    print '=', v.value, v.doc

class Node(object):
    def __init__(self,doc=None, calc=None):
        self.calc = calc
        self.doc = doc
        self.usedby = []
        self.value = None

    def pp(self):
        print '=', self.value , self.doc , 'used by', [n.doc for n in self.usedby], self.calc.__doc__

#----------------------------------------------------------
class MyDAG(DAG): # implementation
    '''''my dag'''
    def __init__(self):
        super(MyDAG, self).__init__()

        if hasattr(self,'a'):
            return
        self.a = Node('GBPUSD')
        self.b = Node('USDEUR')
        self.c = Node('EURGBP')

        # internal nodes, (func defined later [in code])
        self.d = Node('Mult', self.calcMult)

        self.a.usedby.append(self.d)
        self.b.usedby.append(self.d)
        self.c.usedby.append(self.d)

    # set input node functions
    def set_a(self,v):
        self.setValue(self.a,v)

    def set_b(self,v):
        self.setValue(self.b,v)

    def set_c(self,v):
        self.setValue(self.c,v)

    # get output values
    def get_d(self):
        return self.d.value

    def ppInputs(self):
        print self.__doc__, ' inputs'
        print 'a', '=', self.a.value, self.a.doc
        print 'b', '=', self.b.value, self.b.doc
        print 'c', '=', self.c.value, self.c.doc

    def calcMult(self ):
        '''''Mult 2 numbers'''
        return self.a.value * self.b.value * self.c.value


if __name__ == '__main__':
    print '-------------'
    MyDAG().set_a(2)
    MyDAG().set_b(5)
    DAG().pp()
    MyDAG().set_c(0.1)
    DAG().pp()
    MyDAG().ppInputs()
    DAG().ppOutputs()

    print 'mult = ', MyDAG().get_d()
