"""
CULMINATING ASSIGNMENT 2: RSI

Create a program which will provide answers to the tasks posed in the assignment description.

For this assignment, you will start from scratch with this blank template.
It is your reponsibility to include all necessary program components in this file.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.

The relevant data file is named "all_participant_data_rsi.csv" and is located in data > drop-jump.

All file paths need to be relative and execute from this file's directory;
the Visual Studio Code setting "Python > Terminal: Execute in File Dir" 
must be enabled in File > Preferences > Settings.

See Canvas for additional requirements.
"""
# Task 1: conduct a paired t-test comparing all the force plate and accelerometer RSI values
############################################################################################
# this means I need to determine wheather those two sets of data are significantly different from each other
# a t-test will be an appropriate statistical test to use for this comparison because the two measurements are from the same trial
# import the necessary libraries for task 1:
import numpy as np
from os import path
from scipy import stats
# import the new libraries necessary for task 2:
from scipy.stats import norm, chisquare
import matplotlib.pyplot as plt
# import the new libraries necessary for task 3:
import pandas as pd

def main(full_path_to_file):
    # check to see if the file exists 
    if not path.exists(full_path_to_file):
        print("File does not exist", full_path_to_file)
        return None

    # load in the RSI data from the CSV file (learned through Module 3)
    # tell python the values are separated by commas, skip the first row, and only use the 2nd and 3rd columns
    data = np.loadtxt(full_path_to_file, delimiter=',', skiprows=1, usecols=(1, 2))

    # separate the force plate and accelerometer RSI values and select the columns for the data (learned through Module 3)
    force_plate = data[:, 0]
    accelerometer = data[:, 1]

    # conduct the paired t-test (Learned through Module 4)
    results = stats.ttest_rel(force_plate, accelerometer)

    # get the t-value and p-value from the results
    t_value = results.statistic
    p_value = results.pvalue

    return t_value, p_value, accelerometer

#Task 2: for the RSI values gathered using an accelerometer, fit a normal distribution and conduct a Chi2 Goodness of Fit Test
##############################################################################################################################
# this means I need to determine whether the accelerometer RSI values are normally distributed
def task_2(accelerometer):
    # fit the accelerometer data to a normal distribution (Learned through Module 5)
    (fitted_mean, fitted_std) = norm.fit(accelerometer)

    # use the normal distribution to create 5 bins for the Chi2 Goodness of Fit Test (Learned through Module 5)
    probabilities = np.linspace(0, 1, 6)
    bins = norm.ppf(probabilities, loc=fitted_mean, scale=fitted_std)

    # count the number of samples in each bin (Learned through Module 5)
    observed_counts, observed_edges = np.histogram(accelerometer, bins=bins)

    # use normal distribution to calculate the expected counts for each bin (Learned through Module 5)
    expected_probabilities = np.diff(norm.cdf(bins, loc=fitted_mean, scale=fitted_std))

    # calculate the expected counts for each bin (Learned through Module 5)
    expected_counts = expected_probabilities * len(accelerometer)

    # conduct the Chi2 goodness of fit test (Learned through Module 5)
    (chi_stat, p_value) = chisquare(f_obs=observed_counts, f_exp=expected_counts, ddof=2)

    # print the results
    print("Chi2 statistic:", chi_stat)
    print("fitted mean:", fitted_mean)
    print("fitted standard deviation:", fitted_std)
    print("p-value:", p_value)

    # given significance level for the test
    alpha = 0.05

    # determine whether the null hypothesis can be rejected or not (Learned through Module 4)
    if p_value < alpha:
        print("Reject the null hypothesis.")
    else:
        print("Fail to reject the null hypothesis.")

    # plot a histogram of the accelerometer data with the normal distribution curve overlaid (Learned through Module 5)
    x = np.linspace(np.min(accelerometer), np.max(accelerometer), 1000)
    y = norm.pdf(x, loc=fitted_mean, scale=fitted_std)

    # plot the normal distribution curve over the histogram of the accelerometer data
    plt.plot(x, y, label='Fitted Normal Distribution') 

    # include appropriate labels, titles, and legends
    plt.title('Normal Distribution Fit for RSI Data')
    plt.xlabel('Accelerometer RSI')
    plt.ylabel('Probability Density')
    plt.legend()
    plt.show()

# Task 3: from the force plate and accelerometer-based RSI data for all participants, create a datafram containing only the trials from participant 'F'
########################################################################################################################################################
def task_3(full_path_to_file):
    # load the RSI data into a pandas dataframe (Learned through Module 4)
    df = pd.read_csv(full_path_to_file)

    # filter the dataframe to only include trials from participant 'F' (Learned through Module 4)
    participant_f = df[df['trial'].str.startswith('F')]

    # print the dataframe containing only the trials from participant 'F'
    print("\nParticipant F RSI Data:")
    print(participant_f)

    # separate the force plate and accelerometer RSI values for participant 'F' (Learned through Module 4)
    force_plate = participant_f['force_plate_rsi'].to_numpy()
    accelerometer = participant_f['accelerometer_rsi'].to_numpy()

    # calculate the 95% confidence interval for the force plate data
    force_plate_ci = stats.t.interval(
        confidence=0.95, 
        df=len(force_plate)-1,
        loc=np.mean(force_plate),
        scale=stats.sem(force_plate)
    )

    # calculate the 95% confidence interval for the accelerometer data
    accelerometer_ci = stats.t.interval(
        confidence=0.95, 
        df=len(accelerometer)-1,
        loc=np.mean(accelerometer),
        scale=stats.sem(accelerometer)
    )

    # print the confidence intervals for both the force plate and accelerometer measurements
    print("\nPartipant F 95% Confidence Intervals:")
    print("Force Plate:", force_plate_ci)
    print("Accelerometer:", accelerometer_ci)

# when running this file directly, this will execute first (Learned through Module 3 and 4) 
if __name__ == "__main__":
    # change the filename
    filename = "all_participant_data_rsi.csv"

    # load the data to the data folder
    path_to_data = "../../data/drop-jump/"

    # combine the folder path and filename to make a single relative path
    full_path_to_file = path_to_data + filename

    # call the main function to conduct the paired t-test
    results = main(full_path_to_file)

    if results is not None:
        # separate the t-value and p-value
        t_value, p_value, accelerometer = results

        # set the significance value
        alpha = 0.05

        # print the results 
        print("Paired t-test results:")
        print("t-value:", t_value)
        print("p-value:", p_value)

        # determine whether the null hypothesis can be rejected or not (Learned through Module 4)
        if p_value < alpha:
            print("Reject the null hypothesis.")
        else:
            print("Fail to reject the null hypothesis.")

        # call the task_2 function to conduct the Chi2 Goodness of Fit Test
        task_2(accelerometer)

        # call the task_3 function to create a dataframe for participant 'F' and calculate the 95% confidence intervals
        task_3(full_path_to_file)
