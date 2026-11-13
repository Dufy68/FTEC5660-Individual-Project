# FTEC5660 Individual Project

This LiTS reproducibility study compares 3 and 10 MCTS iterations on a fixed MATH500 subset across three trials. See the [methods, results, and run instructions](coursework/README.md), the [trial summary](coursework/results/main_trials.csv), and the [raw evidence archive](coursework/deliverables/FTEC5660_LiTS_Evidence.zip).

## Set up the study

Clone this repository, then run the following from its root. These commands prepare the pinned LiTS checkout and copy the coursework into it.

```sh
git clone https://github.com/xinzhel/lits-llm.git lits-upstream
git -C lits-upstream checkout 25e94d862cb4514c22d9a80a635e392461769df7
git -C lits-upstream apply ../patches/deepseek-thinking.patch
cp -R coursework lits-upstream/
cd lits-upstream
```

Continue with the Python setup and API configuration in [coursework/README.md](coursework/README.md). LiTS is distributed under its upstream Apache 2.0 license.
