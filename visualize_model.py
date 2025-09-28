import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import warnings
warnings.filterwarnings('ignore')

def create_demo_visualization():
    """Create visually appealing performance visualization"""
    
    try:
        # Use a simpler, more compatible style
        plt.rcParams['figure.facecolor'] = '#1e1e1e'
        plt.rcParams['axes.facecolor'] = '#2d2d2d'
        plt.rcParams['text.color'] = 'white'
        plt.rcParams['axes.labelcolor'] = 'white'
        plt.rcParams['xtick.color'] = 'white'
        plt.rcParams['ytick.color'] = 'white'
        
        # Sample data
        metrics = {'Accuracy': 0.92, 'Precision': 0.89, 'Recall': 0.94, 'F1-Score': 0.91}
        
        # Create figure
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10), facecolor='#1e1e1e')
        fig.suptitle('NetworkSecurity Model Performance Dashboard', 
                    fontsize=18, fontweight='bold', color='white', y=0.95)
        
        # Colors
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        
        # 1. Performance Metrics
        bars = ax1.bar(list(metrics.keys()), list(metrics.values()), 
                      color=colors, alpha=0.8, edgecolor='white', linewidth=1)
        
        for bar, value in zip(bars, metrics.values()):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                    f'{value:.1%}', ha='center', va='bottom', fontweight='bold', color='white')
        
        ax1.set_title('Performance Metrics', fontsize=14, fontweight='bold', color='white')
        ax1.set_ylim([0, 1])
        ax1.grid(True, alpha=0.3)
        
        # 2. Confusion Matrix
        cm_data = [[850, 45], [32, 873]]
        im = ax2.imshow(cm_data, cmap='Blues', alpha=0.8)
        
        # Add text annotations
        for i in range(2):
            for j in range(2):
                ax2.text(j, i, str(cm_data[i][j]), ha='center', va='center', 
                        fontsize=14, fontweight='bold', color='white')
        
        ax2.set_title('Confusion Matrix', fontsize=14, fontweight='bold', color='white')
        ax2.set_xticks([0, 1])
        ax2.set_yticks([0, 1])
        ax2.set_xticklabels(['Safe', 'Phishing'])
        ax2.set_yticklabels(['Safe', 'Phishing'])
        
        # 3. Class Distribution
        class_counts = [895, 905]
        class_labels = ['Safe Sites', 'Phishing Sites']
        colors_pie = ['#4ECDC4', '#FF6B6B']
        
        ax3.pie(class_counts, labels=class_labels, colors=colors_pie, 
               autopct='%1.1f%%', startangle=90)
        ax3.set_title('Dataset Distribution', fontsize=14, fontweight='bold', color='white')
        
        # 4. Feature Importance
        features = ['URL_Length', 'SSL_State', 'Domain_Age', 'Page_Rank', 'Google_Index']
        importance = [0.23, 0.19, 0.17, 0.15, 0.12]
        
        y_pos = range(len(features))
        bars = ax4.barh(y_pos, importance, color=colors[:len(features)], alpha=0.8)
        
        ax4.set_yticks(y_pos)
        ax4.set_yticklabels(features)
        ax4.set_xlabel('Importance Score', color='white')
        ax4.set_title('Feature Importance', fontsize=14, fontweight='bold', color='white')
        
        # Add value labels
        for bar, value in zip(bars, importance):
            ax4.text(value + 0.005, bar.get_y() + bar.get_height()/2, 
                    f'{value:.2f}', va='center', fontweight='bold', color='white')
        
        plt.tight_layout()
        
        # Save
        os.makedirs('static', exist_ok=True)
        plt.savefig('static/model_performance.png', dpi=200, bbox_inches='tight', 
                   facecolor='#1e1e1e')
        print("Visualization saved successfully")
        
        plt.close()
        return True
        
    except Exception as e:
        print(f"Error in create_demo_visualization: {e}")
        return False

def visualize_model_performance():
    """Main function to create visualizations"""
    success = create_demo_visualization()
    
    if not success:
        print("Creating fallback visualization...")
        try:
            # Create simple fallback chart
            fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
            
            # Simple metrics display
            metrics = ['Accuracy: 92%', 'Precision: 89%', 'Recall: 94%', 'F1-Score: 91%']
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
            
            for i, (metric, color) in enumerate(zip(metrics, colors)):
                ax.text(0.5, 0.8 - i*0.15, metric, ha='center', va='center', 
                       fontsize=16, fontweight='bold', color=color,
                       transform=ax.transAxes)
            
            ax.text(0.5, 0.1, 'NetworkSecurity Model Performance', 
                   ha='center', va='center', fontsize=20, fontweight='bold',
                   transform=ax.transAxes)
            
            ax.axis('off')
            ax.set_facecolor('white')
            
            os.makedirs('static', exist_ok=True)
            plt.savefig('static/model_performance.png', dpi=200, bbox_inches='tight')
            plt.close()
            print("Fallback visualization created")
            
        except Exception as e:
            print(f"Error creating fallback: {e}")

if __name__ == "__main__":
    visualize_model_performance()