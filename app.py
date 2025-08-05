# app.py
import streamlit as st
import numpy as np
from numpy.linalg import inv
from math import acos, degrees
from symmetry_operators import get_cubic_symmetry_operators
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ----------------------------------------
# Function: Get Rotation Axis and Angle
# ----------------------------------------
def get_rotation_axis_angle(M):
    """
    Given a 3x3 misorientation matrix, return the rotation axis (unit vector)
    and rotation angle in degrees.
    """
    angle_rad = acos(np.clip((np.trace(M) - 1) / 2, -1.0, 1.0))
    angle_deg = degrees(angle_rad)

    rx = M[2, 1] - M[1, 2]
    ry = M[0, 2] - M[2, 0]
    rz = M[1, 0] - M[0, 1]
    axis = np.array([rx, ry, rz])
    norm = np.linalg.norm(axis)

    if norm == 0:
        axis = np.array([0, 0, 0])
    else:
        axis = axis / norm

    return axis, angle_deg

# ----------------------------------------
# Function: Plot Rotation Axis on Sphere
# ----------------------------------------
def plot_rotation_axis(axis):
    """Plot the rotation axis as a vector on a unit sphere."""
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Unit sphere
    u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:25j]
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)
    ax.plot_surface(x, y, z, color='lightblue', alpha=0.2, edgecolor='gray')

    # Rotation axis vector (both directions)
    ax.quiver(0, 0, 0, axis[0], axis[1], axis[2], color='red', linewidth=2)
    ax.quiver(0, 0, 0, -axis[0], -axis[1], -axis[2], color='red', linewidth=2, linestyle='dotted')

    ax.set_title("Rotation Axis (Red)")
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_box_aspect([1, 1, 1])

    return fig

# ----------------------------------------
# Function: Misorientation
# ----------------------------------------
def calculate_misorientation(gA, gB):
    M = np.dot(gB, inv(gA))
    cos_theta = (np.trace(M) - 1) / 2
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    angle_rad = acos(cos_theta)
    angle_deg = degrees(angle_rad)
    return M, angle_deg

# ----------------------------------------
# Function: Disorientation using Symmetry
# ----------------------------------------
def calculate_disorientation(gA, gB):
    symmetry_ops = get_cubic_symmetry_operators()
    min_angle = 180.0

    for Oc1 in symmetry_ops:
        for Oc2 in symmetry_ops:
            M = np.dot(Oc1, np.dot(np.dot(gB, inv(gA)), Oc2))
            cos_theta = (np.trace(M) - 1) / 2
            cos_theta = np.clip(cos_theta, -1.0, 1.0)
            angle_rad = acos(cos_theta)
            angle_deg = degrees(angle_rad)
            if angle_deg < min_angle:
                min_angle = angle_deg

    return min_angle

# ----------------------------------------
# Streamlit App UI
# ----------------------------------------
st.set_page_config(page_title="Grain Misorientation Calculator", layout="centered")
st.title("🧊 Grain Misorientation & Disorientation Calculator")
st.markdown("Enter or upload orientation matrices to compute misorientation and disorientation between two grains.")

# Default matrix input
st.subheader("🧮 Input Orientation Matrices")
default_gA = "[[1, 0, 0], [0, 1, 0], [0, 0, 1]]"
default_gB = "[[0, -1, 0], [1, 0, 0], [0, 0, 1]]"
gA_input = st.text_area("Matrix gA (3x3):", default_gA)
gB_input = st.text_area("Matrix gB (3x3):", default_gB)

try:
    gA = np.array(eval(gA_input))
    gB = np.array(eval(gB_input))

    if gA.shape != (3, 3) or gB.shape != (3, 3):
        st.error("❌ Both matrices must be 3x3.")
    else:
        if st.button("🔍 Compute Misorientation & Disorientation"):
            # Compute misorientation
            M, mis_angle = calculate_misorientation(gA, gB)

            # Compute disorientation
            dis_angle = calculate_disorientation(gA, gB)

            # Compute and plot rotation axis
            axis, _ = get_rotation_axis_angle(M)
            fig = plot_rotation_axis(axis)

            # Display results
            st.success("✅ Computation Successful")
            st.subheader("📊 Results")
            st.write("**Misorientation Matrix (M):**")
            st.write(M)
            st.metric("Misorientation Angle (°)", f"{mis_angle:.2f}")
            st.metric("Minimum Disorientation Angle (°)", f"{dis_angle:.2f}")

            # Display plot
            st.subheader("🧭 Rotation Axis Visualization")
            st.pyplot(fig)
            st.markdown(f"**Rotation Axis (unit vector):** `{axis}`")

except Exception as e:
    st.error(f"❌ Error parsing input: {e}")
