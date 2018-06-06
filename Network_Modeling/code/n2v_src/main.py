import n2v
from gensim.models import Word2Vec

def learn_embeddings(walks, dimensions, window_size, workers, iter, subreddit, timestamp):
	'''
	Learn embeddings by optimizing the Skipgram objective using SGD.
	'''
	lista = []

	walks =[[str(x) for x in walk] for walk in walks]
	model = Word2Vec(walks, size=dimensions, window=window_size, min_count=0, sg=1, workers=workers, iter=iter)
	model.wv.save_word2vec_format('../embeddings/karate_{0}_{1}.emd'.format(subreddit, timestamp))

	return


def main_n2v(args, net, timestamp):
	'''
	Pipeline for representational learning for all nodes in a graph.
	'''
	nx_G = net
	G = n2v.Graph(nx_G, args.directed, args.p, args.q)
	G.preprocess_transition_probs()
	walks = G.simulate_walks(args.num_walks, args.walk_length)
	learn_embeddings(walks, args.dimensions, args.window_size, args.workers, args.iter, args.subreddit, timestamp)



