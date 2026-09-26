import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import pchip_interpolate

st.set_page_config(page_title="Summer Temperatures Distribution", layout="wide")

st.title("Summer Temperature Distribution Shift")
st.write("Interactive replication of the NYT/NASA Northern Hemisphere summer temperature distribution comparison.")

# Sidebar controls for interactivity
st.sidebar.header("Plot Parameters")
noise_level = st.sidebar.slider("Noise Intensity", min_value=0.000, max_value=0.040, value=0.015, step=0.002)
shift_offset = st.sidebar.slider("Temperature Shift Offset (2013–2023)", min_value=0.5, max_value=2.0, value=1.25, step=0.05)
opacity = st.sidebar.slider("Distribution Opacity", min_value=0.3, max_value=1.0, value=0.85, step=0.05)

# Initialize figure layout
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), facecolor='white')
fig.subplots_adjust(hspace=0.28)

np.random.seed(42)
x = np.linspace(-4.5, 5.5, 1200)

# 1951-1980 Reference Silhouette Control Points
x_pts1 = [-4.5, -3.2, -2.6, -2.1, -1.6, -1.2, -0.8, -0.4, 0.0,
          0.4, 0.8, 1.2, 1.6, 2.0, 2.5, 3.1, 3.11, 40]
y_pts1 = [0.00, 0.005, 0.015, 0.02, 0.07, 0.28, 0.55, 0.88, 1.05,
          0.87, 0.65, 0.35, 0.17, 0.05, 0.025, 0.0005, 0, 0]
y1_smooth = pchip_interpolate(x_pts1, y_pts1, x)

# 2013-2023 Reference Silhouette Control Points
x_pts2 = [-4.5, -3.0, -2.0, -1.2, -0.7, -0.3, 0.0, 0.2, 0.4, 0.6, 0.8,
         1.2, 1.4, 1.7, 2.0, 2.4, 2.6, 3.0, 4.0, 5.5]
y_pts2 = [0.00, 0.002, 0.008, 0.025, 0.07, 0.15, 0.25, 0.30, 0.50, 0.50,
          0.70, 0.82, 0.84, 0.79, 0.68, 0.53, 0.53, 0.30, 0.12, 0.00]
y2_smooth = pchip_interpolate(x_pts2, y_pts2, x)

# Apply interactive empirical noise & shift
noise1 = np.random.normal(0, noise_level * 0.8, size=len(x)) * np.exp(-0.2 * x**2)
y1 = np.clip(y1_smooth + noise1, 0, None)

noise2 = np.random.normal(0, noise_level, size=len(x)) * np.exp(-0.15 * (x - shift_offset)**2)
y2 = np.clip(y2_smooth + noise2, 0, None)

# Color Palette Matching NYT / NASA Visual Style
c_ext_cold = '#004B6E'
c_cold = '#6BA3C1'
c_normal = '#D6D6D6'
c_hot = '#E66E38'
c_ext_hot = '#C82B1D'

# Category Boundaries
b_ext_cold = -2.5
b_cold = -0.43
b_hot = 0.43
b_ext_hot = 2.5

def fill_distribution(ax, x_vals, y_vals, alpha=1.0):
    ax.fill_between(x_vals, y_vals, where=(x_vals < b_cold), color=c_cold, alpha=alpha, lw=0)
    ax.fill_between(x_vals, y_vals, where=((x_vals >= b_cold) & (x_vals < b_hot)), color=c_normal, alpha=alpha, lw=0)
    ax.fill_between(x_vals, y_vals, where=((x_vals >= b_hot) & (x_vals < b_ext_hot)), color=c_hot, alpha=alpha, lw=0)
    ax.fill_between(x_vals, y_vals, where=(x_vals >= b_ext_hot), color=c_ext_hot, alpha=alpha, lw=0)

for ax in (ax1, ax2):
    ax.set_facecolor('white')
    ax.set_xlim(-4.5, 5.5)
    ax.set_ylim(0, 1.25)
    ax.axis('off')

    for b in [b_ext_cold, b_cold, b_hot, b_ext_hot]:
        ax.plot([b, b], [0, 1.15], color='#E2E2E2', lw=0.8, zorder=1)

# Top Subplot: 1951-1980
fill_distribution(ax1, x, y1)
ax1.text(-4.4, 1.18, "Summer Temperatures", fontsize=11, fontweight='bold', color='#222222')
ax1.text(-4.4, 1.08, "June-July-August in the\nNorthern Hemisphere", fontsize=8.5, color='#888888')
ax1.text(3.3, 1.08, "1951-1980", fontsize=24, color='#333333')

ax1.annotate('', xy=(-4.1, 0.45), xytext=(-4.1, 0.25),
             arrowprops=dict(arrowstyle='->', color='#888888', lw=1.2))
ax1.text(-4.4, 0.17, "More frequent", fontsize=8.5, color='#888888')

ax1.annotate("1951-1980\n(base period)", xy=(-1.3, 0.33), xytext=(-2.3, 0.28),
             fontsize=8, color='#888888',
             arrowprops=dict(arrowstyle='-', color='#B0B0B0', lw=0.8))

# Bottom Subplot: 2013-2023
ax2.fill_between(x, y1, color='#E0E0E0', alpha=0.8, zorder=1)
ax2.plot(x, y1, color='#B0B0B0', lw=0.1, linestyle='--', zorder=1)

fill_distribution(ax2, x, y2, alpha=opacity)
ax2.text(-4.4, 1.18, "Summer Temperatures", fontsize=11, fontweight='bold', color='#222222')
ax2.text(-4.4, 1.08, "June-July-August in the\nNorthern Hemisphere", fontsize=8.5, color='#888888')
ax2.text(3.3, 1.08, "2013-2023", fontsize=24, color='#333333')

ax2.annotate('', xy=(-4.1, 0.45), xytext=(-4.1, 0.25),
             arrowprops=dict(arrowstyle='->', color='#888888', lw=1.2))
ax2.text(-4.4, 0.17, "More frequent", fontsize=8.5, color='#888888')

ax2.annotate("1951-1980\n(base period)", xy=(-1.3, 0.22), xytext=(-2.3, 0.17),
             fontsize=8, color='#888888',
             arrowprops=dict(arrowstyle='-', color='#B0B0B0', lw=0.8))

# X-axis Labels
labels = [
    (-3.8, "Extremely cold", c_ext_cold),
    (-1.0, "Cold", c_cold),
    (-0.1, "Normal", '#888888'),
    (1.1, "Hot", c_hot),
    (3.2, "Extremely hot", c_ext_hot)
]
for x_pos, text, col in labels:
    ax1.text(x_pos, -0.08, text, fontsize=9, color=col, fontweight='bold')
    ax2.text(x_pos, -0.08, text, fontsize=9, color=col, fontweight='bold')

plt.tight_layout()

# Render plot in Streamlit
st.pyplot(fig)
