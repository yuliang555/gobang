import math
import matplotlib.pyplot as plt
import random
import copy

from gobang import draw, check, get_points, my_chess



class Node1():
    """
    搜索树结点
    """
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0


class State1():
    """
    状态定义：在(i, j)处落子v形成棋盘chess
    """
    def __init__(self, i, j, v, chess):
        self.i = i
        self.j = j
        self.v = v
        self.chess = chess


def select(node):
    """
    选择
    """
    exploration_factor = 0.5  # 调整探索因子
    selected_child = max(node.children, key=lambda child: (child.value / (child.visits + 1e-6)) +
                                                             exploration_factor * math.sqrt(math.log(node.visits + 1) / (child.visits + 1e-6)))
    return selected_child


def expand(node):
    """
    扩展
    """
    v = node.state.v % 2 + 1
    points = get_points(node.state.chess)
    for point in points:
        i, j = point[1], point[2]              
        chess = copy.deepcopy(node.state.chess)
        chess[i][j] = v               
        state = State1(i, j, v, chess)
        child = Node1(state, node)
        node.children.append(child)
        if check(i, j, v, chess):
            node.children = node.children[-1:]
            break
               

def rollout(state, root):
    """
    模拟
    """
    i, j, v = state.i, state.j, state.v
    chess = copy.deepcopy(state.chess)
    points = get_points(chess)
    while True:        
        if check(i, j, v, chess):
            if v == root.state.v:
                return -1
            else:
                return 1
        if points == []:
            return 0
        point = random.choice(points)
        i, j = point[1], point[2]
        v = v % 2 +1
        chess[i][j] = v
        points = get_points(chess)
        

def backword(node, value):
    """
    回溯
    """
    while node:
        node.visits += 1
        node.value += value
        node = node.parent
        
        
def mcts(root, max_iteration):
    for iteration in range(max_iteration):       
        current_node = root
        while current_node.children != []:
            current_node = select(current_node)
        if current_node == root or current_node.visits != 0:
            expand(current_node)
            current_node = current_node.children[0]
        value = rollout(current_node.state, root)
        backword(current_node, value)
    return max(root.children, key=lambda child: child.value).state
            



if __name__ == "__main__":
    i, j, v = -1, -1, 2
    step = 0
    chess = my_chess
    fig, ax = plt.subplots(1, 1, tight_layout=True)
    draw(ax, chess)
    plt.pause(1)
    while step < 100:
        step += 1
        pre_state = State1(i, j, v, chess)
        state = mcts(Node1(pre_state), 1000)
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
    


