# OVERVIEW

This code follows up on a convolutional neural network architecture previously implemented for learning to match question and answer sentences described in the paper:

Aliaksei Severyn and Alessandro Moschitti. *Learning to Rank Short Text Pairs with Convolutional Deep Neural Networks*. SIGIR, 2015

The code following their paper is [available here.](https://github.com/aseveryn/deep-qa)

Following changes are made to the model:
1. The code now uses for a different dataset( [Yahoo Answers](https://drive.google.com/file/d/0BzMkWccldefraVBZRlJjbS1XRHc/view?usp=sharing)). The dataset has been split to obtain the top five categories with the highest number of questions and these categories can be downloaded from [here](https://drive.google.com/open?id=0B1ttwhq718PdYlNMeC1hNmhyOWs). The dataset consists of 5 XML files, each related to a particular category as specified by the file name. Since this dataset consists of longer answers for each question, we consider question-answer pairs whose answer length are at a maximum of 150 words while loading the data for the CNN, as opposed to the paper, which has 50 words.

2. Instead of computing the word overlap between question and an answer, we follow a more general approach, and compare the similarity score obtained from a Word2vec model between each word in the question with every word in the answer. Similarity scores greater than a certain threshold(our current approach uses a threshold of 0.8, but can be changed from parse.py) will be considered the same as two words overlaping and will be added as before to the word embeddings of wordsas described in the paper. 

3. Small changes have been made to the bash scripts.

# DEPENDENCIES

- python 2.7+
- [gensim](https://radimrehurek.com/gensim/)(required for computing similarity score)
- numpy
- [theano](http://deeplearning.net/software/theano/)
- scikit-learn (sklearn)
- pandas
- tqdm
- fish
- numba

# EMBEDDINGS

The pre-initialized word2vec embeddings have to be downloaded from [here](https://drive.google.com/folderview?id=0B-yipfgecoSBfkZlY2FFWEpDR3M4Qkw5U055MWJrenE5MTBFVXlpRnd0QjZaMDQxejh1cWs&usp=sharing).

For computing the similarity score, we use the [GoogleNews word2vec model](https://drive.google.com/file/d/0BzMkWccldefraXpFcW05cWd5Skk/view?usp=sharing) since this model has been more thoroughly trained and hence can find similarities more accurately.


# BUILD
First download the dataset into your root folder directory. To split the XML file of a specific category into separate train/test/dev file and to load data from these files run:

`$ sh run_build_datasets.sh $FOLDERNAME/$FILENAME`

where FOLDERNAME is the folder name of the recently downloaded XML files and FILENAME is the filename of the specific XML file that you want to run your CNN on.

Example: `$ sh run_build_datasets.sh dataset/Health.xml`

The script creates a folder named after your filename and adds a TRAIN/ folder inside it, which contains all your data for the CNN.

To train the model for a specific category, run

`python run_nnet.py $FOLDERNAME/$CATEGORYNAME/TRAIN`

where FOLDERNAME is the folder name of the recently downloaded XML files and CATEGORYNAME is the name of the category that you want to run your CNN on which contains a TRAIN folder inside it previously created from `run_build_datasets.sh`

Example: `python run_nnet.py dataset/Health/TRAIN`

The results for the different categories are as follows:


Similarity Threshold = 0.8

| Category              | MAP  | MRR   |
|-----------------------|:---: |:-----:|
|Family-Relationship    |0.6218|0.6218 |
|Business-Finance       |0.7801|0.7801 |
|Health                 |0.6177|0.6177 |
|Home-Garden            |0.6838|0.6836 |
|Education-Reference    |0.7322|0.7322 |

# REFERENCES

Aliaksei Severyn and Alessandro Moschitti. 
*Learning to Rank Short Text Pairs with Convolutional Deep Neural Networks*. 
SIGIR, 2015

# License

This software is licensed under the [Apache 2 license](http://www.apache.org/licenses/LICENSE-2.0).
