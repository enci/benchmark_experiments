<p align="center">
  <img height="300px" src="images/logo.png"/>
</p>
<h1 align="center">
PCG Benchmark Experiments
</h1>

This repo for the experiments from our paper ["The Procedural Content Generation Benchmark: An Open-source Testbed for Generative Challenges in Games"]() that uses and test the [PCG Benchmark](https://github.com/amidos2006/pcg_benchmark). To cite the framework or the paper use the following bibliography
```
@inproceedings{khalifa20XXpcgbenchmark,
  title={PCG Benchamrk},
  author={Khalifa, Ahmed .....}
}
```

## Installation
1. Clone this repo to your local machine.
2. Install the requirements using the following command `pip install -r requirements.txt`.
3. If everything goes fine, you are ready to run the experiments or expand on them. Please check the following sections for that.

## Supported Generators
In the paper, we explored 3 different search based generators:
- [Random Search (`random`)](generators/random.py): Every generation, a new population of individuals is randomly created and evaluated. The new population is combined with the previous generation, and the best N individuals are kept for this generation.
- [μ + λ Evolution Strategy (`es`)](generators/es.py): Every generation, a new population of λ is mutated from the previous generation and evaluated, with the best μ individuals kept between generations. Candidates are evolved using a uniform mutation rate. 
- [Genetic Algorithm (`ga`)](generators/ga.py): This method expands on the ES method by introducing selection and crossover operators. We use tournament selection on T individuals to select candidates that produce new offspring. One-point crossover is used to combine parents, with a crossover rate. This method uses the same uniform mutation as ES. The population size is fixed and elitism preserves the best top solutions between generations.

## Using The Generator Runner
This section talks about using [`run.py`](run.py) to run one of the generators in the [`generators`](generators/) folder. The `run.py` is designed to run interactive generators and save the data between these iterations. The script takes a couple of parameters and then runs the generator and saves all the details of the run in folders on your hard drive. The parameters are:
- `outputfolder`: This is the only **mandatory** input for the script. It specifies the folder that the outputs should be saved inside.
- `--problem`|`-p`: The problem name that you want to run the generator against. Look at all the problem names in [Problems section](#problems) for that. The default value for this parameter is `binary-v0`
- `--generator`|`-g`: The file name where the generator is saved in. Right now there are three files for three different generators. [`random`](generators/random.py) contains a Random Search algorithm, [`es`](generators/es.py) contains a Mu + Lambda evolution Strategy, and [`ga`](generators/ga.py) contains a Genetic algorithm. The default value for this parameter is `random`.
- `--steps`|`-s`: The number of iterations to run the generator [`update`](generators/generator.py#L12) function for.
- `--earlystop`|`-e`: If this exists in the command line, the generator will stop as soon as the best solution is the maximum which is 1.0.

If you wanna set some of the algorithm hyperparameters for the available algorithm such as the fitness function used in the search process. You can in the command line the parameter name in the form of `fitness` or `--fitness` and then follow by the allowed values. For the fitness function, we have 3 different ones: 
- [`quality`|`fitness_quality`](generators/search.py#L132) computes the quality metric for the content and returns it as fitness. 
- [`quality_control`|`fitness_quality_control`](generators/search.py#L135) computes the quality metric then control if you passed the quality as cascaded fitness. 
- [`quality_control_diversity`|`fitness_quality_control_diversity`](generators/search.py#L141) computes the quality then controllability then diversity in cascaded manner as fitness, this fitness is not stable because diversity depends on the population and how diverse it is so the value of a chromosome from before that passes diversity might not pass it now.

Every parameter has a default value for example the fitness default is `quality`.

Here is an example of running a Genetic Algorithm to try to solve [`sokoban-v0`](pcg_benchmark/probs/sokoban) problem with a fitness that cares about quality and controllability and number of generations/iterations of 1000. If at any time the algorithm finds a solution, it will stop before reaching 1000 iterations.
```bash
python run.py outputs -p sokoban-v0 -g ga -s 1000 -e --fitness quality_control
```

Finally, before you start, look in the reset function for every generator to know the names of its hyperparameters if you want to tune them to a specific value. For example, `ga` has `pop_size`|`--pop_size` parameter to set the size of the population of the genetic algorithm.

## Adding a new Generator to `run.py`
This section will talk about how to integrate your generator to work with `run.py` (the generator runner). To add your new generator such that you can just use `run.py`, you need to make sure that your generator implements the `generators.utils.Generator` class. This involves making sure the constructor only needs one input `env`. Besides the constructor, you need to implement the following functions:
- `reset(self, **kwargs)`: this function initializes your generator to do a new run at any moment. Each algorithm also has hyperparameters that are being set here using kwargs. For example, all the algorithms have `seed` to seed the random number generator.
- `update(self)`: this function updates the current state of the generator to generate the next state. In evolution, it is the next generation. In cellular automata/NCA, it is the next update from its current state. In PCGRL, it is the next update of the map from its current state. In GANs, it could just produce a new one and that is it.
- `best(self)`: this function returns the evaluation of the solution so far where the value should be bounded between 0 and 1 where 1 means it solved the problem.
- `save(self, foldername)`: saves the state of the generator in a specific folder (`foldername`) so you can analyze the results and load it to continue later.
- `load(self, foldername)`: loads the state of the generator from the specific folder (`foldername`) so you can continue the update or generation later.

You can always have access to the parent class variables:
- `self._env`: access to the problem environment so you can call functions to evaluate the content
- `self._random`: a `numpy` random variable that can be used to sample random stuff.

One last note, if you decide to build a search algorithm you can build on top of `generators.search.Generator` which is the base class of all the search base ones. It has a definition for `Chromosome` class and the `Generator` base class has access to `self._chromosomes` and `self._fitness_fn` for the fitness function. The fitness function is set from the ones in the same file. These are the ones that are defined: 
- `quality(self)`: return a value between 0 and 1 where 1 means it has solved the problem from quality perspective
- `controlability(self)`: return a value between 0 and 1 where 1 means it has solved the problem from a controllability perspective. In our generators, we assign a control parameter to each chromosome to evaluate.
- `diversity(self)`: return a value between 0 and 1 where 1 means it is very different from all the other chromosomes that are surrounding it. In our generators, we calculate the diversity between all the individuals in the population during evolution.

If you want to have your new fitness function just add it in the same module `generators.search` and the system will access it using the name when provided in the command line.

## Examples of Generated Content
These are some examples of the generated content for every environment in the framework, for the optimization algorithm more details can be found about them in the paper or by checking [`generators.es`](generators/es.py) and [`generators.ga`](generators/ga.py). Random here is just sampling randomly from the space. If you need to check more examples please check the [images](images/) folder.

| Name | Random | Evolution Strategy | Genetic Algorithm |
| ---- | ------ | ------------------ | ----------------- |
| `arcade-v0` | ![Random](images/arcaderules/random_1.png) | ![Evolution Strategy](images/arcaderules/es_1.png) | ![Genetic Algorithm](images/arcaderules/ga_1.png) |
| `binary-v0` | ![Random](images/binary/random_1.png) | ![Evolution Strategy](images/binary/es_1.png) | ![Genetic Algorithm](images/binary/ga_1.png) |
| `building-v0` | ![Random](images/building/random_1.png) | ![Evolution Strategy](images/building/es_1.png) | ![Genetic Algorithm](images/building/ga_1.png) |
| `ddave-v0` | ![Random](images/ddave/random_1.png) | ![Evolution Strategy](images/ddave/es_1.png) | ![Genetic Algorithm](images/ddave/ga_1.png) |
| `elimination-v0` | ![Random](images/elimination/random_1.png) | ![Evolution Strategy](images/elimination/es_1.png) | ![Genetic Algorithm](images/elimination/ga_1.png) |
| `isaac-v0` | ![Random](images/isaac/random_1.png) | ![Evolution Strategy](images/isaac/es_1.png) | ![Genetic Algorithm](images/isaac/ga_1.png) |
| `loderunner-v0` | ![Random](images/loderunner/random_1.png) | ![Evolution Strategy](images/loderunner/es_1.png) | ![Genetic Algorithm](images/loderunner/ga_1.png) |
| `mdungeons-v0` | ![Random](images/mdungeons/random_1.png) | ![Evolution Strategy](images/mdungeons/es_1.png) | ![Genetic Algorithm](images/mdungeons/ga_1.png) |
| `smb-v0` | ![Random](images/smb/random_1.png) | ![Evolution Strategy](images/smb/es_1.png) | ![Genetic Algorithm](images/smb/ga_1.png) |
| `sokoban-v0` | ![Random](images/sokoban/random_1.png) | ![Evolution Strategy](images/sokoban/es_1.png) | ![Genetic Algorithm](images/sokoban/ga_1.png) |
| `talakat-v0` | ![Random](images/talakat/random_1.gif) | ![Evolution Strategy](images/talakat/es_1.gif) | ![Genetic Algorithm](images/talakat/ga_1.gif) |
| `zelda-v0` | ![Random](images/zelda/random_1.png) | ![Evolution Strategy](images/zelda/es_1.png) | ![Genetic Algorithm](images/zelda/ga_1.png) |

## Processing results
You can quickly run and then evaluate your results, plotting the relevant graphs using `run_experiments.bat` and `data_processing.py`, provided in this repo but not included in the library itself.
These are ready-made scripts, but you can run the experiments in any other way you want. Once experiments are over, you can process the results via
```bash
python data_processing.py run_pipeline --root_dir="./results" --output_dir='./plots'
```
You can also just execute single steps of the pipeline (`process_environment`, `process_all_envs`, `aggregate_envs_statistics`, `aggregate_over_runs`, and `plot`) by changing `run_pipeline` with the corresponding function (and using the corresponding parameters).

## Special Thanks
Thanks to Kenny for creating [1-Bit Pack](https://kenney.nl/assets/1-bit-pack) which was used for most of the 12 problems in the benchmark. Even the ones that didn't use it were inspired by the color palette used in that pack.

## Contributing
Bug reports and pull requests are welcome on GitHub at [https://github.com/amidos2006/benchmark_experiments](https://github.com/amidos2006/benchmark_experiments).

## License
This code is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).
