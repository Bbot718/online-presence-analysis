def create_performance_visualization(self, metrics):
    """Create performance visualizations using free Google PageSpeed data"""
    # Gauge Chart for Overall Score
    gauge_chart = self.chart_generator.create_gauge_chart(
        value=metrics['performance_score'],
        title="Performance Score",
        filename="performance_gauge"
    )
    
    # Core Web Vitals Bar Chart
    vitals_data = {
        'FCP': metrics['first_contentful_paint'] / 1000,
        'LCP': metrics['largest_contentful_paint'] / 1000,
        'TBT': metrics['total_blocking_time'],
        'CLS': metrics['cumulative_layout_shift'] * 100
    }
    bar_chart = self.chart_generator.create_bar_chart(
        data=vitals_data,
        title="Core Web Vitals",
        filename="core_web_vitals"
    ) 