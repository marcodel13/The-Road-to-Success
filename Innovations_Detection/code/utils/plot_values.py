import matplotlib.pyplot as plt
import pylab
import re
import argparse


def Parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-data', type=str, help="Specify data path")
    parser.add_argument('-subreddit', type=str, help="Specify subreddit name")
    parser.add_argument('-range', nargs='+', type=int, help="Specify the range of words to plot", default=[0,-1])

    return parser.parse_args()


input = open(
    '/Users/marcodeltredici/workspace/PYCHARM/new_exp/experiment_2/innovations_detection/results/LiverpoolFC_author_ss.txt').readlines()


def PlotTrajectories(input):
    final_values = []
    dfp = []

    for line in input:
        final_values.append(float(line.split(',')[-1].split(']')[0]))

        tw = re.findall(r"'(\w+)'", line)[0]
        traj = [float(x) for x in re.findall(r"\[(.+)\]", line)[0].split(',')]

        dfp.append((tw, traj))

    for item in dfp[int(args.range[0]):int(args.range[1])]:
        plt.plot(item[1], label=item[0])

    plt.legend()
    F = pylab.gcf()
    DefaultSize = F.get_size_inches()
    F.set_size_inches((DefaultSize[0] * 2, DefaultSize[1] * 2))
    F.savefig('plot_{0}'.format(args.subreddit))
    plt.close()


def PlotFinalValues(input):

    final_values = []

    for line in input:

        fv = float(re.findall(r' \((\d+\.\d+), ', line)[0])
        final_values.append(fv)

    plt.plot(final_values)
    plt.savefig('values_distribution_{0}'.format(args.subreddit))
    plt.close()



''' RUN THE CODE '''

if __name__ == "__main__":
    args = Parse_args()
    PlotTrajectories(open(args.data).readlines())
    PlotFinalValues(open(args.data).readlines())

