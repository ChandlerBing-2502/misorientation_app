# 🧊 Grain Misorientation & Disorientation Calculator

A web-based tool built using **Streamlit** to calculate and visualize:

- Misorientation matrix and angle between two grains
- Disorientation angle (considering cubic symmetry)
- 3D rotation axis on a unit sphere

---

## 🔍 Features

- Input 3×3 orientation matrices (`gA` and `gB`)
- Calculate misorientation matrix and misorientation angle
- Compute disorientation using cubic symmetry operators
- 3D visualization of the rotation axis on a unit sphere
- Deployable on Streamlit Cloud

---

## ⚙️ How to Run Locally

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/misorientation-app.git
cd misorientation_app

pip install -r requirements.txt
streamlit run app.py

# File Structure
misorientation_app/
├── app.py                   # Main Streamlit app
├── symmetry_operators.py    # Cubic symmetry matrix generators
├── requirements.txt         # Python dependencies
└── README.md                # Project info

🧠 Built With
Python 3
Streamlit
NumPy
Matplotlib

