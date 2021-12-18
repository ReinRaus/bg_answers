import math

mult = 4 # находит результат для 1, 4 и 9

class mirrorXN():
    def __init__( self, right, mult ): # (self, string, int)
        self.mult = mult
        self.r  = str(right) # строкой
        self.ri = int(right) # целым числом
        self.rp = int( self.ri * self.mult / math.pow( 10, len(self.r) ) ) # сколько добавляется в старший разряд
        self.l  = str(self.ri * self.mult)[::-1][:len(self.r)] # зеркальное отражение умножения правой части на mult строкой
        self.l += "0"* ( len(self.r) - len(self.l) ) # добавление нулей в конец, если не хватает 01*4=4 ->40
        self.li = int(self.l) # целым числом
        self.lp = int( self.r[::-1] ) - self.li * self.mult # сколько надо добавить из младшего разряда
        if self.lp == self.rp: # если в старший разряд добавляется столько же, сколько нужно добавить из младшего разряда, то это искомое значение
            self.match( int(self.l + self.r) )
            if self.l[-1] == self.r[0]: # например, в 21978 цифра 9 может быть задействована как последняя цифра 219 и первая цифра 978
                self.match( int(self.l + self.r[1:]) ) # цифра 9 - центр симметрии и это тоже искомое значение

    def match(self, v):
        if str(v*self.mult) == str(v)[::-1]:
            res.append( v )
        else:
            print( 'Bad match:', v )
            
    def __str__(self):
        return self.l+"<<"+str(self.lp)+"..."+str(self.rp)+"<<"+self.r

for lastDigit in range(1,10):
    iters = 10
    res = []
    x = mirrorXN(lastDigit, mult)
    work2 = [x]
    while iters > 0:
        work = work2.copy()
        work2 = []
        for i in work:
            for appendDigit in range(0,10):
                x = mirrorXN( str(appendDigit)+i.r, mult )
                if x.lp>-1 and x.lp<x.mult and x.l[0]!='0': # по законам умножения в старший разряд может быть добавлено от 0 до mult-1, выходящие за
                    work2.append( x )                       # эти границы значения недопустимы, кроме того недопустимо, чтобы число начиналось на 0
                    print( x )
        iters -= 1
    if len(res)>0:
        res.sort()
        print( res )
        print( 'mult =', mult, '  last digit =', lastDigit )

