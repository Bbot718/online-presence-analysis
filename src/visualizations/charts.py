import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from wordcloud import WordCloud
import plotly.graph_objects as go

class ChartGenerator:
    def __init__(self):
        plt.style.use('seaborn-v0_8-darkgrid')
        self.output_dir = Path("data/output/charts")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_pie_chart(self, data, title, filename):
        """Create a pie chart using matplotlib"""
        plt.figure(figsize=(10, 8))
        plt.pie(
            data.values(),
            labels=data.keys(),
            autopct='%1.1f%%',
            colors=sns.color_palette("husl", len(data)),
            startangle=90
        )
        plt.title(title)
        plt.axis('equal')
        
        return self._save_matplotlib_chart(filename)

    def create_gauge_chart(self, value, title, filename):
        """Create a gauge chart using plotly"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            title={'text': title},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 75], 'color': "gray"},
                    {'range': [75, 100], 'color': "darkgray"}
                ]
            }
        ))
        
        return self._save_plotly_chart(fig, filename)

    def create_bar_chart(self, data, title, filename):
        """Create a bar chart using matplotlib"""
        plt.figure(figsize=(10, 6))
        plt.bar(data.keys(), data.values())
        plt.title(title)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        return self._save_matplotlib_chart(filename)

    def create_word_cloud(self, text, title, filename):
        """Create a word cloud visualization"""
        wordcloud = WordCloud(
            width=800, 
            height=400,
            background_color='white',
            max_words=100,
            contour_width=3,
            contour_color='steelblue'
        ).generate(text)
        
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(title)
        
        return self._save_matplotlib_chart(filename)

    def create_spider_chart(self, scores):
        """Create spider/radar chart for scores"""
        categories = list(scores.keys())
        values = list(scores.values())
        
        angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False)
        values += values[:1]
        angles = np.concatenate((angles, [angles[0]]))
        
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        ax.plot(angles, values)
        ax.fill(angles, values, alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        plt.title("Score Overview")
        
        return self._save_matplotlib_chart("spider_chart")

    def create_stacked_bar(self, data, categories, title, filename):
        """Create a stacked bar chart"""
        plt.figure(figsize=(12, 6))
        bottom = np.zeros(len(data[list(data.keys())[0]]))
        
        for category in categories:
            values = data[category]
            plt.bar(range(len(values)), values, bottom=bottom, label=category)
            bottom += values
        
        plt.title(title)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        
        return self._save_matplotlib_chart(filename)

    def _save_matplotlib_chart(self, filename):
        """Save matplotlib chart to file"""
        filepath = self.output_dir / f"{filename}.png"
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()
        return filepath

    def _save_plotly_chart(self, fig, filename):
        """Save plotly chart to file"""
        filepath = self.output_dir / f"{filename}.png"
        fig.write_image(str(filepath))
        return filepath