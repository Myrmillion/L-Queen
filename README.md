<div align="justify">

# Context

This project has been realized as part of ParaDis, a class dedicated to Parallel and Distributed computing from the MSE (Master of Science in Ingenieering) from the HES-SO.

# Goal

The app built during the project is dedicated to solving a generalized version of the [**eight queens puzzle**](https://en.wikipedia.org/wiki/Eight_queens_puzzle) problem. Instead of solving for an `8×8` grid only the app solves for an `L×L` grid where `L` is also the number of queens on the board.

The underlying goal is to use parallelization and distribution techniques, to solve the problem with as many queens as possible in less than 10 minutes.

More information in the `paradis2021-8.pdf` file at the root of the project.

# To run the app

Use the following command :

```
mpirun --use-hwthread-cpus -np 20 python3 ./n-queen_REGULAR-PARALLEL.py
```

</div>
