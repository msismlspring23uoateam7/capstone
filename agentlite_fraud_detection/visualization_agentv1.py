import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd
from agentlite.actions.BaseAction import BaseAction

class VisualizationAgent:
    def __init__(self):
        pass

    def visualize_data(self, data, sample_size=2000):
        if len(data) > sample_size:
            data=data.sample(n=sample_size)
        # Automatically detect if data is large or small
        if data.shape[1] <= 10:  # Fewer columns, use pairplot for correlation
            plt.figure(figsize=(14, 7))
            sns.pairplot(data)
            plt.title('Pairwise Relationships Between Features')
            plt.show()
        else:
            # If there are many columns, use dimensionality reduction techniques
            self.visualize_with_tsne(data)

    def visualize_correlation_matrix(self, data):
        plt.figure(figsize=(12, 8))
        sns.heatmap(data.corr(), annot=True, fmt='.2f', cmap='coolwarm')
        plt.title('Correlation Matrix')
        plt.show()

    def visualize_with_tsne(self, data):
        from sklearn.manifold import TSNE
        tsne = TSNE(n_components=2, random_state=42)
        tsne_result = tsne.fit_transform(data)
        tsne_df = pd.DataFrame(tsne_result, columns=['TSNE1', 'TSNE2'])

        plt.figure(figsize=(14, 7))
        sns.scatterplot(x='TSNE1', y='TSNE2', data=tsne_df)
        plt.title('t-SNE Visualization')
        plt.show()

    def advanced_visualization(self, data):
        # Example: Dynamic scatter plot using Plotly
        fig = px.scatter_matrix(data, dimensions=data.columns, title='Scatter Matrix Plot')
        fig.show()