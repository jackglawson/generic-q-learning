from game import Game
from strategy import Strategy
from utils import animate
from settings import learning_params
import time
import pickle

start = time.time()


def save(learning_strategy, last_game):
    end = time.time()

    with open('learning_strategy.pkl', 'wb') as pickle_file:
        pickle.dump(learning_strategy, pickle_file)

    with open('last_game.pkl', 'wb') as pickle_file:
        pickle.dump(last_game, pickle_file)

    print('Time taken: {}'.format(end - start))
    print('SAVED')


strategy = Strategy(learning=True, explain=False)


try:
    for epoch in range(learning_params.num_epochs):
        # print('#################### GAME {} ##################'.format(epoch))
        game = Game(strategy)
        game.play()
        last_game = game
        if epoch % (1000) == 0:
            print('Num epochs: {}'.format(epoch))
            #print('Progress: {}%'.format(epoch/learning_params.num_epochs*100))

except:
    print('STOPPING')

save(strategy, last_game)


#animate(game.log)