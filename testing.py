from __future__ import division
import csv
import pandas as pd
import os


def parse(filename):
    arg1 = []
    arg2 = []
    arg3 = []
    arg4 = []
    arg5 = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        while True:
            try:
                line = reader.next()
                if line[0] == "arg1":
                    arg1.append(line)
                elif line[0] == "arg2":
                    arg2.append(line)
                elif line[0] == "arg3":
                    arg3.append(line)
                elif line[0] == "arg4":
                    arg4.append(line)
                elif line[0] == "arg5":
                    arg5.append(line)
            except StopIteration:
                break
    return [arg1, arg2, arg3, arg4, arg5]



def process(argument, label_location):
    '''
    :param argument: list of lines from CSV file
    :param label_location: location of label in CSV headers
    :return: two dictionaries containing subdictionaries
                "bigrams"
                  *  "freq" frequency information for bigrams
                  *  "n_freq" normalized
                "unigrams"
                  *  "freq" frequency information for unigrams
                  *  "n_freq" normalized
    '''

    total = len(argument)
    arg_name = None

    actions = 0
    action_action = 0
    action_evaluation = 0
    action_orientation = 0

    evaluations = 0
    evaluation_action = 0
    evaluation_orientation = 0
    evaluation_evaluation = 0

    orientations = 0
    orientation_action = 0
    orientation_evaluation = 0
    orientation_orientation = 0

    for index, item in enumerate(argument):
            if index+1 == total:
                arg_name = item[0]
                if item[label_location] == "Action":
                    actions += 1
                elif item[label_location] == "Evaluation":
                    evaluations += 1
                elif item[label_location] == "Orientation":
                    orientations += 1
                break

            elif item[label_location] == "Action":
                actions += 1
                if argument[index+1][label_location] == "Evaluation":
                    action_evaluation += 1
                elif argument[index+1][label_location] == "Action":
                    action_action += 1
                elif argument[index+1][label_location] == "Orientation":
                    action_orientation += 1

            elif item[label_location] == "Evaluation":
                evaluations += 1
                if argument[index+1][label_location] == "Action":
                    evaluation_action += 1
                elif argument[index+1][label_location] == "Evaluation":
                    evaluation_evaluation += 1
                elif argument[index+1][label_location] == "Orientation":
                    evaluation_orientation += 1

            elif item[label_location] == "Orientation":
                orientations += 1
                if argument[index+1][label_location] == "Action":
                    orientation_action += 1
                elif argument[index+1][label_location] == "Evaluation":
                    orientation_evaluation += 1
                elif argument[index+1][label_location] == "Orientation":
                    orientation_orientation += 1


    d = {"argument": arg_name, "A": actions/total, "AO": action_orientation/total, "AA": action_action/total,
                "AE": action_evaluation/total, "E": evaluations/total, "EO": evaluation_orientation/total,
                "EE": evaluation_evaluation/total, "EA": evaluation_action/total, "O": orientations/total,
                "OO": orientation_orientation/total, "OE": orientation_evaluation/total, "OA": orientation_action/total}
    df = pd.DataFrame(d, index=[d["argument"]])
    return df


A = parse('ra.csv')
print A
B = parse('sa.csv')
print B

os.remove('out.csv')
pd.DataFrame(columns=['A', 'AA', 'AE', 'AO', 'E', 'EA', 'EE', 'EO',  'O', 'OA', 'OE', 'OO', 'argument']).to_csv('out.csv')

with open('out.csv', 'a') as f:
    for item in A:
        process(item, 2).to_csv(f, header=False)

    #for item in B:
    #    process(item, 3).to_csv(f, header=False)





