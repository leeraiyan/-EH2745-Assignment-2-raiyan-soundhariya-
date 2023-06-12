import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

class GraphPlotter:
    def __init__(self) -> None:
        self.indexToDimension = ['Voltage Magnitude at Node 1','Voltage Magnitude at Node 2','Voltage Magnitude at Node 1','Voltage Magnitude at Node 4',
                                 'Voltage Magnitude at Node 5','Voltage Magnitude at Node 6','Voltage Magnitude at Node 7','Voltage Magnitude at Node 8',
                                 'Voltage Magnitude at Node 9',
                                 'Voltage Angle at Node 1','Voltage Angle at Node 2','Voltage Angle at Node 3','Voltage Angle at Node 4','Voltage Angle at Node 5',
                                 'Voltage Angle at Node 6','Voltage Angle at Node 7','Voltage Angle at Node 8','Voltage Angle at Node 9']


    def scatterPlotScikitLearn(self, inputs, dimensions, final_cluster):
        unique_values, counts = np.unique(final_cluster, return_counts=True)
        num_plots = 5

        # Create a K-means clustering model with 4 clusters
        kmeans = KMeans(n_clusters=len(unique_values))
        # Fit the model to the data
        kmeans.fit(inputs)

        # Get the predicted cluster labels for each data point
        cluster_labels = kmeans.labels_

        # Select four random dimensions for pairwise plots
        random_dimensions = dimensions

        static_folder = os.path.join("application", "static")
        os.makedirs(static_folder, exist_ok=True)

        filenames = []
        # Iterate over each plot
        for i in range(num_plots):
            fig, ax = plt.subplots()

            # Create a scatter plot for the selected dimensions
            for cluster in np.unique(cluster_labels):
                cluster_indices = np.where(cluster_labels == cluster)
                ax.scatter(inputs[cluster_indices, random_dimensions[i, 0]],
                        inputs[cluster_indices, random_dimensions[i, 1]],
                        label=f'Cluster {cluster}')

            # Set labels and title for each subplot
            ax.set_xlabel(f'{self.indexToDimension[random_dimensions[i, 0]]}')
            ax.set_ylabel(f'{self.indexToDimension[random_dimensions[i, 1]]}')
            ax.set_title(f'K-Means Pairwise Scatter Plot {i+1} (Scikit-Learn)')
            ax.legend()
            filename = os.path.join(static_folder, f'Kmeans-scatter-scikitlearn{i+1}.png')
            plt.savefig(filename)
            filenames.append(filename)
        return filenames, cluster_labels    


    def scatterPlot(self, inputs, final_cluster):
        num_plots = 5

        # Select three random dimensions for each plot
        random_dimensions = np.random.choice(inputs.shape[1], (num_plots, 3), replace=False)

        static_folder = os.path.join("application", "static")
        os.makedirs(static_folder, exist_ok=True)

        filenames = []
        # Iterate over each plot
        for i in range(num_plots):
            fig, ax = plt.subplots()

            # Create a scatter plot for the selected dimensions
            for cluster in np.unique(final_cluster):
                cluster_indices = np.where(final_cluster == cluster)
                ax.scatter(inputs[cluster_indices, random_dimensions[i, 0]],
                        inputs[cluster_indices, random_dimensions[i, 1]],
                        label=f'Cluster {cluster}')

            # Set labels and title for each subplot
            ax.set_xlabel(f'{self.indexToDimension[random_dimensions[i, 0]]}')
            ax.set_ylabel(f'{self.indexToDimension[random_dimensions[i, 1]]}')
            ax.set_title(f'K-Means Pairwise Scatter Plot {i+1}')
            ax.legend()
            filename = os.path.join(static_folder, f'Kmeans-scatter{i+1}.png')
            plt.savefig(filename)
            filenames.append(filename)
        return filenames, random_dimensions

    def barChart(self, final_cluster):
        static_folder = os.path.join("application", "static")
        os.makedirs(static_folder, exist_ok=True)    


        unique_values, counts = np.unique(final_cluster, return_counts=True)

        # Create a new figure and axis
        fig, ax = plt.subplots()

        # Plot the bar chart
        ax.bar(unique_values.tolist(), counts.tolist())

        # Set labels and title
        ax.set_xlabel('Categories')
        ax.set_ylabel('Values')
        ax.set_title('Size of Clusters')
        filename = os.path.join(static_folder, f'Kmeans-barChart.png')
        plt.savefig(filename)

        return filename



    def barChartScikitLearn(self, final_cluster):
        static_folder = os.path.join("application", "static")
        os.makedirs(static_folder, exist_ok=True)    

        unique_values, counts = np.unique(final_cluster, return_counts=True)

        # Create a new figure and axis
        fig, ax = plt.subplots()

        # Plot the bar chart with red color
        ax.bar(unique_values.tolist(), counts.tolist(), color='red')

        # Set labels and title
        ax.set_xlabel('Categories')
        ax.set_ylabel('Values')
        ax.set_title('Size of Clusters')
        filename = os.path.join(static_folder, f'Kmeans-barChart-scikitlearn.png')
        plt.savefig(filename)

        return filename



    def plot(self, inputs_df, final_cluster):
        final_cluster = final_cluster.astype(int)
        # Select the number of pairwise scatter plots you want
        inputs = inputs_df[['vm1','vm2','vm3','vm4','vm5','vm6','vm7','vm8','vm9',
                'degree1','degree2','degree3','degree4','degree5','degree6','degree7','degree8','degree9']].to_numpy()
        filenamesScatterPlot, dimensions =  self.scatterPlot(inputs, final_cluster)
        filenameBarChart = self.barChart(final_cluster)
        filenamesScikitLearn, cluster_labels = self.scatterPlotScikitLearn(inputs, dimensions, final_cluster)
        filenameBarChartScikitLearn = self.barChartScikitLearn(cluster_labels)


