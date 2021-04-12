# Soft bodys simulation
It is based on a physic law : The hook law, for managing forces applied to mass points.
It inclueds euler integration.
## Code
### Hook's law : 

```x1, y1, x2, y2 = Points[i, j] ```

```Fx[j], Fy[j] += -k * R/d * (d - L0) ```

with ` k = stiffness constant` , ` R an array ([x2 - x1], [y2 - y1]) `and  ` L0 original lenght of the spring`

### Euler integration

```SumForces(j):
  F = [0, 0]
  F+= force(i, j)
  return F
```

and here, `j` is the other point of the spring. 

## Warings
There is no energy conservation, due to the euler integration. Have fun :)
