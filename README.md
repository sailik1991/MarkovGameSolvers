## About this code-base

This code was mostly written for papers presented at AAAI-19 AICS and GameSec-19. This code can compute the min-max strategies for both the players participating in a two-player zero-sum Markov Game. As the game has a zero-sum structure, the code also give you the nash and stackelberg equilibrium of the Markov Game (which is equal to the min-max equilibirum).

**New addition:** Compute the the Nash or the Strong Stackelberg Eq. strategies for a general-sum Markov Game.

## Installation

You can install the package and its dependencies using pip:

```bash
pip install -r requirements.txt
```

Or install directly from the repository:

```bash
pip install .
```

## How to use it

After installation, you can import and use the package as follows:

```python
# For zero-sum games
from MarkovGameSolvers.zero_sum.agents import UniformRandom, OptimalMixed
agent = UniformRandom()
# or
agent = OptimalMixed()

# For general-sum games
from MarkovGameSolvers.general_sum.agents import UniformRandom, NashEq, StackelbergEq
agent = UniformRandom()
# or
agent = NashEq()
# or
agent = StackelbergEq()
```

You can also run the main functions directly:

```bash
# For zero-sum games
python -c "from MarkovGameSolvers.zero_sum.agents import main; main()"

# For general-sum games
python -c "from MarkovGameSolvers.general_sum.agents import main; main()"
```

This implementation uses PuLP as an open-source alternative to Gurobi for solving optimization problems. The original implementation required Gurobi, which is a commercial solver (though it offers a free academic license).

## Considerations if it helps you

If you use this for code for your research, we would appreciate if you cite our work. :)
+ Zero-sum
```
@article{chowdhary2018markov,
  title={Markov game modeling of moving target defense for strategic detection of threats in cloud networks},
  author={Chowdhary, Ankur and Sengupta, Sailik and Huang, Dijiang and Kambhampati, Subbarao},
  journal={AAAI Workshop on Artificial Intelligence for Cyber Security (AICS)},
  year={2019}
}
```
+ General-sum
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

## Contact

If you are interested in collaboration/clarification or feel there is a correction that needs to be made, please send me a email at `sailik.cse.jdvu {at} gmail {dot} com`.
