import matplotlib.pyplot as plt
import seaborn as sns
import os

# Global settings for professional-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12


class Visualizer:
    """
    Class for managing visualizations and automatically saving plots.
    All figures are saved in the 'figures/' folder at the project root.
    """
    
    def __init__(self, save_path: str = None):
        if save_path is None:
            # Determine project root regardless of where the notebook is run from
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.abspath(os.path.join(current_dir, ".."))
            self.save_path = os.path.join(project_root, "figures")
        else:
            self.save_path = save_path
        
        # Create the folder if it doesn't exist
        os.makedirs(self.save_path, exist_ok=True)
        print(f"✅ Plots will be saved in folder: {self.save_path}")
    
    def plot_response(self, t, x, title: str = "Step Response", 
                     filename: str = "step_response.png", 
                     xlabel: str = "Time (s)", 
                     ylabel: str = "Displacement (m)",
                     show: bool = True):
        """
        Plot the system response and save it automatically.
        """
        plt.figure()
        plt.plot(t, x, 'b-', linewidth=2.5, label='Position')
        plt.title(title, fontsize=14, pad=15)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Automatic saving
        save_full_path = os.path.join(self.save_path, filename)
        plt.savefig(save_full_path, dpi=300, bbox_inches='tight')
        print(f"   📊 Plot saved: {save_full_path}")
        
        if show:
            plt.show()
        plt.close()
    
    def compare_responses(self, t, responses_dict, title="Comparison of responses", 
                         filename="comparison.png"):
        """
        Plot multiple responses on the same graph.
        responses_dict = {'Name1': x1, 'Name2': x2, ...}
        """
        plt.figure()
        for label, x in responses_dict.items():
            plt.plot(t, x, linewidth=2, label=label)
        
        plt.title(title, fontsize=14)
        plt.xlabel("Time (s)")
        plt.ylabel("Displacement (m)")
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        save_full_path = os.path.join(self.save_path, filename)
        plt.savefig(save_full_path, dpi=300, bbox_inches='tight')
        print(f"   📊 Comparative plot saved: {save_full_path}")
        
        plt.show()
        plt.close()