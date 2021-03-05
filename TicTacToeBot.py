from enum import Enum
class Evaluation(Enum):
    WIN = 1
    DRAW = 0
    LOSS = -1

# class Player(Enum):
#     PLAYER_X = 1
#     PLAYER_O = 2
#     NO_ONE = 0

# X goes first, then O


class TicTacToeBot(object):
    def __init__(self):
        self.evaluated = {}

    def bestMove(self,state):
        if state in self.evaluated:
            return self.evaluated[state][1]
        return self.evaluate(state)[1]
    
    def evaluate(self,state):
        if state in self.evaluated:
            return self.evaluated[state]

        options = self.getAvailableSquares(state)
        player = 1 if (len(options) % 2 == 1) else 2
        winner = self.findWinner(state)

        # check first if theres a win/loss
        if winner != 0:
            # print(winner,player)
            evaluation = Evaluation.WIN if winner == player else Evaluation.LOSS
            self.evaluated[state] = (evaluation,-1)
            return (evaluation,-1)
        
        # if nothing left, then must be a draw
        if len(options) == 0:
            self.evaluated[state] = (Evaluation.DRAW, -1)
            return (Evaluation.DRAW, -1)

        
        for opt in options:
            newState = state + player*(3**(8-opt))
            self.evaluate(newState)

        #     

        # check child states
        # print(self.stateToGrid(state), 'has children:')
        # bestOption = options[0]
        # bestEval = Evaluation.LOSS
        drawFound = -1
        for opt in options:
            newState = state + player*(3**(8-opt))
            evaluation = self.evaluate(newState)[0]
            # print(f'{opt}:      ', self.stateToGrid(newState),'   ',evaluation)
            if evaluation == Evaluation.LOSS:
                self.evaluated[state] = (Evaluation.WIN,opt)
                # print("       Therefore I am a WIN")
                return (Evaluation.WIN,opt)
            elif evaluation == Evaluation.DRAW:
                drawFound = opt

        if drawFound != -1:
            self.evaluated[state] = (Evaluation.DRAW,drawFound)
        else:
            self.evaluated[state] = (Evaluation.LOSS,options[0])
        return self.evaluated[state]
            #     bestEval, bestOption = evaluation, opt

            # if evaluation == Evaluation.WIN:
            #     self.evaluated[state] = (Evaluation.LOSS,opt)
            #     print("     This is a loss")
            #     return (Evaluation.LOSS,opt)
            # elif evaluation == Evaluation.DRAW:
            #     drawFound = opt
        
        # print("      Giving back",bestEval,bestOption)
        # self.evaluated[state] = (bestEval,bestOption)
        # return (bestEval,bestOption)

        # lossFound = False
        # for opt in options:
        #     newState = state + player*(3**(8-opt))
        #     evaluation = self.evaluate(newState)[0]
        #     print(f'{opt}:      ', self.stateToGrid(newState),'   ',evaluation)
        #     if evaluation == Evaluation.LOSS:
        #         self.evaluated[state] = (Evaluation.WIN,opt)
        #         print("       Therefore I am a WIN")
        #         return (Evaluation.WIN,opt)
        #     elif evaluation == Evaluation.WIN:
        #         lossFound = True
        
        # # print("      Giving back",bestEval,bestOption)
        # # self.evaluated[state] = (bestEval,bestOption)
        # if drawFound != -1:
        #     self.evaluated[state] = (Evaluation.DRAW,drawFound)
        #     print("     This is a draw")
        # else:
        #     self.evaluated[state] = (Evaluation.WIN,options[0])
        #     print("     This is a win")
        # return self.evaluated[state]

    def groupAllSame(self,grid,cells):
        return all(grid[cells[0]]==grid[c] for c in cells) and grid[cells[0]] != 0

    def findWinner(self,state):
        grid = self.stateToGrid(state)
        for i in range(3):
            if self.groupAllSame(grid,[3*i,3*i+1,3*i+2]): return grid[3*i]
        for i in range(3):
            if self.groupAllSame(grid,[i,i+3,i+6]): return grid[i]
        if self.groupAllSame(grid,[0,4,8]): return grid[0]
        if self.groupAllSame(grid,[2,4,6]): return grid[2]
        return 0

    def getAvailableSquares(self,state):
        # convert state (ternary form) into string
        curr = state
        available = []
        for i in range(9):
            if curr % 3 == 0:
                available.append(8-i)
            curr = curr // 3
        return available

    def stringToState(self,string):
        state = 0
        for i in range(9):
            if string[i] == 'X':
                state = 3 * state + 1
            elif string[i] == 'O':
                state = 3 * state + 2
            else:
                state = 3 * state
        return state

    def gridToState(self,grid):
        state = 0
        for cell in grid:
            state = 3 * state + cell
        return state

    # returns in a single row of 9
    def stateToGrid(self,state):
        grid = []
        curr = state
        for _ in range(9):
            grid.insert(0,curr % 3)
            curr = curr // 3
        return grid

    def pprint(self,state):
        grid = self.stateToGrid(state)
        for i in range(3):
            print(grid[3*i:3*i+3])

class TicTacToeGame(object):
    def __init__(self):
        self.bot = TicTacToeBot()
        self.state = 0

    def play(self):
        for _ in range(5):
            move = int(input("Your move: "))
            self.state += 3**(8-move)

            self.bot.pprint(self.state)

            if self.bot.findWinner(self.state) != 0:
                print("You win")
                break

            print("")

            botMove = self.bot.bestMove(self.state)
            if botMove == -1:
                print("Draw")
                break
            self.state += 2*(3**(8-botMove))
            self.bot.pprint(self.state)

            if self.bot.findWinner(self.state) != 0:
                print("Bot wins")
                break



    def printState(self):
        bot.pprint(self.state)
    
bot = TicTacToeBot()
# print(bot.evaluate(bot.gridToState([0, 0, 2, 1, 1, 2, 1, 0, 2])))
# print(newState)
# print(bot.getAvailableSquares(newState))
# print("FINAL:",bot.evaluate(newState))
# print(bot.stateToGrid(1))
# print(bot.evaluated)
# for k,v in bot.evaluated.items():
#     bot.pprint(k)
#     print("Evaluation",v)

game = TicTacToeGame()
game.play()


