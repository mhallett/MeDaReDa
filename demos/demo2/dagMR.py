# dagMR.py
# dag MedaReda

print '#############'

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
           try:
              new_value = u.calc()
           except:
               new_value = None # leave value as None # Could set as error string ??
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

        # build the DAG
        self.a = Node('A')
        self.b = Node('B')
        self.c = Node('C')
        self.d = Node('D')
        self.h = Node('Ccy')

        # internal nodes, (func defined later [in code])
        self.e = Node('E', self.calcEgMult)
        self.f = Node('F', self.calcEgAdd2 )
        self.g = Node('G', self.calcZ )
        self.i = Node('I', self.calcUSD )

        # define dependencies for each internal node
        # e ------------------------------
        self.a.usedby.append(self.e)
        self.b.usedby.append(self.e)

        # f ------------------------------
        self.c.usedby.append(self.f)
        self.d.usedby.append(self.f)

        # g ------------------------------
        self.e.usedby.append(self.g)
        self.f.usedby.append(self.g)

        # i ------------------------------
        self.a.usedby.append(self.i)
        self.h.usedby.append(self.i)

    # functions for setting input nodes
    def set_a(self,v):
            self.setValue(self.a,v)

    def set_b(self,v):
            self.setValue(self.b,v)

    def set_c(self,v):
            self.setValue(self.c,v)

    def set_d(self,v):
            self.setValue(self.d,v)

    def set_ccy(self,v):
            self.setValue(self.h,v)

    def ppInputs(self):
        print self.__doc__, ' inputs'
        print 'a', '=', self.a.value, self.a.doc
        print 'b', '=', self.b.value, self.b.doc
        print 'c', '=', self.c.value, self.c.doc
        print 'd', '=', self.d.value, self.d.doc
        print 'h', '=', self.h.value, self.h.doc

    def calcEgAdd2(self ):
        '''''Add 2 numbers'''
        return self.c.value + self.d.value # a * b

    def calcEgMult(self ):
        '''''Mult 2 numbers'''
        return self.a.value * self.b.value

    def calcZ(self ):
        '''''Z Eg final calc'''
        return  self.e.value + 2 * self.f.value

    def calcUSD(self ):
        '''''Use ccy'''
        ccy = self.h.value
        a = self.a.value
        if ccy == 'USD':
            return a * 2
        return  0


print '-------------'

MyDAG().set_a(1)
MyDAG().set_b(2)
MyDAG().set_c(3)
MyDAG().set_d(4)
MyDAG().set_ccy('USD')
DAG().pp()
MyDAG().ppInputs()
DAG().ppOutputs()
MyDAG().set_a(5)
DAG().ppOutputs()
