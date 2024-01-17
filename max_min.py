import math
import matplotlib.pyplot as plt
import random
import copy

from gobang import draw, check, get_points, my_chess
from evaluate import Evaluate





class Node2():
    """
    搜索树结点
    """
    def __init__(self, deep, state, parent=None):
        self.deep = deep
        self.state = state
        self.points = []
        self.parent = parent
        self.children = []
        self.alpha = -1e+6
        self.beta = 1e+6


class State2():
    """
    状态定义：在(i, j)处落子v形成棋盘chess
    """
    def __init__(self, i, j, v, chess):
        self.i = i
        self.j = j
        self.v = v
        self.chess = chess


def max_min(root, max_deep):
    evaluate = Evaluate(10)
    v_min = root.state.v
    v_max = v_min % 2 + 1
    stack = [root]
    while stack != []:
        current = stack[-1]
        if current.points == []:
            # 当前结点后代全部探索完
            parent = current.parent
            if parent:
                grand = parent.parent
                if grand:
                    if current.state.v == v_min and parent.alpha < current.beta:
                        parent.alpha = current.beta
                        if parent.alpha >= grand.beta:
                            parent.points = []
                    if current.state.v == v_max and parent.beta > current.alpha:
                        parent.beta = current.alpha
                        if parent.beta <= grand.alpha:
                            parent.points = []
            stack.pop()
        else:
            deep = current.deep + 1
            point = current.points.pop()
            i, j = point[1], point[2]
            v = current.state.v % 2 + 1
            chess = copy.deepcopy(current.state.chess)
            chess[i][j] = v
            state = State2(i, j, v, chess)
            node = Node2(deep, state, parent=current)             
            if deep == max_deep:
                node.points = []
                node.alpha = evaluate.evaluate(chess, v_max)
            else:       
                node.points = get_points(chess)
            current.children.append(node)            
            stack.append(node)
    return max(root.children, key=lambda child: child.alpha).state    
            
    

                

if __name__ == "__main__":
    i, j, v = -1, -1, 2
    step = 0
    chess = my_chess
    fig, ax = plt.subplots(1, 1, tight_layout=True)
    draw(ax, chess)
    plt.pause(1)
    while step < 100:
        step += 1 
        root = Node2(0, State2(i, j, v, chess))
        root.points = get_points(chess)
        state = max_min(root, 3)
        i, j, v, chess = state.i, state.j, state.v, state.chess
        s = '黑方' if v == 1 else '白方'
        print('step: %3d  %5s   (%2d,  %2d)' % (step, s, i+1, j+1))
        status = check(i, j, v, chess)
        draw(ax, chess)
        plt.pause(1)
        if status == True:
            print()
            print('############################################################')    
            print(f'{s} 在第 {step} 步胜出')
            plt.show()
            break







