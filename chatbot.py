"""
DevOps Troubleshooting Chatbot
Main chatbot class for loading model and generating responses
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
import warnings
warnings.filterwarnings('ignore')


class DevOpsChatbot:
    """
    DevOps troubleshooting chatbot using fine-tuned Mistral-7B with LoRA
    """
    
    def __init__(
        self,
        base_model="mistralai/Mistral-7B-Instruct-v0.2",
        lora_model="Lebowski17/devops-lora-mistral",
        load_in_4bit=True,
        device_map="auto"
    ):
        """
        Initialize the chatbot with model loading
        
        Args:
            base_model: Base model identifier
            lora_model: LoRA adapter model identifier
            load_in_4bit: Whether to use 4-bit quantization
            device_map: Device mapping strategy
        """
        self.base_model_name = base_model
        self.lora_model_name = lora_model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"🔧 Loading DevOps Chatbot...")
        print(f"📱 Device: {self.device}")
        
        # Configure quantization if requested
        if load_in_4bit:
            self.bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type="nf4"
            )
        else:
            self.bnb_config = None
        
        # Load tokenizer
        print("📚 Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(base_model)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Load base model
        print("🤖 Loading base model...")
        base_model_kwargs = {
            "device_map": device_map,
            "torch_dtype": torch.float16
        }
        if self.bnb_config:
            base_model_kwargs["quantization_config"] = self.bnb_config
            
        self.base_model = AutoModelForCausalLM.from_pretrained(
            base_model,
            **base_model_kwargs
        )
        
        # Load LoRA adapter
        print("🔌 Loading LoRA adapter...")
        self.model = PeftModel.from_pretrained(self.base_model, lora_model)
        
        print("✅ Model loaded successfully!\n")
        
    def generate_response(
        self,
        question,
        max_tokens=300,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        repetition_penalty=1.1
    ):
        """
        Generate response to a DevOps question
        
        Args:
            question: User's question/problem
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            do_sample: Whether to use sampling
            repetition_penalty: Penalty for repetition
            
        Returns:
            Generated response text
        """
        # Format prompt in instruction format
        prompt = f"<s>[INST] {question} [/INST]"
        
        # Tokenize input
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(self.model.device)
        
        # Generate response
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=do_sample,
                repetition_penalty=repetition_penalty,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode and clean response
        full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the assistant's response (remove the instruction part)
        if "[/INST]" in full_response:
            response = full_response.split("[/INST]")[-1].strip()
        else:
            response = full_response
            
        return response
    
    def chat(self):
        """
        Interactive CLI chat interface
        """
        print("=" * 60)
        print("🤖 DevOps Troubleshooting Chatbot")
        print("=" * 60)
        print("\nI can help you with:")
        print("  🐳 Docker issues")
        print("  📦 Git problems")
        print("  🖥️  Linux/system administration")
        print("  ☁️  CI/CD and cloud deployments")
        print("  🔧 Backend and database issues")
        print("\nType 'exit' or 'quit' to end the conversation.\n")
        print("=" * 60 + "\n")
        
        while True:
            try:
                # Get user input
                question = input("You: ").strip()
                
                # Check for exit commands
                if question.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Thanks for using DevOps Chatbot. Goodbye!")
                    break
                
                # Skip empty inputs
                if not question:
                    continue
                
                # Generate and display response
                print("\n🤖 Bot: ", end="", flush=True)
                response = self.generate_response(question)
                print(response)
                print("\n" + "-" * 60 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Chat interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")


def main():
    """
    Main function to run the chatbot
    """
    # Initialize chatbot
    chatbot = DevOpsChatbot()
    
    # Start interactive chat
    chatbot.chat()


if __name__ == "__main__":
    main()
