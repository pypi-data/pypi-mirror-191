"""Utilities for PVT computations"""
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import pandas as pd
import matplotlib.pyplot as plt

# Gaius Agent
from ia.gaius.prediction_models import *
def emotives_value_metrics_builder(lst_of_emotives):
    """
    Create Metrics Data Structure for each emotive in testset
    """
    emotives_metrics_data_structure = {}
    for emotive in lst_of_emotives:
        emotives_metrics_data_structure[emotive] = {
            "predictions": [],
            "actuals": [],
            "metrics": {
                "resp_pc": None, # response rate percentage
                "rmse": None,
                # "smape_acc": None, # NOTE: Took this out because the metrics for values cannot handle unknown predictions, so only precision matters
                "smape_prec": None
            }
        }
    return emotives_metrics_data_structure


def emotives_polarity_metrics_builder(lst_of_emotives):
    """
    Create Metrics Data Structure for each emotive in testset
    """
    emotives_metrics_data_structure = {}
    for emotive in lst_of_emotives:
        emotives_metrics_data_structure[emotive] = {
            "predictions": [],
            "actuals": [],
            "metrics": {
                "resp_pc": None,
                "accuracy": None,
                "precision": None
            }
        }
    return emotives_metrics_data_structure


def classification_metrics_builder(lst_of_labels):
    """
    Create Metrics Data Structure for a classification problem where labels are tracked and used.
    """
    classification_metrics_data_structure = {
        'predictions': [],
        'actuals': [],
        'labels': list(lst_of_labels) + ['i_dont_know'],
        'metrics': {
            'resp_pc': None,
            'accuracy': None,
            'precision': None
        }
    }
    return classification_metrics_data_structure


def model_per_emotive_(ensemble, emotive, potential_normalization_factor):
    "Using a Weighted Moving Average, though the 'moving' part refers to the prediction index."
    ## using a weighted posterior_probability = potential/marginal_probability
    ## FORMULA: pv + ( (Uprediction_2-pv)*(Wprediction_2) + (Uprediction_3-pv)*(Wprediction_3)... )/mp
    # A Weighted Moving Average puts more weight on recent data and less on past data. This is done by multiplying each bar’s price by a weighting factor. Because of its unique calculation, WMA will follow prices more closely than a corresponding Simple Moving Average.
    # https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/wma#:~:text=Description,a%20corresponding%20Simple%20Moving%20Average.
    _found = False
    while not _found:
        for i in range(0,len(ensemble)):
            if emotive in ensemble[i]['emotives'].keys():
                _found = True
                principal_value = ensemble[i]['emotives'][emotive]  ## Let's use the "best" match (i.e. first showing of this emotive) as our starting point. Alternatively, we can use,say, the average of all values before adjusting.
                break
        if i == len(ensemble) and not _found:
            return 0
        if i == len(ensemble) and _found:
            return principal_value
    marginal_probability = sum([x["potential"] for x in ensemble]) # NOTE: marginal_probability = mp, this might the wrong calculation for this variable.
    weighted_moving_value = 0 # initialized top portion of summation
    for x in ensemble[i+1:]:
        if emotive in x['emotives']:
            weighted_moving_value += (x['emotives'][emotive] - (principal_value)) * ((x["potential"] / potential_normalization_factor))
    weighted_moving_emotive_average = principal_value + (weighted_moving_value / marginal_probability)
    return weighted_moving_emotive_average


def make_modeled_emotives_(ensemble):
    '''The emotives in the ensemble are of type: 'emotives':[{'e1': 4, 'e2': 5}, {'e2': 6}, {'e1': 5 'e3': -4}]'''
    emotives_set = set()
    potential_normalization_factor = sum([p['potential'] for p in ensemble])

    filtered_ensemble = []
    for p in ensemble:
        new_record = p
        new_record['emotives'] = average_emotives([p['emotives']]) # AVERAGE
        filtered_ensemble.append(new_record)

#     filtered_ensemble = bucket_predictions(filtered_ensemble) # BUCKET

    for p in filtered_ensemble:
        emotives_set = emotives_set.union(p['emotives'].keys())
    return {emotive: model_per_emotive_(ensemble, emotive, potential_normalization_factor) for emotive in emotives_set}



def plot_confusion_matrix(test_num, class_metrics_data_structures):
    """
    Takes a node classification test to create a confusion matrix. This version includes the i_dont_know or unknown label.
    """

    for node_name, class_metrics_data in class_metrics_data_structures.items():
        print(f'-----------------Test#{test_num}-{node_name}-Plots-----------------')
        sorted_labels = sorted(class_metrics_data['labels'])
        cm           = confusion_matrix(class_metrics_data['actuals'], class_metrics_data['predictions'], labels=sorted_labels)
        disp         = ConfusionMatrixDisplay(confusion_matrix=cm,display_labels=sorted_labels)
        disp.plot()
        plt.show()

