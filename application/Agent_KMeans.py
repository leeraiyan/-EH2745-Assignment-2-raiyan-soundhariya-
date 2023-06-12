import numpy as np


class AgentKMeans:
    def __init__(self) -> None:
        pass

    # To perform the k-nearest-neighbor, we need to calculate Euclidean distance
    def euclidean_distance(self, x1, x2):
        return np.sqrt(np.sum((x1 - x2) ** 2))

    # Calculates mean of number of data points
    def calc_mean(self, data, types, k):
        types = types.astype(int)
        unique_values, counts = np.unique(types, return_counts=True)
        new_means = np.zeros((k, data.shape[1]))
        # print("unique values", unique_values)
        # print("counts", counts)

        for i, type in enumerate(types):
            # print("new means",new_means[type])
            # print("data i ", type(data[i]))
            # print("data new_means", type(new_means[type]))
            try:
                new_means[type] = np.add(new_means[type], data[i])
                # new_means[type] += data[i]
            except:
                print("new_means", new_means[type])
                print("data", data[i])

        # print("shape of new_means", new_means.shape)
        # print("shape of counts", counts.shape)

        for i in range(len(counts)):

            new_means[i] /= counts[i]
        return new_means

    # Calculates difference between previous and new mean values
    def calc_diff(self, x1, x2):
        return np.sum(np.abs(x1 - x2))

    # Calculate cost
    def calc_cost(self, data, means, types):
        cost = 0
        types = types.astype(int)
        unique_values, counts = np.unique(types, return_counts=True)
        for i, type in enumerate(types):
            cost += self.euclidean_distance( means[type],data[i])

        return cost

    def kmeans_clustering(self, data, init_guess=3):
        inputs = data[['vm1','vm2','vm3','vm4','vm5','vm6','vm7','vm8','vm9',
                'degree1','degree2','degree3','degree4','degree5','degree6','degree7','degree8','degree9']].to_numpy()
        
        n_of_data = inputs.shape[0]
        k = 1  # Number of centroids (initializes at one, increases as algorithm runs) until cost difference is small
        J_min = None  # Minimum cost
        J_r = []  # saved costs
        means_r = []
        final_cluster = None

        means_thresh = 1e-4
        while True:
            print("k {}".format(k))
            loop = 0
            # loop by picking random starting element equal to init_guess number of times
            while loop < init_guess:
                init_mean = np.zeros((k, inputs.shape[1]))
                print("loop {}".format(loop))

                for i in range(k):
                    init_mean[i] = inputs[np.random.randint(inputs.shape[0])]

                means_diff = np.ones(k)

                # Continue while new means are different from old ones. Main part of the algorithm.
                curr_means = init_mean
                while np.sum(means_diff) > means_thresh:
                    belong_to = np.zeros(n_of_data)

                    # Assign data points to the closest centroid
                    for i, point in enumerate(inputs):
                        distances = [self.euclidean_distance(point, mean) for mean in curr_means]
                        belong_to[i] = np.argmin(distances)

                    # Find new means
                    next_means = self.calc_mean(inputs, belong_to, k)

                    # Calculate difference between old and new means
                    print("len current means", curr_means.shape)
                    print("len next means", next_means.shape)
                    means_diff = self.calc_diff(curr_means, next_means)

                    # Update current means
                    curr_means = next_means

                # Calculate cost of the current means
                J = self.calc_cost(inputs, curr_means, belong_to)
                final_cluster = belong_to
                # If cost is less than previous attempt, replace the previous result from your previous guess
                if J_min is None:
                    J_min = J
                    means = curr_means
                elif J < J_min:
                    J_min = J
                    means = curr_means

                loop += 1

            # Check if the exit condition is fulfilled
            if k == 1:
                prev_J = J_min
                J_r.append(J_min)
                means_r.append(means)
                print(J_min)
            elif k > 1:
                diff_J = abs(prev_J - J_min)
                J_r.append(J_min)
                means_r.append(means)
                print(J_min)
                if diff_J < 30:
                    break
                else:
                    prev_J = J_min
            k += 1

        # Returns number of means, the cost function for the best value & the mean values in vector means
        print("final number of clusters", k)
        return k, J_r, means_r, final_cluster