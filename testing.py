from __future__ import division
import csv
import pandas as pd
import os

#  this is all one huge hack, please forgive me



def parse_narratives_recall(list):
    nar0 = []
    nar1 = []
    nar2 = []
    nar3 = []
    nar4 = []
    nar5 = []
    nar6 = []
    nar7 = []
    nar8 = []
    nar9 = []
    for line in list:
        if line[1] == "0":
            nar0.append(line)
        elif line[1] == "1":
            nar1.append(line)
        elif line[1] == "2":
            nar2.append(line)
        elif line[1] == "3":
            nar3.append(line)
        elif line[1] == "4":
            nar4.append(line)
        elif line[1] == "5":
            nar5.append(line)
        elif line[1] == "6":
            nar6.append(line)
        elif line[1] == "7":
            nar7.append(line)
        elif line[1] == "8":
            nar8.append(line)
        elif line[1] == "9":
            nar9.append(line)
    return [nar0, nar1, nar2, nar3, nar4, nar5, nar6, nar7, nar8, nar9]


def parse_narratives_sum(list):
    nar0 = []
    nar1 = []
    nar2 = []
    nar3 = []
    nar4 = []
    for line in list:
        if line[1] == "0":
            nar0.append(line)
        elif line[1] == "1":
            nar1.append(line)
        elif line[1] == "2":
            nar2.append(line)
        elif line[1] == "3":
            nar3.append(line)
        elif line[1] == "4":
            nar4.append(line)
    return [nar0, nar1, nar2, nar3, nar4]

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
    narrative = None

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
                narrative = item[1]
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


    d = {"narrative": narrative, "argument": arg_name, "A": actions/total, "AO": action_orientation/total, "AA": action_action/total,
                "AE": action_evaluation/total, "E": evaluations/total, "EO": evaluation_orientation/total,
                "EE": evaluation_evaluation/total, "EA": evaluation_action/total, "O": orientations/total,
                "OO": orientation_orientation/total, "OE": orientation_evaluation/total, "OA": orientation_action/total}
    df = pd.DataFrame(d, index=[d["argument"]])
    return df


def write(infile, recall=True):
    with open('out.csv', 'a') as f:
        arguments = parse(infile)
        for argument in arguments:
            if recall:
                for narrative in parse_narratives_recall(argument):
                    process(narrative, 2).to_csv(f, header=False)
            else:
                for narrative in parse_narratives_sum(argument):
                    process(narrative, 3).to_csv(f, header=False)

def process_ra(filename):
    with open('out1.csv', 'a') as f:
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            accumulator = []
            for line in reader:
                accumulator.append(line)
            process(accumulator[1:], 2).to_csv(f, header=False)

def process_sa(filename):
    with open('out1.csv', 'a') as f:
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            accumulator = []
            for line in reader:
                accumulator.append(line)
            process(accumulator[1:], 3).to_csv(f, header=False)

os.remove('out1.csv')
pd.DataFrame(columns=['A', 'AA', 'AE', 'AO', 'E', 'EA', 'EE', 'EO',  'O', 'OA', 'OE', 'OO', 'argument', 'narrative']).to_csv('out1.csv')
process_ra('ra.csv')
process_sa('sa.csv')

os.remove('out.csv')
pd.DataFrame(columns=['A', 'AA', 'AE', 'AO', 'E', 'EA', 'EE', 'EO',  'O', 'OA', 'OE', 'OO', 'argument', 'narrative']).to_csv('out.csv')
write('ra.csv')
write('sa.csv', False)




