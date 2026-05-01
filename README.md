# 🩺 GlucoSim — Glucose Meal Impact Simulator

<div align="center">

![GlucoSim Banner](https://img.shields.io/badge/GlucoSim-Predictive%20Health%20Analytics-7c3aed?style=for-the-badge&logo=heart&logoColor=white)

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-GitHub%20Pages-06b6d4?style=for-the-badge)](https://olivechaitanya.github.io/GlucoSim/)
[![HTML](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=flat&logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)

**Simulate how Indian foods & medications affect your blood glucose levels — powered by pharmacokinetic modeling.**

[🌐 Live Demo](https://olivechaitanya.github.io/GlucoSim/) · [📋 Report Bug](https://github.com/olivechaitanya/GlucoSim/issues) · [💡 Request Feature](https://github.com/olivechaitanya/GlucoSim/issues)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🍛 **60+ Indian Foods** | Comprehensive database with GI, GL, carbs, fiber, fat, protein |
| 🧪 **Pharmacokinetic Modeling** | Real glucose absorption/clearance simulation using convolution |
| 💊 **Medication Simulation** | Metformin, Sulfonylureas, DPP-4, SGLT2 Inhibitors, Insulin |
| 📈 **Interactive Charts** | Steady, fixed-axis glucose projection chart via Chart.js |
| 🎯 **Smart Metrics** | Peak glucose, time-to-peak, return-to-baseline, time-in-range |
| 🌑 **Premium Dark UI** | Glassmorphism, particle canvas, 3D card tilt, magnetic buttons |
| 📱 **Fully Responsive** | Works seamlessly across desktop and mobile devices |

---

## 🖥️ Live Demo

> **[🚀 Open GlucoSim →](https://olivechaitanya.github.io/GlucoSim/)**

---

## 🚀 Getting Started

### Run Locally

```bash
# Clone the repository
git clone https://github.com/olivechaitanya/GlucoSim.git
cd GlucoSim

# Serve locally (Python)
python -m http.server 8080

# Open in browser
# Navigate to http://localhost:8080
```

No build step required — pure HTML, CSS, and JavaScript!

---

## 🧪 How It Works

GlucoSim uses a **pharmacokinetic (PK) model** to simulate postprandial glucose response:

```
1. 🍽️  Food Selection  →  Carb/GI data lookup
2. 📐  Absorption Rate  →  ka = 0.015 + 0.0006 × GI (modulated by fat/protein)
3. 🧬  Glucose Response  →  Convolution of absorption × clearance kernel
4. 💊  Medication Effect  →  Gaussian profile by drug type & dose
5. 📊  Final Curve  →  Baseline + ΣFood_Δ − Medication_Effect
```

**Key parameters modeled:**
- Glycemic Index (GI) & Glycemic Load (GL)
- Fiber's carbohydrate absorption reduction
- Fat & protein slowing of gastric emptying
- Body weight–adjusted insulin sensitivity
- Activity level's impact on glucose uptake

---

## 📸 Screenshots

> *(Add screenshots here after deploying)*

---

## 🗂️ Project Structure

```
GlucoSim/
├── index.html          # Main application UI
├── app.js              # Simulation logic + Chart.js rendering
├── styles.css          # Premium dark-mode glassmorphism styles
└── README.md           # This file
```

---

## ⚙️ Tech Stack

- **Frontend:** HTML5, Vanilla CSS3, Vanilla JavaScript (ES6+)
- **Charts:** [Chart.js 4.4](https://www.chartjs.org/) + [chartjs-plugin-annotation](https://www.chartjs.org/chartjs-plugin-annotation/)
- **Fonts:** Google Fonts (Inter)
- **Hosting:** GitHub Pages

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## ⚠️ Disclaimer

> This tool is for **educational purposes only**. The predictions are based on simplified pharmacokinetic models and individual responses may vary significantly. **Always consult your healthcare provider** for medical advice regarding diabetes management.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">

Made with ❤️ for diabetic health awareness

**[⭐ Star this repo](https://github.com/olivechaitanya/GlucoSim)** if you found it helpful!

</div>
