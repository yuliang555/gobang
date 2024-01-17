from enum import IntEnum
import copy
import time

class MAP_ENTRY_TYPE(IntEnum):
    MAP_EMPTY = 0,
    MAP_PLAYER_ONE = 1,
    MAP_PLAYER_TWO = 2,
    MAP_NONE = 3

class CHESS_TYPE(IntEnum):
    NONE = 0,
    SLEEP_TWO = 1,
    LIVE_TWO = 2,
    SLEEP_THREE = 3
    LIVE_THREE = 4,
    CHONG_FOUR = 5,
    LIVE_FOUR = 6,
    LIVE_FIVE = 7,
    
CHESS_TYPE_NUM = 8

FIVE = CHESS_TYPE.LIVE_FIVE.value
FOUR, THREE, TWO = CHESS_TYPE.LIVE_FOUR.value, CHESS_TYPE.LIVE_THREE.value, CHESS_TYPE.LIVE_TWO.value
SFOUR, STHREE, STWO = CHESS_TYPE.CHONG_FOUR.value, CHESS_TYPE.SLEEP_THREE.value, CHESS_TYPE.SLEEP_TWO.value
            
class Evaluate():
    def __init__(self, chess_len):
        self.len = chess_len
        self.record = [[[0,0,0,0] for i in range(chess_len)] for j in range(chess_len)]
        self.count = [[0 for i in range(CHESS_TYPE_NUM)] for j in range(CHESS_TYPE_NUM)]


    def reset(self):
        self.record = [[[0,0,0,0] for i in range(self.len)] for j in range(self.len)]
        self.count = [[0 for i in range(CHESS_TYPE_NUM)] for j in range(CHESS_TYPE_NUM)]        
        self.save_count = 0
        
    
    def evaluate(self, board, turn):
        self.reset()        
        if turn == MAP_ENTRY_TYPE.MAP_PLAYER_ONE:
            mine = 1
            opponent = 2
        else:
            mine = 2
            opponent = 1        
        for i in range(self.len):
            for j in range(self.len):
                if board[i][j] == mine:
                    self.evaluatePoint(board, i, j, mine, opponent)
                elif board[i][j] == opponent:
                    self.evaluatePoint(board, i, j, opponent, mine)        
        mine_count = self.count[mine-1]
        opponent_count = self.count[opponent-1]
        mscore, oscore = self.getScore(mine_count, opponent_count)
        return (mscore - oscore)
    
           
    def getScore(self, mine_count, opponent_count):
        mscore, oscore = 0, 0
        if mine_count[FIVE] > 0:
            return (10000, 0)
        if opponent_count[FIVE] > 0:
            return (0, 10000)
                
        if mine_count[SFOUR] >= 2:
            mine_count[FOUR] += 1
            
        if opponent_count[FOUR] > 0:
            return (0, 9050)
        if opponent_count[SFOUR] > 0:
            return (0, 9040)
        
        if mine_count[FOUR] > 0:
            return (9030, 0)
        if mine_count[SFOUR] > 0 and mine_count[THREE] > 0:
            return (9020, 0)
            
        if opponent_count[THREE] > 0 and mine_count[SFOUR] == 0:
            return (0, 9010)
            
        if (mine_count[THREE] > 1 and opponent_count[THREE] == 0 and opponent_count[STHREE] == 0):
            return (9000, 0)
        
        if mine_count[SFOUR] > 0:
            mscore += 2000

        if mine_count[THREE] > 1:
            mscore += 500
        elif mine_count[THREE] > 0:
            mscore += 100
            
        if opponent_count[THREE] > 1:
            oscore += 2000
        elif opponent_count[THREE] > 0:
            oscore += 400

        if mine_count[STHREE] > 0:
            mscore += mine_count[STHREE] * 10
        if opponent_count[STHREE] > 0:
            oscore += opponent_count[STHREE] * 10
            
        if mine_count[TWO] > 0:
            mscore += mine_count[TWO] * 4
        if opponent_count[TWO] > 0:
            oscore += opponent_count[TWO] * 4
                
        if mine_count[STWO] > 0:
            mscore += mine_count[STWO] * 4
        if opponent_count[STWO] > 0:
            oscore += opponent_count[STWO] * 4
        
        return (mscore, oscore)

   
    def evaluatePoint(self, board, i, j, mine, opponent):
        dir_offset = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for k in range(4):
            if self.record[i][j][k] == 0:
                self.analysisLine(board, i, j, k, dir_offset[k], mine, opponent, self.count[mine-1])
            else:
                self.save_count += 1
    
    
    def getLine(self, board, i, j, dir, opponent):
        line = [0 for i in range(9)]       
        tmp_i = i + (-5 * dir[0])
        tmp_j = j + (-5 * dir[1])
        for k in range(9):
            tmp_i += dir[0]
            tmp_j += dir[1]
            if (tmp_i < 0 or tmp_i >= self.len or 
                tmp_j < 0 or tmp_j >= self.len):
                line[k] = opponent
            else:
                line[k] = board[tmp_i][tmp_j]                        
        return line
   
         
    def analysisLine(self, board, i, j, dir_index, dir, mine, opponent, count):
        def setRecord(self, i, j, left, right, dir_index, dir):
            tmp_i = i + (-5 + left) * dir[0]
            tmp_j = j + (-5 + left) * dir[1]
            for _ in range(left, right):
                tmp_i += dir[0]
                tmp_j += dir[1]
                self.record[i][j][dir_index] = 1
    
        empty = MAP_ENTRY_TYPE.MAP_EMPTY.value              
        line = self.getLine(board, i, j, dir, opponent)
        
        left_idx, right_idx = 4, 4
        while right_idx < 8:
            if line[right_idx+1] != mine:
                break
            right_idx += 1
        while left_idx > 0:
            if line[left_idx-1] != mine:
                break
            left_idx -= 1
                    
        left_range, right_range = left_idx, right_idx
        while right_range < 8:
            if line[right_range+1] == opponent:
                break
            right_range += 1
        while left_range > 0:
            if line[left_range-1] == opponent:
                break
            left_range -= 1
                   
        chess_range = right_range - left_range + 1
        if chess_range < 5:
            setRecord(self, i, j, left_range, right_range, dir_index, dir)
            return CHESS_TYPE.NONE        
        setRecord(self, i, j, left_idx, right_idx, dir_index, dir)
        
        m_range = right_idx - left_idx + 1
        
        # M:mine chess, P:opponent chess or out of range, X: empty
        if m_range == 5:
            count[FIVE] += 1
        
        # Live Four : XMMMMX 
        # Chong Four : XMMMMP, PMMMMX
        if m_range == 4:
            left_empty = right_empty = False
            if line[left_idx-1] == empty:
                left_empty = True			
            if line[right_idx+1] == empty:
                right_empty = True
            if left_empty and right_empty:
                count[FOUR] += 1
            elif left_empty or right_empty:
                count[SFOUR] += 1
        
        # Chong Four : MXMMM, MMMXM, the two types can both exist
        # Live Three : XMMMXX, XXMMMX
        # Sleep Three : PMMMX, XMMMP, PXMMMXP
        if m_range == 3:
            left_empty = right_empty = False
            left_four = right_four = False
            if line[left_idx-1] == empty:
                if line[left_idx-2] == mine: # MXMMM
                    setRecord(self, i, j, left_idx-2, left_idx-1, dir_index, dir)
                    count[SFOUR] += 1
                    left_four = True
                left_empty = True
                
            if line[right_idx+1] == empty:
                if line[right_idx+2] == mine: # MMMXM
                    setRecord(self, i, j, right_idx+1, right_idx+2, dir_index, dir)
                    count[SFOUR] += 1
                    right_four = True 
                right_empty = True
            
            if left_four or right_four:
                pass
            elif left_empty and right_empty:
                if chess_range > 5: # XMMMXX, XXMMMX
                    count[THREE] += 1
                else: # PXMMMXP
                    count[STHREE] += 1
            elif left_empty or right_empty: # PMMMX, XMMMP
                count[STHREE] += 1
        
        # Chong Four: MMXMM, only check right direction
        # Live Three: XMXMMX, XMMXMX the two types can both exist
        # Sleep Three: PMXMMX, XMXMMP, PMMXMX, XMMXMP
        # Live Two: XMMX
        # Sleep Two: PMMX, XMMP
        if m_range == 2:
            left_empty = right_empty = False
            left_three = right_three = False
            if line[left_idx-1] == empty:
                if line[left_idx-2] == mine:
                    setRecord(self, i, j, left_idx-2, left_idx-1, dir_index, dir)
                    if line[left_idx-3] == empty:
                        if line[right_idx+1] == empty: # XMXMMX
                            count[THREE] += 1
                        else: # XMXMMP
                            count[STHREE] += 1
                        left_three = True
                    elif line[left_idx-3] == opponent: # PMXMMX
                        if line[right_idx+1] == empty:
                            count[STHREE] += 1
                            left_three = True
                        
                left_empty = True
                
            if line[right_idx+1] == empty:
                if line[right_idx+2] == mine:
                    if line[right_idx+3] == mine:  # MMXMM
                        setRecord(self, i, j, right_idx+1, right_idx+2, dir_index, dir)
                        count[SFOUR] += 1
                        right_three = True
                    elif line[right_idx+3] == empty:
                        #setRecord(self, x, y, right_idx+1, right_idx+2, dir_index, dir)
                        if left_empty:  # XMMXMX
                            count[THREE] += 1
                        else:  # PMMXMX
                            count[STHREE] += 1
    
    
                        right_three = True
                    elif left_empty: # XMMXMP
                        count[STHREE] += 1
                        right_three = True
                        
                right_empty = True
            
            if left_three or right_three:
                pass
            elif left_empty and right_empty: # XMMX
                count[TWO] += 1
            elif left_empty or right_empty: # PMMX, XMMP
                count[STWO] += 1
        
        # Live Two: XMXMX, XMXXMX only check right direction
        # Sleep Two: PMXMX, XMXMP
        if m_range == 1:
            left_empty = right_empty = False
            if line[left_idx-1] == empty:
                if line[left_idx-2] == mine:
                    if line[left_idx-3] == empty:
                        if line[right_idx+1] == opponent: # XMXMP
                            count[STWO] += 1
                left_empty = True

            if line[right_idx+1] == empty:
                if line[right_idx+2] == mine:
                    if line[right_idx+3] == empty:
                        if left_empty: # XMXMX
                            #setRecord(self, x, y, left_idx, right_idx+2, dir_index, dir)
                            count[TWO] += 1
                        else: # PMXMX
                            count[STWO] += 1
                elif line[right_idx+2] == empty:
                    if line[right_idx+3] == mine and line[right_idx+4] == empty: # XMXXMX
                        count[TWO] += 1
                        
        return CHESS_TYPE.NONE






if __name__ == "__main__":
    chess = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    evaluate = Evaluate(10)
    print(evaluate.evaluate(chess, 1))

