# 🌾 Biomaterial Handling & Processing – Lab Course

This repository serves as the official portfolio and resource hub for the **Biomaterial Handling & Processing** course, consolidating weekly programming assignments and data analysis lab code.

> 📌 **[한국어 버전 (Korean Version)](../ko/README.md)** 도 제공됩니다.

## 📌 Repository Purpose & Structure
In this course, students learn about the physical, optical, and mechanical properties of post-harvest agricultural products and various biological resources. Through hands-on labs using programming tools such as digital image processing (OpenCV), students quantitatively analyze these properties.

Each week, students download (clone) newly provided lab materials organized in **weekly folders (e.g., `week2`, `week3`...)** to their local PCs. After completing the lab exercises in their IDE, students commit and push their results (`git add/commit/push`) to build a cumulative learning portfolio throughout the semester.

---

## 📂 Weekly Lab Summary

### [Week 01] Orientation & Setting Up the Development Environment
- Python and GitHub account setup, local development environment (VS Code, etc.) configuration, and repository creation

### [Week 02] Geometric Shape Index Analysis: Circularity & Sphericity Algorithm Implementation
Learn the fundamentals of digital image processing and compute key physical characteristics of apple specimens — **Circularity and Sphericity** — from captured images.
- **[Group A] Normal Apple Data ([`apple_side_A.png`](week2/apple_side_A.png), [`apple_top_A.png`](week2/apple_top_A.png))**: Round, nearly symmetrical normal specimens
- **[Group B] 10% Distorted Apple Data ([`apple_side_B.png`](week2/apple_side_B.png), [`apple_top_B.png`](week2/apple_top_B.png))**: Asymmetric specimens with one axis distorted
- **Key Learning Scripts**:
  - [`step1_preprocess.py`](week2/step1_preprocess.py): Image loading, grayscale conversion, blur-based noise removal
  - [`step2_contour.py`](week2/step2_contour.py): Otsu's binarization and object contour extraction
  - [`step3_shape_analysis.py`](week2/step3_shape_analysis.py): Geometric feature extraction (perimeter, area) and formula-based shape index (Circularity) computation with visualization
- ➡️ **[View Detailed Lab Tutorial for This Week](week2/week02_lab_circularity_sphericity.md)**

### [Week 03] Volume & Surface Area Estimation via Numerical Integration
Automatically extract the avocado profile from a reference image using OpenCV, apply cubic spline interpolation, then estimate the volume of revolution (`V = π∫r²dx`) via Simpson's and Trapezoidal numerical integration.
- **Sample Specimen**: Hass avocado front-view reference image ([`avocado_front_view.png`](week3/images/avocado_front_view.png))
- **Key Learning Scripts**:
  - [`avocado_profile.py`](week3/avocado_profile.py): (**New**) Image loading → OpenCV contour detection → automatic profile data extraction
  - [`step1_interpolation.py`](week3/step1_interpolation.py): Image-based profile extraction + cubic spline interpolation, 3-panel visualization
  - [`step2_volume.py`](week3/step2_volume.py): Volume estimation via numerical integration (Simpson vs. Trapezoidal), convergence analysis
  - [`step3_3d_visualization.py`](week3/step3_3d_visualization.py): Input image → 3D reconstruction → 2D profile, 3-panel visualization
- ➡️ **[View Detailed Lab Tutorial for This Week](week3/week03_lab_volume_surface_area.md)**

### [Week 04] Density, Porosity & Virtual 3D Packing
Understand the concepts of **True Density, Bulk Density, and Porosity**—key physical properties of biomaterials. Quantitatively evaluate these properties through Python-based data augmentation and 3D space simulation.
- **Sample Specimens**: Avocado (Hass) and Apple (using virtual geometry and weight data)
- **Key Learning Scripts**:
  - [`step1_density_porosity.py`](week4/step1_density_porosity.py): Cross-validate density/porosity calculation formulas (volume subtraction vs. density ratio methods) and implement 3D virtual packing (visualizing products and voids).
  - [`step2_advanced_apple.py`](week4/step2_advanced_apple.py): An advanced assignment where students use the provided base structure and input apple specimen data (geometric dimensions and weight) to complete advanced calculations and the 3D virtual packing code themselves.
- ➡️ **[View Detailed Lab Tutorial for This Week](week4/Week04_Lab_Density_Porosity.md)**

### [Week 05] (To be updated in upcoming weeks)
- (Next week update...)

---

## 👩‍🏫 Common Lab Preparation Guide (Environment Setup & Code Execution)
This lab assumes a local PC environment with Python and external libraries (OpenCV, NumPy) installed. Please follow the steps below before starting.

### 1. Download Base Code & Data (Clone)
Each week, students must pull the base code and image data distributed by the instructor to their local PC.
- **[Method 1] Git Command (Recommended)**: Clone the entire repository via terminal.
   ```bash
   git clone [provided_lab_repository_url.git]
   ```
- **[Method 2] AI IDE Prompt**: If using an AI-based IDE like Cursor or Antigravity, you can type directly in the chat window.
  - *e.g., "Clone this GitHub repository ([repository_url]) into a folder called biomaterial-handling on my C drive and open it."*
- **[Method 3] Download**: Click the `Code` button on the GitHub web page > `Download ZIP`, then extract to your desired folder.

### 2. Launch IDE & Load Project Folder
1. Open your preferred editor (VS Code, Cursor, Antigravity, etc.).
2. Always use **`File` > `Open Folder...`** from the top menu to open **the entire top-level directory (`biomaterial-handling/`)**.
   *(Opening only a sub-week folder may cause relative path errors when running Python scripts in the terminal.)*

### 3. Install Required Python Packages & Update Portfolio
1. Open the built-in terminal in your IDE (e.g., `` Ctrl + ` `` in VS Code).
2. Install the required OpenCV and NumPy packages:
   ```bash
   pip install opencv-python numpy
   ```
3. Run each weekly script (e.g., `python step1_preprocess.py`) in the terminal to verify execution.
4. **Update Your Results**: After completing the lab, be sure to modify this `README.md` file (`git add/commit`) and `push` to your own GitHub repository to maintain your assignment portfolio.
5. If you need coding help or encounter difficulties, feel free to ask AI tools (ChatGPT, Antigravity, etc.) for guidance.

---

## 4. Version Control & GitHub Submission Guide (Folder-Based Management)

Students do not need to create a new repository each week. Instead, **manage weekly assignments by creating weekly folders (week02, week03...) within a single master repository (e.g., `biomaterial-handling`)**.

### 4-1. Initialize Project Git Repository (One-Time Setup)
Open a terminal (command prompt) in your top-level project folder (e.g., `C:\biomaterial-handling`).
1. `git init`: Initialize the current folder as a local Git repository.
2. (On GitHub website) Create a new Repository named `biomaterial-handling`.
3. `git remote add origin https://github.com/[your-username]/biomaterial-handling.git`: Link the remote repository.

> 💡 **[AI Prompt Alternative] Using Cursor / Antigravity**
> If terminal commands are difficult, you can **ask AI directly** while the folder is open in your IDE:
> - *"Initialize this folder as a local Git repository and connect it to my GitHub remote at `[your-username]/biomaterial-handling`."*

### 4-2. Create Weekly Assignment Folders & Save Source Code
Each week when a new lab is assigned, create the corresponding week folder inside the top-level directory and save your code there.
1. Create this week's assignment folder: `week02` (next week: `week03`)
2. Save all Python scripts (`step1`, `step2`, `step3`), original images (`apple_side_A.png`), and result screenshots inside the `week02` folder.

### 4-3. Push Assignments to GitHub Remote (Weekly)
Once your folder is organized, run the following commands from the top-level directory terminal:
1. `git add .`: Stage all new/modified weekly folders (e.g., week02)
2. `git commit -m "Add week02 shape analysis python scripts"`: Save a weekly snapshot
3. `git push -u origin main`: (Use `-u origin main` only the first time; afterwards just `git push`)
   - **Note**: Use a **Personal Access Token (PAT)** instead of a password.

> 💡 **[AI Prompt Alternative] Quick Weekly Commit & Push**
> - *"Stage all files in the new `week02` folder, commit with the message 'Add week02 shape analysis python scripts', and push to origin main."*

### 4-4. Update Main README.md (For Collaboration/Evaluation)
Update the `README.md` file in the top-level folder each week to build your portfolio:
- **Project Overview**: State your name / student ID / indicate this is the Biomaterial Handling assignment repository
- **Weekly Update Log**: 
  - `[Week 02]` Completed apple contour recognition and circularity/sphericity calculation scripts
  - `[Week 03]` Performed avocado volume/surface area estimation via numerical integration
  - `[Week 04]` Calculated density/porosity and implemented 3D virtual packing
  - `[Week 05]` (To be updated next week)

---
*After completing your assignment, submit your GitHub repository URL (e.g., `https://github.com/your-username/biomaterial-handling/tree/main/en/week02`) to your TA/professor for final grading.*
