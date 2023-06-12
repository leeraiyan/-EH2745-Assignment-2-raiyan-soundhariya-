# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 19:23:28 2023

@author: ADMIN
"""
import os
import csv
import random
import math
import operator
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix



class AgentKNN:
    def __init__(self) -> None:
        self.caseInteger = {
            'Normal Operation': 1,
            'High Load Operation': 2,
            'Low Load Operation': 3,
            'Gen Disconnected - High Load Operation': 4,
            'Gen Disconnected - Low Load Operation': 5,
            'Line Disconnected - High Load Operation': 6,
            'Line Disconnected - Low Load Operation': 7

        }


    #Create dataset for training and testing
    def loadDataset(self, dataRatio, trainingSet=[] , testSet=[]):
        with open('./check.csv', 'r') as csvfile:
            lines = csv.reader(csvfile)
            dataset = list(lines)
            for x in range(len(dataset)-1):
                #Classified as 18 data inputs of voltage and angle
                for y in range(18):
                    dataset[x][y] = float(dataset[x][y])
                if random.random() < dataRatio: 
                    trainingSet.append(dataset[x]) 
                else: 
                    testSet.append(dataset[x]) 
                    
    #Calculate the distance between the  test point and existing points in the training set          
    def euqlideanDistance(self, testSet1, trainSet1, length): 
        distance = 0 
        for x in range(length): 
            distance += pow(float(testSet1[x]) - float(trainSet1[x]), 2) 
        return math.sqrt(distance) 

    #Find the test class nearest to the train class
    def KNNeighbours(self, trainingSet, testInstance, k): 
        distances = [] 
        length = len(testInstance)-1 
        for x in range(len(trainingSet)): 
            dist = self.euqlideanDistance(testInstance, trainingSet[x], length) 
            distances.append((trainingSet[x], dist))
        #Sorts the distances between the test point and train set in ascending order
        distances.sort(key=operator.itemgetter(1)) 
        neighbours = [] 
        for x in range(k): 
            neighbours.append(distances[x][0]) 
        return neighbours 

    #Predict the class for the test set
    def predict(self, neighbours): 
        classVotes = {} 
        for x in range(len(neighbours)): 
            response = neighbours[x][-1] 
            if response in classVotes: 
                classVotes[response] += 1 
            else: 
                classVotes[response] = 1 
        sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True) 
        return sortedVotes[0][0] 

    #Calculate the testing accuracy
    def calculateAccuracy(self, testSet, predictions): 
        predictedArr = np.zeros(len(testSet))
        labelsArr = np.zeros(len(testSet))
        correct = 0 
        for x in range(len(testSet)): 
            if testSet[x][-1] == predictions[x]: 
                correct += 1 
            predictedArr[x] = predictions[x]
            labelsArr[x] = testSet[x][-1]

        cm = confusion_matrix(labelsArr, predictedArr)

        # Plot confusion matrix
        plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title("Confusion Matrix")
        plt.colorbar()
        plt.xticks(np.arange(len(cm)), labels=np.unique(labelsArr))
        plt.yticks(np.arange(len(cm)), labels=np.unique(labelsArr))
        plt.xlabel("Predicted Labels")
        plt.ylabel("True Labels")

        static_folder = os.path.join("application", "static")
        os.makedirs(static_folder, exist_ok=True)
        filename = os.path.join(static_folder, f'KNN-confusion.png')
        plt.savefig(filename)
        return (correct/float(len(testSet))) * 100.0 

    def KNN(self): 
        # prepare data 
        trainingSet=[] 
        testSet=[] 
        dataRatio = 0.8
        self.loadDataset(dataRatio, trainingSet, testSet) 
        predictions=[] 
        k = 55 


        for x in range(len(testSet)): 
            neighbours = self.KNNeighbours(trainingSet, testSet[x], k) 
            result = self.predict(neighbours) 
            predictions.append(result) 
            print('> Predicted Class=' + repr(result) + ', Actual Class=' + repr(testSet[x][-1]))
        accuracy= self.calculateAccuracy(testSet, predictions)
        print('Testing Accuracy:', accuracy, '%')
        
