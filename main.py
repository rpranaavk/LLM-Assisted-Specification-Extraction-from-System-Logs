import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("API Key not found. Please check your .env file.")

genai.configure(api_key=API_KEY)

# Use 'gemini-1.5-flash' for speed/cost or 'gemini-1.5-pro' for deep reasoning
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Define the Intended Policy (The "Law")
INTENDED_POLICY = """
POLICY DOCUMENT:
1. Administrators: Full access to all resources (READ, WRITE, DELETE).
2. Developers: READ/WRITE access to 'staging' resources only. No access to 'prod'.
3. Interns: READ-only access to 'staging' resources. Strictly NO access to 'prod' and NO DELETE permissions.
"""

def analyze_logs(log_file_path):
    # 3. Load the Data
    try:
        with open(log_file_path, 'r') as f:
            logs = json.load(f)
    except FileNotFoundError:
        print("Error: audit_logs.json not found.")
        return

    # 4. Construct the Prompt
    prompt = f"""
    You are an AI Security Auditor. Your job is to detect "Policy Drift" by comparing actual system logs against a written policy.
    
    INPUT DATA:
    
    --- INTENDED POLICY ---
    {INTENDED_POLICY}
    
    --- SYSTEM LOGS (ACTUAL BEHAVIOR) ---
    {json.dumps(logs, indent=2)}
    
    TASK:
    1. Analyze the logs to determine the *effective* permissions users are exercising.
    2. Compare these effective permissions against the Intended Policy.
    3. Flag any specific log entries that violate the policy.
    
    OUTPUT FORMAT (Markdown):
    ## Executive Summary
    [Brief overview of compliance status]
    
    ## Violation Details
    | User | Role | Action | Violation Type |
    |------|------|--------|----------------|
    | [User] | [Role] | [Action] | [Why is this a violation?] |
    
    ## Recommendations
    [Actionable steps to fix the issues]
    """

    # 5. Generate and Print Response
    print("🤖 AI Auditor is analyzing logs... please wait.\n")
    response = model.generate_content(prompt)
    print(response.text)

if __name__ == "__main__":
    analyze_logs("audit_logs.json")