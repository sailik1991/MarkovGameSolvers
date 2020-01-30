__author__ = "Sailik Sengupta"

'''
Prints the Value function and optimal policy for each state.
'''
def print_iteration_info(k, V, pi):
    if k != 300:
        return
    print ('---------------')
    print("Itreation -- {}".format(k))
    print ('---------------')

    for s in range(len(V)):
        print("V({})  : {}".format(s, V[s]))
        print("pi({}) : {}".format(s, pi[s]))
    print()
