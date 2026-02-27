"""
Gradio Web Interface for DevOps Chatbot
Deploy easily to Hugging Face Spaces or run locally
"""

import gradio as gr
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
import warnings
warnings.filterwarnings('ignore')


class ChatbotInterface:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.load_model()
    
    def load_model(self):
        """Load model and tokenizer"""
        print("Loading model...")
        
        base_model_name = "mistralai/Mistral-7B-Instruct-v0.2"
        lora_model_name = "Lebowski17/devops-lora-mistral"
        
        # Quantization config
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4"
        )
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(base_model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Load base model
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            quantization_config=bnb_config,
            device_map="auto",
            torch_dtype=torch.float16
        )
        
        # Load LoRA
        self.model = PeftModel.from_pretrained(base_model, lora_model_name)
        print("Model loaded successfully!")
    
    def generate_response(self, message, history, temperature, max_tokens):
        """Generate chatbot response"""
        # Format prompt
        prompt = f"<s>[INST] {message} [/INST]"
        
        # Tokenize
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(self.model.device)
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9,
                do_sample=True,
                repetition_penalty=1.1,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode
        full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract response
        if "[/INST]" in full_response:
            response = full_response.split("[/INST]")[-1].strip()
        else:
            response = full_response
            
        return response


def create_interface():
    """Create Gradio interface"""
    
    chatbot_interface = ChatbotInterface()
    
    # Custom CSS for better styling
    custom_css = """
    .gradio-container {
        font-family: 'Arial', sans-serif;
    }
    .header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    """
    
    # Example questions
    examples = [
        ["My Docker container exits immediately after starting. What should I check?"],
        ["How do I resolve a Git merge conflict?"],
        ["I'm getting 'permission denied' when running a bash script. How do I fix this?"],
        ["My CI/CD pipeline is failing. What are common causes?"],
        ["How can I debug a database connection timeout?"],
        ["What does Docker exit code 137 mean?"],
        ["How do I fix detached HEAD state in Git?"],
    ]
    
    with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:
        
        # Header
        gr.HTML("""
        <div class="header">
            <h1>🤖 DevOps Troubleshooting Chatbot</h1>
            <p>AI-powered assistant for infrastructure and deployment issues</p>
        </div>
        """)
        
        # Description
        gr.Markdown("""
        ### What I Can Help With:
        - 🐳 **Docker**: Container issues, networking, volumes
        - 📦 **Git**: Merge conflicts, workflow problems
        - 🖥️ **Linux**: Permission issues, shell scripts, cron jobs
        - ☁️ **CI/CD**: Pipeline failures, deployments
        - 🔧 **Backend**: API issues, database connections
        
        Ask me anything about DevOps troubleshooting!
        """)
        
        # Chat interface
        chatbot = gr.Chatbot(
            height=400,
            show_label=False,
            avatar_images=(None, "🤖")
        )
        
        with gr.Row():
            msg = gr.Textbox(
                placeholder="Describe your DevOps issue...",
                show_label=False,
                scale=4
            )
            send = gr.Button("Send", scale=1, variant="primary")
        
        # Advanced settings
        with gr.Accordion("⚙️ Advanced Settings", open=False):
            temperature = gr.Slider(
                minimum=0.1,
                maximum=1.0,
                value=0.7,
                step=0.1,
                label="Temperature (creativity)",
                info="Higher = more creative, Lower = more focused"
            )
            max_tokens = gr.Slider(
                minimum=50,
                maximum=500,
                value=300,
                step=50,
                label="Max tokens",
                info="Maximum length of response"
            )
        
        # Examples
        gr.Examples(
            examples=examples,
            inputs=msg,
            label="Try these examples:"
        )
        
        # Clear button
        clear = gr.Button("🗑️ Clear Chat")
        
        # Info footer
        gr.Markdown("""
        ---
        **Model:** Mistral-7B-Instruct-v0.2 + LoRA fine-tuning | 
        [GitHub](https://github.com/YOUR_USERNAME/devops-chatbot) | 
        [Model Card](https://huggingface.co/Lebowski17/devops-lora-mistral)
        """)
        
        # Chat logic
        def respond(message, chat_history, temp, max_tok):
            if not message.strip():
                return "", chat_history
            
            bot_message = chatbot_interface.generate_response(
                message, 
                chat_history,
                temp,
                max_tok
            )
            chat_history.append((message, bot_message))
            return "", chat_history
        
        # Event handlers
        msg.submit(respond, [msg, chatbot, temperature, max_tokens], [msg, chatbot])
        send.click(respond, [msg, chatbot, temperature, max_tokens], [msg, chatbot])
        clear.click(lambda: None, None, chatbot, queue=False)
    
    return demo


if __name__ == "__main__":
    demo = create_interface()
    demo.queue()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
