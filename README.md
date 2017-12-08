# VotePredictor
Using Naive Bayes to Predict Votes of Congressmen from Bill Texts. By David Gibson, Thomas Chang, Mustafa Bal.

# System Description
All code is written for python 3.6 and is assumed to be executed in the top level directory of the git repository. Additionally, nltk and matplotlib.pylplot are dependencies for this project. These two libraries can be found  at the following two links: [nltk]{http://www.nltk.org/install.html and [matplotlib]{http://matplotlib.org/users/installing.html}. Generated plots will vary slightly from displayed plots because of randomization in the training and validation sets.

1. Clone the [git repo](https://github.com/mstfbl/VotePredictor)
2. Unzip **complete.zip** and keep **complete.json** in the same directory as **model.py**
3. Execute ```python model.py``` (this creates three files **training\_set.json**, **validation\_set.json**, and **model.json**)
4. Execute ```python validate.py``` 1 100 1" to parameter sweep *c* from the values 1-100. (Usage for this file is ```python validate.py start numIter step``` where start is the first value of *c* tested, numIter is the number of different values of *c* tested, and step is the amount *c* is incremented every iteration)
5. Execute ```python plotChyperparam.py```
6. Open **plot.png** to examine the plot

In order to test multiple values for *k*, the value was adjusted by hand in the source code. Additionally, other values of *c* can be tested by following the usage of **validate.py**.
