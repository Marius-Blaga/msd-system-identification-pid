import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

class Visualizer:
    """
    Handles plotting and automatic saving of figures.
    All plots are saved in the 'figures/' directory.
    """

    def __init__(self, save_path: str = "figures"):
        self.save_path = save_path
        os.makedirs(save_path, exist_ok=True)

    def plot_response(self, t, x, title="Step Response",
                      filename="step_response.png",
                      xlabel="Time (s)",
                      ylabel="Displacement (m)",
                      show=True):

        if len(t) != len(x):
            raise ValueError("t and x must have same length")

        plt.figure()
        plt.plot(t, x, linewidth=2.5, label="Position")

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True, alpha=0.3)
        plt.legend()

        save_full_path = os.path.join(self.save_path, filename)
        plt.savefig(save_full_path, dpi=300, bbox_inches='tight')

        if show:
            plt.show()

        plt.close()
        return save_full_path