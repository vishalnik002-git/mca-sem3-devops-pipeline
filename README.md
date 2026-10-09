[![MCA DevOps CI/CD Pipeline](https://github.com/vishalnik002-git/mca-sem3-devops-pipeline/actions/workflows/pipeline.yml/badge.svg)](https://github.com/vishalnik002-git/mca-sem3-devops-pipeline/actions)

# DevOps Pipeline Optimization System
**MCA 3rd Semester Project (Academic Session 2026-2027)**  
**School of Computer Application and Technology, Galgotias University**

---

### 📌 Project Overview
The **DevOps Pipeline Optimization System** is designed to automate and streamline the software delivery lifecycle. It integrates modern DevOps practices including automated builds, containerization, Infrastructure as Code (IaC), and cloud deployment to eliminate manual errors, optimize resource utilization, and accelerate deployment cycles.

---

### 👥 Project Team
* **Vishal Yadav** (Admission No: 25SCSE2030186 | Enrollment No: 25132030877)
* **Satyam Tiwari** (Admission No: 25SCSE2030189 | Enrollment No: 25132030794)
* **Rohit Baghel** (Admission No: 25SCSE2030104 | Enrollment No: 25132030769)

**Project Guide:** Dr. Deepak Kumar Panda  
**Program:** Master of Computer Applications (MCA Core, 3rd Semester)

---

### 🛠️ Tech Stack & Tools
* **Version Control:** Git, GitHub
* **CI/CD Pipeline:** GitHub Actions
* **Containerization:** Docker
* **Infrastructure as Code (IaC):** Terraform
* **Cloud Platform:** Microsoft Azure (Azure App Service, Azure Container Registry)
* **Backend Application:** Python (Flask)

---

### 🏗️ Architecture & Pipeline Flow
1. **Source Code & Commit:** Developers commit code changes to GitHub repository (`main` branch).
2. **Continuous Integration (GitHub Actions):** Triggered automatically on push; sets up Python environment and installs dependencies.
3. **Container Build & Registry:** Docker image is built and pushed to **Azure Container Registry (ACR)**.
4. **Cloud Infrastructure (IaC):** **Terraform** manages resource groups, ACR, Service Plan, and Azure Linux Web App.
5. **Continuous Deployment:** Azure Web App pulls latest image from ACR and serves the live Flask application.

---

### 📁 Project Structure
```text
.
├── .github/
│   └── workflows/
│       └── pipeline.yml        # GitHub Actions CI/CD pipeline definition
├── terraform/
│   ├── main.tf                 # Terraform infrastructure configuration (Azure)
│   ├── variable.tf             # Terraform input variables
│   └── .terraform.lock.hcl     # Terraform provider lock
├── app.py                      # Flask web application
├── Dockerfile                  # Containerization file
├── .gitignore                  # Git ignore rules
├── DevOps_Pipeline_Optimization_System_FINAL_Major_Project_Report.pdf  # Project Report (PDF)
├── DevOps_Pipeline_Optimization_System_FINAL_Major_Project_Report.docx # Project Report (DOCX)
└── README.md                   # Project documentation
```

---

### 🚀 Getting Started (Local Setup)

#### 1. Clone the repository
```bash
git clone https://github.com/vishalnik002-git/mca-sem3-devops-pipeline.git
cd mca-sem3-devops-pipeline
```

#### 2. Run Application Locally
```bash
# Create and activate virtual environment (optional)
python -m venv venv
venv\Scripts\activate      # Windows

# Install Flask dependencies
pip install flask

# Run application
python app.py
```
Visit `http://localhost:5000` in your browser.

#### 3. Run with Docker
```bash
# Build Docker image
docker build -t mca-devops-app:latest .

# Run container
docker run -d -p 5000:5000 --name devops-app mca-devops-app:latest
```

#### 4. Infrastructure as Code (Terraform)
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

---

### 📄 Documentation & Reports
- Detailed Project Report: [`DevOps_Pipeline_Optimization_System_FINAL_Major_Project_Report.pdf`](./DevOps_Pipeline_Optimization_System_FINAL_Major_Project_Report.pdf)