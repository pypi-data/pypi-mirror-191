from pricetree import PriceTree
import timeit

# #Binomial option pricing test script
tree = PriceTree(13, 0.5, 0.05, 1, 0.24)
tree.value_option(11, nat='E', prnt=True)
print('Should be $2.285\n')

tree = PriceTree(13, 0.5, 0.05, 2, 0.24)
tree.value_option(11, nat='E', prnt=True)
print('Should be $2.44\n')

tree = PriceTree(20, 2/3, 0.04, 2, 0.3)
tree.value_option(12, 'E', prnt=True)
print('Should be $8.316\n')
tree.value_option(25, 'E', 'P', prnt=True)
print('Should be $5.124\n')

tree = PriceTree(100, 0.75, 0.05, 3, 0.2)
tree.value_option(110, 'E', 'P', prnt=True)
print('Should be $9.90\n')

tree = PriceTree(50, 1, 0.06, 3, 0.2)
tree.value_option(50, 'E', 'P', prnt=True)
print('Should be $2.86\n')
tree.value_option(50, 'A', 'P', prnt=True)
print('Should be $3.05\n')

tree = PriceTree(40, 1, 0.1, 3, 0.26)
tree.value_option(46, 'E', 'P', prnt=True)
print('Should be $4.69\n')
tree.value_option(46, 'A', 'P', prnt=True)
print('Should be $6.13\n')

# def test_fn():
#     tree = PriceTree(40, 1, 0.1, 1000, 0.26)
#     tree.value_option(46, 'E', 'P')
    
# print(timeit.timeit(lambda: test_fn(), number = 100))

# print(valueOption(40, 46, 1, 0.1, 3, 0.26, 'B', 'P', False, [1, 3])[0])
# print('Should be $5.85\n')