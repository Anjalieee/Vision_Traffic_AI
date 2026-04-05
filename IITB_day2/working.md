🔧 Setup Instructions (IMPORTANT)
## 🔧 Environment Setup

1. Clone the repository:
   git clone https://github.com/Anjalieee/Vision_Traffic_AI.git
   cd Vision_Traffic_AI

2. Create a virtual environment:
   python -m venv venv

3. Activate it:
   Windows:
   venv\Scripts\activate

   macOS/Linux:
   source venv/bin/activate

4. Install dependencies:
   pip install -r requirements.txt
🌐 ChromeDriver / Selenium Note
## 🌐 Browser Setup

This project uses Selenium for web scraping.

- Ensure Google Chrome is installed
- Selenium 4 automatically manages ChromeDriver
- No manual driver installation required

If issues occur:
pip install webdriver-manager
▶️ Run the project
## ▶️ Run

python main.py
Output images are not stored in the repository
- They will be generated in the `images/` folder when the script runs