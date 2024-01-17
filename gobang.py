import numpy as np
import random
import matplotlib.pyplot as plt


shape = 10
win = 5
my_chess = [[0 for i in range(shape)] for j in range(shape)]



def draw(ax, chess):
    """
    显示当前棋盘
    """    
    ax.clear()
    ax.set_xticks(np.arange(0.5, shape-1, step=1))
    ax.set_xticklabels([])
    ax.set_yticks(np.arange(0.5, shape-1, step=1))
    ax.set_yticklabels([])
    ax.grid(True)
    
    ax.imshow([[1 for i in range(shape)] for j in range(shape)], interpolation='none', cmap='PuOr')
    for i in range(shape):
        for j in range(shape):
            if chess[i][j] == 1:
                ax.plot(j, i, color='black', marker='o', markersize=23)
            elif chess[i][j] == 2:
                ax.plot(j, i, color='white', marker='o', markersize=23)
    ax.get_figure().canvas.draw()

        
def check(i, j, v, chess):
    """
    在(i, j)处落子v形成棋盘chess后，判断v是否赢棋
    """
    row = 1
    pre_i, next_i = i - 1, i + 1
    while pre_i >= 0:
        if chess[pre_i][j] == v:
            row += 1
            pre_i -= 1
        else:
            break
    while next_i <= shape - 1:
        if chess[next_i][j] == v:
            row += 1
            next_i += 1
        else:
            break
    if row >= win:
        return True
    col = 1
    pre_j, next_j = j - 1, j + 1
    while pre_j >= 0:
        if chess[i][pre_j] == v:
            col += 1
            pre_j -= 1
        else:
            break
    while next_j <= shape - 1:
        if chess[i][next_j] == v:
            col += 1
            next_j += 1
        else:
            break
    if col >= win:
        return True
    dia_right = 1
    pre_i, next_i, pre_j, next_j = i - 1, i + 1, j - 1, j + 1
    while pre_i >= 0 and pre_j >= 0:
        if chess[pre_i][pre_j] == v:
            dia_right += 1
            pre_i -= 1
            pre_j -= 1
        else:
            break
    while next_i <= shape - 1 and next_j <= shape - 1:
        if chess[next_i][next_j] == v:
            dia_right += 1
            next_i += 1
            next_j += 1
        else:
            break
    if dia_right >= win:
        return True
    dia_left = 1
    pre_i, next_i, pre_j, next_j = i + 1, i - 1, j - 1, j + 1
    while pre_i <= shape - 1 and pre_j >= 0:
        if chess[pre_i][pre_j] == v:
            dia_left += 1
            pre_i += 1
            pre_j -= 1
        else:
            break
    while next_i >= 0 and next_j <= shape - 1:
        if chess[next_i][next_j] == v:
            dia_left += 1
            next_i -= 1
            next_j += 1
        else:
            break
    if dia_left >= win:
        return True
    return False 
         

def hasNeighbor(i, j, chess):
    for row in range(i-1, i+2):
        for col in range(j-1, j+2):
            if row >= 0 and row < shape and col >=0 and col < shape:
                if chess[row][col] != 0:
                    return True
    return False 


def get_points(chess):
    """
    返回当前棋盘chess下所有空的并且有邻子的落子点
    """
    points = []
    half = shape // 2
    for i in range(shape):
        for j in range(shape):
           if chess[i][j] == 0 and hasNeighbor(i, j, chess):
               dis = abs(half - i) + abs(half - j)
               point = [dis, i, j]
               points.append(point)
    if points == []:
        return [[0, half, half]]
    points.sort(reverse=True)
    return points    


# def line(v_max, v_min, list):
#     score = 0
#     if len(list) >= 5:
#         count1, count2 = 0, 0
#         for item in list:
#             count1 += 1
#             if item == v_max:
#                 count2 += 1
#             elif item == v_min:
#                 if count1 > 5:
#                     score += count2
#                 count1, count2 = 0, 0
#     return score


# def evaluation(v, chess):
#     shape = len(chess)
#     v_max, v_min = v, v % 2 + 1
#     score_max, score_min = 0, 0
#     for i in range(shape):
#         list1 = chess[i]
#         list2 = [chess[j][i] for j in range(shape)]
#         list3 = [chess[j][i-j] for j in range(i+1)]
#         list4 = [chess[j][shape-i-1+j] for j in range(i+1)]
#         score_max += line(v_max, v_min, list1)
#         score_max += line(v_max, v_min, list2)
#         score_max += line(v_max, v_min, list3)
#         score_max += line(v_max, v_min, list4)
#         score_min += line(v_min, v_max, list1)
#         score_min += line(v_min, v_max, list2)
#         score_min += line(v_min, v_max, list3)
#         score_min += line(v_min, v_max, list4)
#         print(score_max, score_min)
#     return score_max - score_min


        
        
        

if __name__ == "__main__":
    v = 1
    step = 0
    chess = my_chess
    fig, ax = plt.subplots(1, 1, tight_layout=True)
    draw(ax, chess)
    plt.pause(3)
    while step < 100:
        step += 1
        s = '黑方' if v == 1 else '白方'
        point = random.choice(get_points(chess))
        i, j = point[0], point[1]
        chess[i][j] = v
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
        v = v % 2 + 1


