import math
import random
from math import floor

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Patch
from pandas.errors import SettingWithCopyWarning
from sklearn.manifold import TSNE
from wordcloud import WordCloud

from chester.zero_break.problem_specification import DataInfo


class CategoricalPreModelAnalysis:
    def __init__(self, data_info: DataInfo):
        self.data_info = data_info
        self.cols = self.data_info.feature_types_val["categorical"]
        self.n_cols = len(self.cols)
        self.target = self.data_info.data[self.data_info.target]
        self.target_df = self.data_info.data[[self.data_info.target]]
        self.data = self.data_info.data[self.cols]
        # calc
        self.cols_sorted = self.sort_by_pvalue()
        self.cols_sorted_with_pvalue = None

    def tsne(self):
        X_tsne_3d = TSNE(n_components=3).fit_transform(pd.get_dummies(self.data))
        X_tsne_2d = X_tsne_3d[:, :2]

        fig = plt.figure(figsize=(16, 8))
        ax1 = plt
        # ax2 = fig.add_subplot(122, projection='3d')
        if self.data_info.problem_type_val in ["Regression"]:
            ax1.hexbin(X_tsne_2d[:, 0], X_tsne_2d[:, 1], C=self.target, gridsize=50, cmap='viridis', edgecolors='black')
            # ax2.scatter(X_tsne_3d[:, 0], X_tsne_3d[:, 1], X_tsne_3d[:, 2], c=self.target, cmap='viridis')
            ax1.title("Visualizing Categorical Features and Target with t-SNE (2D)")
            # ax2.set_title("Visualizing Categorical Features and Target with t-SNE (3D)")
        elif self.data_info.problem_type_val in ["Binary regression", "Binary classification"]:
            target_classes = self.target.unique()
            color_map = {target_class: color for target_class, color in zip(target_classes, ['red', 'blue'])}
            colors = self.target.apply(lambda x: color_map[x])
            ax1.scatter(X_tsne_2d[:, 0], X_tsne_2d[:, 1], c=colors)
            # ax2.scatter(X_tsne_3d[:, 0], X_tsne_3d[:, 1], X_tsne_3d[:, 2], c=colors)
            legend_handles = [Patch(color=color_map[target_class], label=target_class) for target_class in
                              target_classes]
            ax1.title("Visualizing Categorical Features and Target with t-SNE (2D)")
            # ax2.set_title("Visualizing Categorical Features and Target with t-SNE (3D)")
            ax1.legend(handles=legend_handles)
        else:  # Multi-class classification
            target_classes = self.target.unique()
            color_map = {target_class: color for target_class, color in
                         zip(target_classes, plt.cm.rainbow(np.linspace(0, 1, len(target_classes))))}
            ax1.legend(
                handles=[Patch(color=color_map[target_class], label=target_class) for target_class in target_classes])
            # ax2.legend(
            #     handles=[Patch(color=color_map[target_class], label=target_class) for target_class in target_classes])

    def any_categorical(self):
        return True if len(self.cols) > 0 else False

    def sort_by_pvalue(self):
        from sklearn.cluster import KMeans
        from scipy.stats import chi2_contingency
        import warnings
        warnings.simplefilter("ignore")

        problem_type = self.data_info.problem_type_val

        if problem_type in ["Regression"]:
            num_groups = min(floor(self.data_info.rows / 20), 10)
            kmeans = KMeans(n_clusters=num_groups, n_init=10)
            kmeans.fit(self.target_df)
            target_labels = kmeans.labels_

        feature_pvalue_list = []
        for col in self.cols:
            data_col = self.data[col]
            if problem_type == "Regression":
                contingency_table = pd.crosstab(data_col, columns=target_labels)
                chi2, pvalue, _, _ = chi2_contingency(contingency_table)
            else:
                contingency_table = pd.crosstab(index=data_col, columns=self.target)
                chi2, pvalue, _, _ = chi2_contingency(contingency_table)
            feature_pvalue_list.append((col, pvalue))

        sorted_list = sorted(feature_pvalue_list, key=lambda x: x[1], reverse=False)
        self.cols_sorted_with_pvalue = sorted_list
        return [x[0] for x in sorted_list]

    def analyze_pvalue(self, is_plot=True, top_features=10):
        self.sort_by_pvalue()
        if len(self.cols) == 0:
            return None
        self.plot_wordcloud_pvalues(self.cols_sorted_with_pvalue)
        if is_plot:
            if self.n_cols > 50:
                print("plotting!")
                self.plot_histogram_pvalues(self.cols_sorted_with_pvalue)
        print("Pvalues for top categorical features:")
        print(pd.DataFrame(self.cols_sorted_with_pvalue[0:top_features], columns=["feature", "pvalue"]))

    def partial_plot(self, classification_row_percent=True):
        import warnings
        warnings.simplefilter("ignore")
        top_features = 25

        if self.n_cols <= 25:
            sample_features = self.n_cols
            top_features = self.n_cols
        else:
            sample_features = min(2 * 25, int(self.n_cols / 2))
        top_feature_names = random.sample(self.cols_sorted[0:top_features], sample_features)
        feature_index = {feature: index for index, feature in enumerate(self.cols_sorted[0:top_features])}
        top_feature_names.sort(key=lambda x: feature_index[x])
        if self.data_info.problem_type_val in ["Binary regression", "Binary classification"]:
            max_plots = 9
            top_n = self.data[:top_features].columns
            dim = math.ceil(math.sqrt(len(top_n)))
            num_rows = math.ceil(max_plots / dim)
            fig, ax = plt.subplots(dim, dim)
            fig.tight_layout()
            if classification_row_percent:
                plt.suptitle("Partial Plot to Identify Patterns between Sampled Categorical Features and Target\n"
                             "Showing % from Feature (row)",
                             fontsize=14, fontweight='bold')
            else:
                plt.suptitle("Partial Plot to Identify Patterns between Sampled Categorical Features and Target\n"
                             "Showing % from Target (column)",
                             fontsize=14, fontweight='bold')
            for i, col in enumerate(top_feature_names):
                if i >= num_rows * num_rows:
                    return None
                ax_i = ax[i // dim, i % dim]
                if classification_row_percent:
                    crosstab = pd.crosstab(self.data[col], self.target, normalize='index') * 100
                    crosstab = crosstab[(crosstab.T != 0).any()]
                    crosstab = crosstab.loc[:, (crosstab != 0).any(axis=0)]
                    crosstab = crosstab.loc[crosstab.sum(axis=1).sort_values(ascending=False).index[:5]]
                else:
                    crosstab = pd.crosstab(self.data[col], self.target, normalize='columns') * 100
                    crosstab = crosstab[(crosstab.T != 0).any()]
                    crosstab = crosstab.loc[:, (crosstab != 0).any(axis=0)]
                    crosstab = crosstab.loc[crosstab.sum(axis=1).sort_values(ascending=False).index[:5]]
                sns.heatmap(crosstab, annot=False, cmap="YlGnBu", fmt='g', ax=ax_i)
                ax_i.set_ylabel(None)
                ax_i.set_xlabel(None)
                ax_i.set_title(col, fontsize=12, fontweight='bold')
            plt.tight_layout()
            plt.show()
        if self.data_info.problem_type_val in ["Regression"]:
            from sklearn.cluster import KMeans
            target = self.target
            kmeans = KMeans(n_clusters=10)
            kmeans.fit(self.target_df)
            target_labels = kmeans.labels_
            plt.figure(figsize=(12, 12))
            plt.suptitle("Partial Plot to Identify Patterns between Categorical Sampled Features and Target",
                         fontsize=16,
                         fontweight='bold')
            grid_size = 4
            num_features = min(grid_size * grid_size, top_features)
            num_rows = int(np.ceil(num_features / grid_size))
            for i, col in enumerate(top_feature_names[:num_features]):
                plt.subplot(num_rows, grid_size, i + 1)
                column = self.data[col]
                if column.dtype == "object":
                    column = column.astype("category").cat.codes
                    column = column[column < 5]
                crosstab = pd.crosstab(target_labels, column, normalize='index')
                sns.heatmap(crosstab, annot=False, cmap='Greens', cbar=True)
                plt.ylabel("Clusters")
                plt.xlabel("{} Value".format(col))
                plt.subplots_adjust(hspace=0.5, wspace=0.5)
        elif self.data_info.problem_type_val in ["Multiclass classification"]:
            plt.figure(figsize=(16, 16))
            plt.suptitle(
                "Heatmap to Show Correlation between Sampled Categorical Features (top 5 categories) and Target",
                fontsize=16,
                fontweight='bold')
            top_features = 16
            top_feature_names = self.data[:top_features].columns
            rows = 4
            cols = 4
            for i, col in enumerate(top_feature_names):
                if i > 15:
                    return None
                plt.subplot(rows, cols, i + 1)
                crosstab = pd.crosstab(self.data[col], self.target, normalize='index') * 100
                crosstab = crosstab[(crosstab.T != 0).any()]
                crosstab = crosstab.loc[:, (crosstab != 0).any(axis=0)]
                crosstab = crosstab.loc[crosstab.sum(axis=1).sort_values(ascending=False).index[:5]]
                sns.heatmap(crosstab, annot=False, cmap="YlGnBu", fmt='g')
                plt.title(col, fontsize=12, fontweight='bold')
            plt.show()
            return None

    @staticmethod
    def plot_histogram_pvalues(features_pvalues):
        """
        Plot histogram of p-values for features.
        :param features_pvalues: List of tuples (column name, pvalue).
        :return: None.
        """
        pvalues = [pvalue for _, pvalue in features_pvalues]
        fig, ax = plt.subplots()
        ax.hist(pvalues, bins=50, edgecolor='k', color='#2ecc71')
        ax.set_title("Histogram of P-values for Categorical Features", fontsize=16)
        ax.set_xlabel("P-value", fontsize=14)
        ax.set_ylabel("Frequency", fontsize=14)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_linewidth(0.5)
        ax.spines['bottom'].set_linewidth(0.5)
        ax.tick_params(axis='both', which='both', labelsize=12)
        plt.show()
        return None

    @staticmethod
    def plot_wordcloud_pvalues(features_pvalues,
                               title="Categorical Features Pvalues Based on Partial Plot"):
        """
        Plot word cloud of features weighted by their p-value.
        :param features_pvalues: List of tuples (column name, pvalue).
        :param title: Title of the plot.
        :return: None.
        """
        features_pvalues = [(feature, 1 - pvalue) for feature, pvalue in features_pvalues]
        wordcloud = WordCloud(
            random_state=21,
            normalize_plurals=True).generate_from_frequencies(dict(features_pvalues))
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.title(title, fontsize=15)
        plt.show()
        return None

    def run(self, is_plot=True):
        if self.n_cols > 1:
            self.analyze_pvalue(is_plot=is_plot)
            if is_plot:
                if 'classification' or 'binary regression' in self.data_info.problem_type_val.lower():
                    self.partial_plot(classification_row_percent=False)
                    self.partial_plot(classification_row_percent=True)
                else:
                    self.partial_plot()
                self.tsne()
        elif self.n_cols == 1:
            self.analyze_pvalue(is_plot=is_plot)
            if is_plot:
                self.partial_plot()
        return None


def format_df(df, max_value_width=10, ci_max_value_width=15, ci_col="CI"):
    pd.options.display.max_columns = None

    def trim_value(val):
        if len(str(val)) > max_value_width:
            return str(val)[:max_value_width] + "..."
        return str(val)

    def trim_ci_value(val):
        if len(str(val)) > ci_max_value_width:
            return str(val)[:ci_max_value_width] + "..."
        return str(val)

    df_subset = df.drop(ci_col, axis=1)
    df_subset = df_subset.applymap(trim_value)
    df[df_subset.columns] = df_subset
    df[ci_col] = df[ci_col].apply(trim_ci_value)

    return df
