# 🚗 Autonomous Insurance Claims Processing Agent

This project is a simple Python- and Streamlit-based tool that reads FNOL (First Notice of Loss) documents and automatically extracts the important claim information from them. It works for both **simple FNOL text formats** and **ACORD Automobile Loss Notice PDFs**, which are commonly used in the insurance industry.

Once the fields are extracted, the system checks for missing mandatory information and applies business rules to recommend the correct routing for the claim (Fast-track, Manual Review, Investigation, etc.).

You can test the deployed app here:  
👉 **https://autonomous-insurance-claims-processing-agent.streamlit.app/**


## 🌟 What the App Can Do

- Upload **TXT** or **PDF (ACORD or custom FNOL)** files  
- Extracts fields like:
  - Policy Number  
  - Policyholder Name  
  - Incident Date & Time  
  - Location  
  - Description of Accident  
  - Vehicle VIN / Make / Model / Year  
  - Estimated Damage  
- Detects missing mandatory fields  
- Applies business routing rules:
  - Damage < 25,000 → Fast-track  
  - Suspicious description (fraud/staged/inconsistent) → Investigation  
  - Injury claims → Specialist Queue  
  - Anything incomplete → Manual Review  
- Displays all extracted data in the Streamlit UI  
- Lets you download the result as a JSON file  

---

## 🏗️ Project Structure

Autonomous-Insurance-Claims-Processing-Agent/
│
├── streamlitapp.py 
├── main.py 
├── documentReader.py 
├── extractor.py 
├── rules.py # Routing logic
├── json_writer.py # Writes outputs to JSON
│
├── sampledocs/ # Sample FNOL/ACORD test files
├── outputs/ # JSON results generated locally
└── requirements.txt # Dependencies



## 💡 How the System Works

### **1. Reading the Document**  
- TXT files are read directly  
- PDFs are read using `pdfplumber`  
- OCR fallback using `pytesseract` (local only)  

### **2. Extracting the Fields**  
The extractor looks for patterns from:
- Simple FNOL forms  
- ACORD Automobile Loss Notice fields (POLICY NUMBER, DATE OF LOSS, V.I.N., etc.)

If a value is missing, it remains `None` and is flagged later.

### **3. Checking Mandatory Fields**  
If required fields are missing → the claim goes to **Manual Review**.

### **4. Routing Logic**  
Based on simple business rules:
- < 25,000 damage → **Fast-track**  
- Suspicious keywords → **Investigation Flag**  
- Injury → **Specialist Queue**  
- Missing fields → **Manual Review**  

### **5. JSON Output**  
The final output includes:
- Extracted fields  
- Missing fields  
- Recommended route  
- Explanation  
- Download option  

---

## ▶️ How to Run Locally

### **1. Clone the repository**
git clone https://github.com/ChanduBollu30/Autonomous-Insurance-Claims-Processing-Agent.git
cd Autonomous-Insurance-Claims-Processing-Agent



### **2. Create a virtual environment**
Windows:
python -m venv venv
venv\Scripts\activate


Mac/Linux:
python3 -m venv venv
source venv/bin/activate


### **3. Install dependencies**
pip install -r requirements.txt


### **4. Run the Streamlit app**
streamlit run streamlitapp.py


### **5. Process sample FNOL files (optional)**
python main.py


## 🌐 Online Deployment

The project is deployed for easy testing using Streamlit Cloud:

👉 **https://autonomous-insurance-claims-processing-agent.streamlit.app/**

You can upload:
- Simple FNOL text files  
- Text-based ACORD PDFs  
- The provided filled ACORD sample  
and see the live extraction and routing.

---

## 🧪 Sample JSON Output

{
"extractedFields": {
"policyNumber": "APD-458921",
"policyholderName": "Suresh Kumar",
"incidentDate": "2025-02-12",
"location": "Near Indiranagar Metro Station, Bengaluru",
"description": "While changing lanes...",
"assetID": "KA03MN4567ZX98234",
"assetType": "MARUTI",
"model": "SWIFT",
"year": "2021",
"estimatedDamage": "22,500 INR",
"initialEstimateNumeric": 22500
},
"missingFields": [],
"recommendedRoute": "Fast-track",
"reasoning": "Estimated damage 22500 is < 25000"
}


## 🚀 Future Improvements

- LLM-based information extraction (Gemini / GPT)  
- Better accuracy for unstructured PDFs  
- Fraud scoring  
- Multi-file batch upload  
- Full backend API version (FastAPI)


## ✨ Final Notes

I built this project as a clean and simple solution for automated FNOL data extraction.  
It supports both **custom FNOL** and **ACORD forms**, and the Streamlit UI makes it easy to test and demonstrate.

Thank you for reviewing the project!
