class Point:
    def __init__(self,x,y):
        self.x_cod = x
        self.y_cod = y
        
    def __str__(self):
        return '<{},{}'.format(self.x_cod,self.y_cod)
    
    def Euclidean_distnce(self,other):
        return ((self.x_cod - other.x_cod)**2 + (self.y_cod - other.y_cod)**2)**0.5
    
class line:
    def __init__(self,A,B,C):
        self.A  = A
        self.B = B
        self.C = C
        
    def __str__(self):
        return '{}x +{}y +{} =0'.format(self.A,self.B,self.C)
    def point_of_line(line,point):
        if line.A*point.x_cod + line.B*point.y_cod + line.C ==0:
            return 'it lies on point'
        else:
            return ' it does not lies on line'
p1= Point(0,0)
p2=Point(9,3)
p3 = line( 1,1,2)
print(p3.point_of_line(p1))
print(p1.Euclidean_distnce(p2))

print(Point(-9,-3))
print(Point(-9,3))
