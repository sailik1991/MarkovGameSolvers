import numpy as np
import nashpy as nash
from strategy import Strategy

__author__ = "Sailik Sengupta"

class UniformRandom(Strategy):
    def get_name(self):
        return 'UR'

    def get_value(self, s, A_D, A_A, R_D, R_A, T, Q_D, Q_A):
        num_d = len(A_D)
        num_a = len(A_A)

        # Get Defender/Leader's Q-value matrix
        M_D = []
        M_A = []
        for d in range(num_d):
            row_D = []
            row_A = []
            for a in range(num_a):
                k = '{}_{}_{}'.format(s, A_D[d], A_A[a])
                row_D.append( Q_D[k] )
                row_A.append( Q_A[k] )
            M_D.append(row_D)
            M_A.append(row_A)

        g = nash.Game(M_D, M_A)
        
        D_s = [1.0/num_d for i in range(num_d)]
        game_value = [-10000,-10000]
        U_A = -100
        for a in range(num_a):
            A_s = [0 for i in range(num_a)]
            A_s[a] = 1.0
            U = g[D_s, A_s]
            if U[1] > game_value[1]:
                game_value = U

        policy = {}
        for d in range(num_d):
            policy['pi_{}'.format(A_D[d])] = D_s[d]

        return game_value[0], game_value[1], policy

class NashEq(Strategy):
    def get_name(self):
        return 'NE'

    def get_value(self, s, A_D, A_A, R_D, R_A, T, Q_D, Q_A):
        num_d = len(A_D)
        num_a = len(A_A)

        # Get Defender/Leader's Q-value matrix
        M_D = []
        M_A = []
        for d in range(num_d):
            row_D = []
            row_A = []
            for a in range(num_a):
                k = '{}_{}_{}'.format(s, A_D[d], A_A[a])
                row_D.append( Q_D[k] )
                row_A.append( Q_A[k] )
            M_D.append(row_D)
            M_A.append(row_A)

        g = nash.Game(M_D, M_A)
        try:
            D_s, A_s = list(g.support_enumeration())[0]
        except IndexError:
            # Game is degenerate
            D_s, A_s = list(g.lemke_howson_enumeration())[0]
        game_value = g[D_s, A_s]

        policy = {}
        for d in range(num_d):
            policy['pi_{}'.format(A_D[d])] = D_s[d]

        return game_value[0], game_value[1], policy

class StackelbergEq(Strategy):
    def get_name(self):
        return 'SSE'

    def get_value(self, s, A_D, A_A, R_D, R_A, T, Q_D, Q_A):
        num_d = len(A_D)
        num_a = len(A_A)
        
        m = self.lib.Model('MIQP')
        m.setParam('OutputFlag', 0)
        m.setParam('LogFile', '')
        m.setParam('LogToConsole', 0)
        
        # Add defender stategies to the model
        x = []
        for i in range(num_d):
            n = 'x_{}'.format(A_D[i])
            x.append(m.addVar(lb=0, ub=1, vtype=self.lib.GRB.CONTINUOUS, name=n))
        m.update()

        # Add defender stategy constraints
        con = self.lib.LinExpr()
        for i in range(num_d):
            con.add(x[i])
        m.addConstr(con==1)

        obj = self.lib.QuadExpr()
        M = 100000000

        q=[]
        for i in range(num_a):
            n = 'q_{}'.format(A_A[i])
            q.append(m.addVar(lb=0, ub=1, vtype=self.lib.GRB.INTEGER, name=n))

        V_a = m.addVar(lb=-self.lib.GRB.INFINITY, ub=self.lib.GRB.INFINITY, vtype=self.lib.GRB.CONTINUOUS, name="V_a")
        m.update()

        # Get Defender/Leader's Q-value matrix
        M_D = []
        M_A = []
        for d in range(num_d):
            row_D = []
            row_A = []
            for a in range(num_a):
                k = '{}_{}_{}'.format(s, A_D[d], A_A[a])
                row_D.append( Q_D[k] )
                row_A.append( Q_A[k] )
            M_D.append(row_D)
            M_A.append(row_A)

        # Update objective function
        for i in range(num_d):
            for j in range(num_a):
                obj.add( M_D[i][j] * x[i] * q[j] )

        # Add constraints to make attaker have a pure strategy
        con = self.lib.LinExpr()
        for j in range(num_a):
            con.add(q[j])
        m.addConstr(con==1)
    
        # Add constrains to make attacker select dominant pure strategy
        for j in range(num_a):
            val = self.lib.LinExpr()
            val.add(V_a)
            for i in range(num_d):
                val.add( float(M_A[i][j]) * x[i], -1.0)
            m.addConstr( val >= 0, q[j].getAttr('VarName')+"_lb" )
            m.addConstr( val <= (1-q[j]) * M, q[j].getAttr('VarName')+"_ub" )

        # Set objective funcion as all attackers have now been considered
        m.setObjective(obj, self.lib.GRB.MAXIMIZE)

        # Solve MIQP
        m.optimize()
        #m.computeIIS()
        #m.write('forum2.ilp')
        #m.write('forum2.mps')

        game_value_a = 0
        policy = {}
        for var in m.getVars():
            if 'x_' in var.varName:
                policy[var.varName] = float(var.x)
            if 'V_a' in var.varName:
                game_value_a = float(var.x)

        return float(m.ObjVal), game_value_a, policy

def main():    
    agents = [UniformRandom(), NashEq(), StackelbergEq()]

    s_header = 'gamma '
    s = ''
    # s = 'gamma V0_ur V1_ur V2_ur V3_ur V0_n V1_n V2_n V3_n V0_s V1_s V2_s V3_s'
    for gamma in range(0, 100, 5):
        
        gamma = gamma/100.0
        s += '\n{} '.format(gamma)

        for agent in agents:
            
            agent.set_gamma(gamma)
            V, pi = agent.run()
            
            for state in V.keys():
                if '\n' not in s_header:
                    s_header += 'V{}_{} '.format(state, agent.get_name())
                s += '{} '.format(V[state])

        if '\n' not in s_header:
            s_header += '\n'

    s = s_header + s
    return s


if __name__ == '__main__':
    print(main())
