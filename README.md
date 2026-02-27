---
title: DevOps Troubleshooting Chatbot
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: "4.0.0"
app_file: app.py
pinned: false
---
## 🎯 What It Does

This chatbot helps developers and DevOps engineers troubleshoot:

- **🐳 Docker Issues**: Container exits, networking, volume mounting
- **📦 Git Problems**: Merge conflicts, detached HEAD states, workflow errors
- **🖥️ Linux/System Admin**: Permission issues, shell scripting, cron jobs
- **☁️ CI/CD & Cloud**: Pipeline failures, deployment issues
- **🔧 Backend**: API bottlenecks, database connection problems

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
4GB+ RAM (for 4-bit quantized model)
CUDA-capable GPU (optional, but recommended)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Bharath5626/devops-chatbot.git
cd devops-chatbot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the chatbot**
```bash
python app/chatbot.py
```

## 🏗️ Architecture

```
Base Model: Mistral-7B-Instruct-v0.2
   ↓
LoRA Fine-tuning (r=16, alpha=32)
   ↓
490 DevOps-specific examples
   ↓
4-bit Quantization (NF4)
   ↓
DevOps Troubleshooting Chatbot
```

## 📊 Model Details

- **Base Model**: `mistralai/Mistral-7B-Instruct-v0.2`
- **Fine-tuning Method**: LoRA (Low-Rank Adaptation)
- **Training Dataset**: 490 instruction-response pairs
- **Model Size**: ~4GB (quantized)
- **Inference Speed**: ~2-3 tokens/sec (CPU), ~20-30 tokens/sec (GPU)

### Training Configuration
```python
LoRA Config:
  - Rank (r): 16
  - Alpha: 32
  - Target Modules: q_proj, v_proj
  - Dropout: 0.05

Training:
  - Epochs: 3
  - Batch Size: 2
  - Gradient Accumulation: 4
  - Learning Rate: 2e-4
```

## 💡 Usage Examples

### Example 1: Docker Container Issue
```
User: My Docker container exits immediately after starting

Bot: Check the Docker logs using `docker logs <container_id>` and ensure 
the main process doesn't exit. Common causes:
1. Missing CMD/ENTRYPOINT
2. Application crashes on startup
3. Incorrect working directory
...
```

### Example 2: Git Merge Conflict
```
User: How do I resolve a Git merge conflict?

Bot: To resolve merge conflicts:
1. `git status` to see conflicted files
2. Open files and look for <<<<<<< HEAD markers
3. Edit to keep desired changes
4. `git add <resolved-files>`
5. `git commit` to complete merge
...
```

## 🛠️ Project Structure

```
devops-chatbot/
├── app/
│   ├── chatbot.py          # Main chatbot application
│   ├── gradio_app.py       # Gradio web interface
│   └── streamlit_app.py    # Streamlit interface
├── notebooks/
│   └── training.ipynb      # Model training notebook
├── docs/
│   ├── training_guide.md   # How the model was trained
│   └── deployment.md       # Deployment instructions
├── tests/
│   └── test_chatbot.py     # Unit tests
├── requirements.txt
├── README.md
└── LICENSE
```

## 🔧 Configuration

Create a `config.yaml` file:

```yaml
model:
  base_model: "mistralai/Mistral-7B-Instruct-v0.2"
  lora_model: "Lebowski17/devops-lora-mistral"
  quantization: "4bit"
  
generation:
  max_tokens: 300
  temperature: 0.7
  top_p: 0.9
  
server:
  host: "0.0.0.0"
  port: 7860
```

## 🌐 Deployment Options

### Option 1: Hugging Face Spaces
1. Create a new Space on Hugging Face
2. Upload `app/gradio_app.py` as `app.py`
3. Add `requirements.txt`
4. Space will auto-deploy!

### Option 2: Google Colab
Open the notebook and run all cells. Share the public Gradio link.

### Option 3: Local Development
```bash
python app/gradio_app.py
# Access at http://localhost:7860
```

### Option 4: Docker
```bash
docker build -t devops-chatbot .
docker run -p 7860:7860 devops-chatbot
```

## 📈 Performance Metrics

| Metric | Value |
|--------|-------|
| Training Loss | 0.45 |
| Training Time | ~45 minutes (T4 GPU) |
| Model Size | 3.8 GB (quantized) |
| Inference (CPU) | 2-3 tokens/sec |
| Inference (GPU) | 20-30 tokens/sec |

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Future Improvements

- [ ] Add conversation memory across sessions
- [ ] Implement RAG for documentation search
- [ ] Support for uploading log files
- [ ] Multi-turn conversation context
- [ ] Add more specialized modules (Kubernetes, Terraform, etc.)
- [ ] Fine-tune on larger dataset (1000+ examples)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Mistral AI** for the base model
- **Hugging Face** for hosting and inference tools
- **PEFT/LoRA** for efficient fine-tuning
- The DevOps community for problem scenarios

## 📧 Contact

**Bharath** - [Bharathsiva453@gmail.com](mailto:Bharathsiva453@gmail.com)

Project Link: [https://github.com/Bharath5626/devops-chatbot](https://github.com/Bharath5626/devops-chatbot)

---

⭐ If you find this project helpful, please give it a star!
