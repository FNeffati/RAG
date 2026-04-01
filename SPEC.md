# RAG Project Specification Doc  
  
  
  
Problem:  
QA and Compliance staff need to quickly find accurate answers from long SOPs/Regulatory Documents without Manually Searching PDFs.  
  
Users:  
This is for internal Pharma/Compliance employee asking questions about SOPs / policies.   
  
Core Functionality:  
- User Asks a question   
- System Retrieves relevant Document chunks   
- LLM generates an answer based ONLY on those chunks  
- Answer includes citations (doc name and snippet)   
- System abstains when the answer is not supported by retrieved context  
  
Non Goals:   
- Fine tuning  
- Feedback loops / Reinforcement Learning from Human Feedback  
- Auth  
- Workflow automation   
- Editing  
- Multi-agent systems  
- Complex infrastructure  
- Deployment hardening  
  
Architecture:   
Documents → chunking → embeddings → vector store → retrieval → LLM → answer + citations  
Using:  
- Python   
- Streamlit (for speed)  
- Local Embeddings Model  
- API Model. API LLM for faster iteration in v1 (Switch to local model on production grade data)  
  
Dataset:  
8-10 Public documents from FDA/GMP. Refer to [X] folder.   
  
Success Criteria:  
- Retrieval returns relevant chunks for ≥80% of test questions  
- Answers include correct source document  
- System abstains on at least 3 known “unanswerable” questions  
- Works on ~15–20 predefined queries  
- Demo runs end-to-end  
  
Deliverable:   
- Working App  
- Clean Readme  
- Example Queries  
- Architecture Diagram  
- System behavior validated on a small evaluation set. See [ Path to Eval ]   
