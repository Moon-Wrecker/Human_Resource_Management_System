# Step 1: Create FAISS database first
python policy_rag.py
# This creates the faiss_index/ folder
# Type 'quit' after it's set up

# Step 2: Start API (it will load existing database)
python api.py
# API loads from faiss_index/ automatically

# Step 3: Use frontend
# Open frontend.html
