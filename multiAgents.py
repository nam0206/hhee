# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        best = 0

        for x in newFood.asList() :
            best = max(best, 1 / getMazeDistance(newPos, x, currentGameState))

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore() + best

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

maze_distance = {}

def bfs(pos1, pos2, gameState):
    from collections import deque

    walls = gameState.getWalls()

    queue = deque([(pos1, 0)])

    visited = set()
    visited.add(pos1)

    while queue:
        current_pos, dist = queue.popleft()

        if current_pos == pos2:
            return dist

        x, y = current_pos

        for dx, dy in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
            next_x, next_y = x + dx, y + dy
            next_pos = (next_x, next_y)

            if not walls[next_x][next_y] and next_pos not in visited:
                visited.add(next_pos)
                queue.append((next_pos, dist + 1))

    return 99999

def getMazeDistance(pos1, pos2, gameState):
    pair_key = tuple(sorted((pos1, pos2)))

    if pair_key in maze_distance:
        return maze_distance[pair_key]

    dist = bfs(pos1, pos2, gameState)

    maze_distance[pair_key] = dist

    return dist

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

        global maze_distance
        maze_distance.clear()


import time

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
        Here are some method calls that might be useful when implementing minimax.
        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1
        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action
        gameState.getNumAgents():
        Returns the total number of agents in the game
        gameState.isWin():
        Returns whether or not the game state is a winning state
        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def minimax(state, agentIndex, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            legalActions = state.getLegalActions(agentIndex)
            numAgents = state.getNumAgents()
            nextAgent = (agentIndex + 1) % numAgents

            nextDepth = depth + 1 if nextAgent == 0 else depth

            if agentIndex == 0:
                max_score = float('-inf')
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    score = minimax(successor, nextAgent, nextDepth)
                    max_score = max(max_score, score)
                return max_score

            else:
                min_score = float('inf')
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    score = minimax(successor, nextAgent, nextDepth)
                    min_score = min(min_score, score)

                return min_score

        legalActions = gameState.getLegalActions(0)
        best_action = legalActions[0]
        best_score = -float('inf')

        for action in legalActions:
            last_state = gameState.generateSuccessor(0, action)
            score = minimax(last_state, 1, 0)
            if score > best_score :
                best_action = action
                best_score = score

        return best_action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def minimax(state, agentIndex, depth, alpha, beta):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            numAgents = state.getNumAgents()
            next_agent = (agentIndex + 1) % numAgents
            next_depth = depth + 1 if next_agent == 0 else depth

            legalActions = state.getLegalActions(agentIndex)

            if agentIndex == 0:
                max_score = float('-inf')
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    score = minimax(successor, next_agent, next_depth, alpha, beta)
                    max_score = max(score, max_score)
                    if max_score > beta: break
                    alpha = max(alpha, score)

                return max_score
            else :
                min_score = float('inf')
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    score = minimax(successor, next_agent, next_depth, alpha, beta)
                    min_score = min(score, min_score)
                    if alpha > min_score: break
                    beta = min(beta, score)

                return min_score

        alpha = float('-inf')
        beta = float('inf')
        legalActions = gameState.getLegalActions(0)
        best_action = legalActions[0]
        best_score = -float('inf')

        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            score = minimax(successor, 1, 0, alpha, beta)

            if score > best_score:
                best_score = score
                best_action = action

            alpha = max(alpha, best_score)

        return best_action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        def expectimax(state, agentIndex, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            legalActions = state.getLegalActions(agentIndex)
            numAgents = state.getNumAgents()
            nextAgent = (agentIndex + 1) % numAgents

            nextDepth = depth + 1 if nextAgent == 0 else depth

            if agentIndex == 0:
                max_score = float('-inf')
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    score = expectimax(successor, nextAgent, nextDepth)
                    max_score = max(max_score, score)
                return max_score

            else:
                total = 0
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    score = expectimax(successor, nextAgent, nextDepth)
                    total += score
                return total / len(legalActions)

        legalActions = gameState.getLegalActions(0)
        best_action = legalActions[0]
        best_score = -float('inf')

        numAgents = gameState.getNumAgents()
        next_agent = 1 % numAgents
        start_depth = 1 if next_agent == 0 else 0


        for action in legalActions :
            last_state = gameState.generateSuccessor(0, action)
            score = expectimax(last_state, next_agent, start_depth)
            if score > best_score :
                best_action = action
                best_score = score

        return best_action


def betterEvaluationFunction(currentGameState: GameState):
    pos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()

    score = currentGameState.getScore()

    if len(foodList) > 0:
        min_food_dist = min([getMazeDistance(pos, food, currentGameState) for food in foodList])
        score -= min_food_dist

    score -= 20 * len(foodList)

    tmp = 0

    for ghost in ghostStates:
        ghost_dist = getMazeDistance(pos, ghost.getPosition(), currentGameState)

        if ghost.scaredTimer == 0:
            if ghost_dist <= 1:
                return float("-inf")

        elif ghost.scaredTimer > 0:
            if ghost_dist > 0:
                tmp = max(tmp, 222.0 / ghost_dist)
    return score + tmp

# Abbreviation
better = betterEvaluationFunction
