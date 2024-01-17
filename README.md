# <a name="_toc30313"></a><a name="_toc18589"></a>**智能五子棋**

## <a name="_toc23612"></a><a name="_toc28316"></a>**一、实验任务**

1 编写程序实现蒙特卡洛树搜索算法，作为五子棋的下棋算法

2 编写程序实现极大极小+α-β 剪枝算法，作为五子棋的下棋算法

3 将两种算法进行博弈对抗，并实现下棋过程的可视化

## <a name="_toc2271"></a>**二、文件描述**

**gobang.py：实现棋盘可视化**

--draw(ax, chess)：显示当前棋盘

--check(i, j, v, chess)：在(i, j)处落子 v 形成棋盘 chess 后，判断 v 是否赢棋

**mcts.py：蒙特卡洛树搜索算法**

--elect(node)：选择

--expand(node)：扩展

--rollout(state, root)：模拟

--backword(node, value)：回溯

--mcts(root, max_iteration)：算法实现

**max_min.py：极大极小法+α-β 剪枝**

**evaluate.py：极大极小法中使用的估价函数**

**main.py：两种算法对弈**

## <a name="_toc25648"></a>**三、运行示例** 
黑方：蒙特卡洛树搜索算法    
白方：极大极小+α-β剪枝算法   
<img src='https://github.com/yuliang555/gobang/blob/master/images/%E5%9B%BE%E7%89%878-1.png' width=33%>
<img src='https://github.com/yuliang555/gobang/blob/master/images/%E5%9B%BE%E7%89%878-2.png' width=33%>
<img src='https://github.com/yuliang555/gobang/blob/master/images/%E5%9B%BE%E7%89%878-3.png' width=33%>

