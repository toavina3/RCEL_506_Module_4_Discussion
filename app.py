import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import pchip_interpolate

# Set Streamlit page configuration
st.set_page_config(
    page_title="Summer Temperatures Distribution",
    layout="centered"
)

st.title("Interactive Summer Temperatures Distribution")
st.markdown("Explore how Northern Hemisphere summer temperature distributions shift over time relative to the 1951–1980 base period.")

# ---------------------------------------------------------
# Sidebar Interactive Parameters
# ---------------------------------------------------------
st.sidebar.header("Visualization Parameters")

# Parameter 1: Noise level scale
noise_factor = st.sidebar.slider(
    "1. Noise Scale Factor",
    min_value=0.0,
    max_value=2.0,
    value=1.0,
    step=0.1,
    help="Adjust the magnitude of empirical noise applied to both distribution curves."
)

# Parameter 2: Transparency of the 2nd curve
alpha_curve2 = st.sidebar.slider(
    "2. Transparency (Alpha) of 2nd Curve",
    min_value=0.0,
    max_value=1.0,
    value=0.85,
    step=0.05,
    help="Adjust the fill opacity of the bottom curve."
)

# Parameter 3: Transition from 1951-1980 to 2013-2023
transition_pct = st.sidebar.slider(
    "3. Period Transition (1951–1980 → 2013–2023)",
    min_value=0,
    max_value=100,
    value=100,
    step=1,
    format="%d%%",
    help="Interpolates linearly between the 1951–1980 baseline (0%) and 2013–2023 (100%)."
)

# ---------------------------------------------------------
# Data Processing & Curve Generation
# ---------------------------------------------------------
t = transition_pct / 100.0
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

# Noise profiles
noise1 = np.random.normal(0, 0.012 * noise_factor, size=len(x)) * np.exp(-0.2 * x**2)
y1 = np.clip(y1_smooth + noise1, 0, None)

noise2 = np.random.normal(0, 0.015 * noise_factor, size=len(x)) * np.exp(-0.15 * (x - 1.25)**2)
y2 = np.clip(y2_smooth + noise2, 0, None)

# Interpolated curve for the bottom subplot
y_bottom_smooth = (1 - t) * y1_smooth + t * y2_smooth
noise_interp = (1 - t) * noise1 + t * noise2
y_bottom = np.clip(y_bottom_smooth + noise_interp, 0, None)

# ---------------------------------------------------------
# Plot Rendering
# ---------------------------------------------------------
c_ext_cold = '#004B6E'
c_cold = '#6BA3C1'
c_normal = '#D6D6D6'
c_hot = '#E66E38'
c_ext_hot = '#C82B1D'

b_ext_cold = -2.5
b_cold = -0.43
b_hot = 0.43
b_ext_hot = 2.5

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), facecolor='white')
fig.subplots_adjust(hspace=0.28)

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

# Top Subplot: 1951-1980 Base Period
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

# Bottom Subplot: Transition Curve
# Ghost outline of 1951-1980 base period
ax2.fill_between(x, y1, color='#E0E0E0', alpha=0.8, zorder=1)
ax2.plot(x, y1, color='#B0B0B0', lw=0.1, linestyle='--', zorder=1)

# Dynamic bottom curve with adjusted transparency
fill_distribution(ax2, x, y_bottom, alpha=alpha_curve2)

# Dynamic text label based on interpolation progress
if t == 0:
    bottom_label = "1951-1980"
elif t == 1:
    bottom_label = "2013-2023"
else:
    start_yr = int(1951 + t * (2013 - 1951))
    end_yr = int(1980 + t * (2023 - 1980))
    bottom_label = f"Interp. ({start_yr}–{end_yr})"

ax2.text(-4.4, 1.18, "Summer Temperatures", fontsize=11, fontweight='bold', color='#222222')
ax2.text(-4.4, 1.08, "June-July-August in the\nNorthern Hemisphere", fontsize=8.5, color='#888888')
ax2.text(2.2, 1.08, bottom_label, fontsize=18 if len(bottom_label) > 10 else 24, color='#333333')

ax2.annotate('', xy=(-4.1, 0.45), xytext=(-4.1, 0.25),
             arrowprops=dict(arrowstyle='->', color='#888888', lw=1.2))
ax2.text(-4.4, 0.17, "More frequent", fontsize=8.5, color='#888888')

ax2.annotate("1951-1980\n(base period)", xy=(-1.3, 0.22), xytext=(-2.3, 0.17),
             fontsize=8, color='#888888',
             arrowprops=dict(arrowstyle='-', color='#B0B0B0', lw=0.8))

# X-axis Labels for both subplots
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
st.pyplot(fig)
