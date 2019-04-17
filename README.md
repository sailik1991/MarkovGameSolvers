This code was mostly written for the paper _Markov Game Modeling of Moving Target Defense for Strategic Detection of Threats in Cloud Networks_. This code can compute the min-max strategies for both the players participating in a two-player zero-sum Markov Game. As the game has a zero-sum structure, the code also give you the nash and stackelberg equilibrium of the Markov Game (which is equal to the min-max equilibirum).

If you use this code for your research, we would really appreciate if you cite our work. :)
```
@article{chowdhary2018markov,
  title={Markov Game Modeling of Moving Target Defense for Strategic Detection of Threats in Cloud Networks},
  author={Chowdhary, Ankur and Sengupta, Sailik and Huang, Dijiang and Kambhampati, Subbarao},
  journal={arXiv preprint arXiv:1812.09660},
  year={2018}
}
```

Either way, to run code, manuver to the appropriate folder and run `agents.py`. The set of commands that one can use to do this starting at the root folder are:
```
cd ./src/zero-sum
python agents.py
```

For using the min-max agent which computes the optimal markov game strategy for the players, you will need to have gurobi installed. Gurobi comes with a free academic license and can be installed into anaconda in 3 simple steps (see [this link](http://www.gurobi.com/documentation/8.0/quickstart_mac/installing_the_anaconda_py.html)).

Send me a mail for collaboration. Use the `test.py` script in each folder to ensure that newly added code does not break the existing code.
