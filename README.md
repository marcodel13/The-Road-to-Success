# The-Road-to-Success

Code and materials to reprocude the findings in the paper _The Road to Success: Assessing the Fate of Linguistic Innovations in Online Communities_ by [Marco Del Tredici](https://sites.google.com/site/marcodeltredici/) and [Raquel Fernández](https://staff.fnwi.uva.nl/r.fernandezrovira/), accepted to [COLING 2018](http://coling2018.org/).

This directory includes three sub-folders:

- Innovations_Detections: includes code to analyze the spread of a linguistic innovation in a communty of speakers.

- Network_Modeling: includes code for creating time-dependent graphs representing the social scturcture of the community and to compute the tie-strenght of the edges connecting users.

- Plots: includes (i) the general probability mass distribution of tie strengths (red) and the probability distribution for innovators (blue) for each subreddit; (ii) an example of a network graph taken from our dataset.

## Requirements

* Python 3
* `networkx`

## Citation

Please cite our paper if you use this code:
```
@inproceedings{deltredici-fernandez:2018:coling,
	Author = {Marco Del Tredici and Raquel Fern\'andez},
	Booktitle = {Proceedings of the 27th International Conference on Computational Linguistics (COLING 2018)},
	Title = {{The Road to Success: Assessing the Fate of Linguistic Innovations in Online Communities}},
	Year = {2018}
  }
``` 
