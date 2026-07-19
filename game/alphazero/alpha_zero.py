from loguru import logger
import numpy as np
from copy import deepcopy
from tqdm import tqdm
import random
import torch
import torch.nn.functional as F

from alphazero.model import Model
from alphazero.alpha_mcts import AMCTS
from alphazero.state import State
from alphazero.alpha_constants import *

class AlphaZero():
    """Class that combines the NN model and MCTS in selfplaying and traning."""
    def __init__(self,model:Model,optimizer:torch.optim.Optimizer):
        self.model:Model = model
        self.mcts:AMCTS = AMCTS(model=model)
        self.board:list = DEFAULT_BOARD
        self.optimizer = optimizer

    def selfplay(self)->list[tuple]:
        """
        Plays with itself once. Returns list of tuples in the form
        (board,\pi values, move choosen, result) for all the states of the
        game.
        """

        game_memory = []
        player = 1
        node = State(board = DEFAULT_BOARD,player=player,move = None,parent=None)
        turn = 0  
        passed = 0
        while not node.is_game_over():
            turn+=1

            if turn >100:
                logger.error(f'hra je ve stavu \n{node} a trva vic nez 100 tahu')
                break

            #no moves so skipping the turn
            poss_moves = node.poss_moves[node.player]
            if passed ==2:
                break

            if not np.any(poss_moves):
                passed +=1
                new_node=State(board=deepcopy(node.board),player=-node.player,parent=node,move=np.zeros(64))   # pass the turn
                node = new_node
                continue # tahy kdy nema na vyber nemusime ucit
            else:
                passed = 0
            new_node,probs = self.mcts.choose_move(node)
            game_memory.append((node.board,probs,new_node.move,node.player)) 
            poss_moves = new_node.poss_moves[new_node.player]

            node = new_node


        winner = node.determine_winner()
        for i in range(len(game_memory)):
            game_memory[i] = (game_memory[0],game_memory[1],game_memory[2],game_memory[3]*winner)
            # pokud vyhral ten stejny hrac jako byl na tahu 

        return game_memory



    def train(self,examples:list):
        """ Back propagates the losses calculated from examples and the
        predictions. """
        random.shuffle(examples)

        for batch_index in range(0,len(examples),BATCH_SIZE):
            batch_end = min(len(examples)-1,batch_index+BATCH_SIZE)
            batch_samples = examples[batch_index:batch_end]


            boards,probs,moves,winner = zip(*batch_samples)
            
            logger.info(f'boardy maji tvar {np.array(boards).shape}')
            boards = torch.tensor(boards[:, 1:3, :], dtype=torch.float32)
            with torch.inference_mode():
                out_policies, out_values = self.model(boards)
                out_policies = torch.softmax(out_policies[0],0,dtype=torch.float32).cpu().numpy()
                out_values = out_values.item()

            policy_targets = torch.tensor(
                probs, dtype=torch.float32, device=self.model.device
            )
            value_target = torch.tensor(
                winner, dtype=torch.float32, device=self.model.device
            )

            policy_loss = F.cross_entropy(out_policies, policy_targets)
            value_loss = F.mse_loss(out_values, value_target)
            loss = policy_loss + value_loss

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

        print(len(examples))

    def learn(self):
        """ Runs all the iterations. Each iteration produces a lot of examples
        by selfplay and then runs all the epochs of training on them."""
        for iteration in range(ITERATIONS):
            logger.info(f'----- iterace {iteration} ----')
            examples = []
            print(examples)
            for _ in tqdm(range(SELFPLAY_ITER)):
                examples.extend(self.selfplay())

            for _ in range(EPOCH_NUM):
                self.train(examples)

            torch.save(self.model.state_dict(), f"model_{iteration}.pt")
            torch.save(self.optimizer.state_dict(), f"optimizer_{iteration}.pt")

