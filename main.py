import matplotlib.pyplot as plt



from gobang import draw, check, get_points, my_chess
from mcts import mcts, Node1, State1
from max_min import max_min, Node2, State2





if __name__ == "__main__":
    i, j, v = -1, -1, 2
    step = 0
    chess = my_chess
    fig, ax = plt.subplots(1, 1, tight_layout=True)
    draw(ax, chess)
    plt.pause(1)
    while step < 100:
        step += 1    
        if v == 2:
            pre_state = State1(i, j, v, chess)
            state = mcts(Node1(pre_state), 500)
            i, j, v, chess = state.i, state.j, state.v, state.chess
        else:
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



