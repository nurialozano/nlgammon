NLGammon is a computer implementation of backgammon in Python, with a neural network trained with reinforcement learning
and a graphical user interface.

The neural network's learning methodology mirrors the one used in TD-Gammon, a neural network developed by Gerald Tesauro
in 1992 that learned how to play backgammon by playing against itself.

In NLGammon, computer moves are chosen based on the predictions of a trained MLPRegressor from the scikit-learn machine learning library for Python.
The neural network has been trained with 700,000 instances of self-play and is saved in file final_brain_700000.txt.
The graphical user interface is developed with pygame.

To play NLGammon, run file Launch.py
