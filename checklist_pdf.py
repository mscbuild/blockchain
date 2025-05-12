from fpdf import FPDF
 
# Define checklist content
checklist_sections = {
    "Basic Blockchain Core": [
        "Define `Block` class with hashing",
        "Define `Blockchain` class",
        "Implement Proof-of-Work",
        "Create Genesis Block",
        "Chain validation method",
        "CLI or script to add and mine blocks",
    ],
    "Transactions & Wallets": [
        "Define `Transaction` class",
        "Generate ECDSA public/private keys",
        "Implement digital signatures",
        "Validate signed transactions",
        "Add mining reward transaction",
        "Maintain list of pending transactions",
    ],
    "Flask Node API": [
        "Set up Flask API server",
        "/mine endpoint",
        "/transactions/new endpoint",
        "/chain endpoint",
    ],
    "Network & Consensus": [
        "Node registration (/nodes/register)",
        "Conflict resolution (/nodes/resolve)",
        "Sync and replace chain from peers",
        "Broadcast transactions (optional)",
    ],
    "Testing & Multi-Node Setup": [
        "Run multiple nodes on different ports",
        "Test transaction creation via Postman",
        "Test mining and reward handling",
        "Validate consensus by running longer chains",
    ],
    "Nice-to-Have Features (Advanced)": [
        "Balance tracking per wallet",
        "Simple wallet CLI or frontend",
        "Blockchain explorer UI",
        "Persistent storage (SQLite or file)",
        "Peer-to-peer communication with WebSockets",
    ]
}

# Generate PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Blockchain Development Progress Checklist", ln=True, align="C")
pdf.set_font("Arial", size=12)

for section, tasks in checklist_sections.items():
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, section, ln=True)
    pdf.set_font("Arial", size=12)
    for task in tasks:
        pdf.cell(10)
        pdf.cell(0, 10, f"[ ] {task}", ln=True)

pdf.output("blockchain_checklist.pdf")
