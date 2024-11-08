import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator


def normalize_score_with_direction(series, higher_is_better=True):
    """
    Normalize scores considering whether higher or lower values are better
    """
    if higher_is_better:
        return (series - series.min()) / (series.max() - series.min())
    else:
        return 1 - (series - series.min()) / (series.max() - series.min())


def style_axis(ax):
    ax.tick_params(axis='both', which='major', length=8, width=1.5, direction='in', color='#2c3e50')
    ax.tick_params(axis='both', which='minor', length=4, width=1, direction='in', color='#2c3e50')
    
    # Add minor ticks
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    
    # Style spines
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)
        spine.set_color('#2c3e50')
        spine.set_position(('outward', 5))
    
    # Adjust font properties
    ax.set_xlabel('Sequence Length', fontsize=12, fontname='Arial', color='#2c3e50', fontweight='bold')
    ax.set_ylabel('Integrated Score', fontsize=12, fontname='Arial', color='#2c3e50', fontweight='bold')
    
    # Style tick labels
    ax.tick_params(axis='both', which='major', labelsize=10, labelcolor='#2c3e50')
    
    return ax


def create_joint_plot(df):
    """
    Create joint plot with density and histograms
    """
    plt.style.use('seaborn-v0_8-white')
    plt.rcParams['font.family'] = 'Arial'
    
    # Create joint plot
    g = sns.JointGrid(data=df, 
                      x='seq_length', 
                      y='integrated_score',
                      marginal_ticks=True,
                      xlim=(40, 180),
                      height=10,
                      ratio=8)
    
    # Add density plot in center
    g.plot_joint(sns.kdeplot,
                 cmap="coolwarm",
                 fill=True,
                 levels=20,
                 alpha=0.95,
                 bw_adjust=0.5)
    
    # Add histograms on the sides with custom colors
    g.plot_marginals(sns.histplot, 
                    bins=30,
                    color='#34495e',
                    alpha=0.6)
    
    # Remove axes from histograms
    g.ax_marg_x.tick_params(labelbottom=False, labelleft=False)
    g.ax_marg_y.tick_params(labelbottom=False, labelleft=False)
    
    # Remove all spines from histograms
    for spine in g.ax_marg_x.spines.values():
        spine.set_visible(False)
    for spine in g.ax_marg_y.spines.values():
        spine.set_visible(False)
    
    # Style main plot
    g.ax_joint.grid(False)
    g.ax_joint = style_axis(g.ax_joint)
    
    formula_text = (
        r"$Score = \frac{1}{3}(ipTM_{norm} + (1-iPAE_{norm}) + ESM2_{norm})$" + "\n" +
        "Higher values indicate better performance"
    )
    
    g.ax_joint.text(0.45, 0.95, formula_text,
                    transform=g.ax_joint.transAxes,
                    fontsize=12,
                    fontname='Arial',
                    color='#2c3e50',
                    bbox=dict(facecolor='white', 
                             alpha=0.9, 
                             edgecolor='none',
                             pad=5),
                    verticalalignment='top')
    
    plt.tight_layout()
    plt.savefig('sequence_performance_joint.png', 
                dpi=300, 
                bbox_inches='tight', 
                facecolor='white',
                pad_inches=0.2)
    plt.close()


def main():
    df = pd.read_csv('ranked_metrics.csv')
    df['seq_length'] = df['seq'].str.len()
    df['norm_iptm'] = normalize_score_with_direction(df['i_ptm'], higher_is_better=True)
    df['norm_ipae'] = normalize_score_with_direction(df['i_pae'], higher_is_better=False)
    df['norm_esm'] = normalize_score_with_direction(df['esm_pll'], higher_is_better=True)
    df['integrated_score'] = (df['norm_iptm'] + df['norm_ipae'] + df['norm_esm']) / 3
    
    create_joint_plot(df)


if __name__ == "__main__":
    main()