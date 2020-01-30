This code was mostly written for papers presented at AAAI-19 AICS and GameSec-19. This code can compute the min-max strategies for both the players participating in a two-player zero-sum Markov Game. As the game has a zero-sum structure, the code also give you the nash and stackelberg equilibrium of the Markov Game (which is equal to the min-max equilibirum).

*New addition:* Compute the the Nash or the Strong Stackelberg Eq. strategies for a general-sum Markov Game.

If you use this code for your research, we would appreciate if you cite our work. :)
```
@inproceedings{sengupta2019general,
  title={General Sum Markov Games for Strategic Detection of Advanced Persistent Threats using Moving Target Defense in Cloud Networks},
  author={Sengupta, Sailik and Chowdhary, Ankur and Huang, Dijiang and Kambhampati, Subbarao},
  booktitle={International Conference on Decision and Game Theory for Security},
  pages={492--512},
  year={2019},
  organization={Springer}
}
```

To run code, manuver to the appropriate folder and run `agents.py`. The set of commands that one can use to do this starting at the root folder are:
```
cd ./src/zero-sum
python agents.py
```
OR
```
cd ./src/general-sum
python agents.py
```

For using the min-max agent which computes the optimal markov game strategy for the players, you will need to have gurobi installed. Gurobi comes with a free academic license and can be installed into anaconda in 3 simple steps (see [this link](http://www.gurobi.com/documentation/8.0/quickstart_mac/installing_the_anaconda_py.html)).

Send me a mail (sailik.cse.jdvu {at} gmail {dot} com) if you are interested in collaboration.
