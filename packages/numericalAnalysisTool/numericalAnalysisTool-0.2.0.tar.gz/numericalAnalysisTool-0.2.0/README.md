# pyNumericalAnalysisToolKit
it's a python module use to make numerical analysis on mathematical formulas


## How to install 

```bash
pip install numericalAnalysisTool
```

## example 

You can find other example in [examples/](examples/) directory.

In this example I will take two function taking two paramter and returning one value. 

```math
f\_add(a,b) = a + b
```

```math
f\_mult(a,b) = a.b
```

So you will have to define those function 

```python 
def f_add(a,b):
    return a + b

def f_mult(a,b):
    return a * b
```

How to use the tool kit : 

```python
from numericalAnalysis.analysor import Analysor

analysor = Analysor()
params_dict = {"a" : [i/100 for i in range(0,100 +1)],# define range value for your parameter a
               "b" : range(-20,20,3) # range value for parameter b
               }
analysor.add_function(f_mult,params_dict)
analysor.add_function(f_add,params_dict)
analysor.compute()# it will compute product of every possible value for a and b gived before
analysor.draw_linear_2D_graph() # it will draw and save fig in "./graph" directory
```

It will product in [/example/graph]() directory all graph representing lineplot as the result of those function in function of every parameter.

### effect of parameter a 
![](examples/graph/scoring_function_multiplication_score_function_addition_a.png)

### effect of parameter b 

![](examples/graph/scoring_function_multiplication_score_function_addition_b.png)


