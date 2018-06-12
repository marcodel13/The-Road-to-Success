# The Road to Success

Code and data to reprocude the findings in the paper _The Road to Success: Assessing the Fate of Linguistic Innovations in Online Communities_ by [Marco Del Tredici](https://sites.google.com/site/marcodeltredici/) and [Raquel Fernández](https://staff.fnwi.uva.nl/r.fernandezrovira/), accepted to [COLING 2018](http://coling2018.org/).

Our analyses exploit data from 20 [Reddit](https://www.reddit.com/) forums (subreddits). The dataset ([20Reddit-Road2Success](https://figshare.com/articles/20Reddit-Road2Success/6479213)) is freely available under a Creative Commons (CC BY 0.4) license. 

This directory includes three sub-folders:

- Innovations_Detection: includes code to analyze the spread of a linguistic innovation in a communty of speakers.

- Network_Modeling: includes code for creating time-dependent graphs representing the social scturcture of the community and to compute the tie-strenght of the edges connecting users.

- Plots: includes (i) plots of the general probability mass distribution of tie strengths and the probability distribution for innovators for each subreddit; (ii) an example of a network graph taken from our dataset.

## Requirements

* Python 3
* `networkx`

## Citation

Please cite our paper if you use any of these materials:
```
@inproceedings{deltredici-fernandez:2018:coling,
	Author = {Marco Del Tredici and Raquel Fern\'andez},
	Booktitle = {Proceedings of the 27th International Conference on Computational Linguistics (COLING 2018)},
	Title = {{The Road to Success: Assessing the Fate of Linguistic Innovations in Online Communities}},
	Year = {2018}
  }
``` 
