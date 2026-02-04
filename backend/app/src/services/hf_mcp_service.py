"""
Hugging Face Model Context Protocol (MCP) Service for integrating with Hugging Face models
"""
import os
import asyncio
from typing import Dict, List, Optional, Any
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import InferenceClient
import torch
from ..config import settings


class HFMCPService:
    """
    Service class to handle communication with Hugging Face models
    """

    def __init__(self):
        self.hf_token = os.getenv("HF_TOKEN") or settings.hf_token if hasattr(settings, 'hf_token') else None
        self.model_name = os.getenv("HF_MODEL_NAME") or settings.hf_model_name
        self.max_tokens = int(os.getenv("HF_MAX_TOKENS", settings.hf_max_tokens))
        self.temperature = float(os.getenv("HF_TEMPERATURE", settings.hf_temperature))
        self.client = None
        self.pipeline = None
        self.tokenizer = None
        self.model = None

        if self.hf_token:
            self.client = InferenceClient(token=self.hf_token)

        # Initialize local model if available
        try:
            self._initialize_local_model()
        except Exception as e:
            print(f"Warning: Could not initialize local model: {e}. Will use inference API if token provided.")
    
    def _initialize_local_model(self):
        """
        Initialize a local model for inference
        """
        if torch.cuda.is_available():
            device = 0  # Use GPU
        else:
            device = -1  # Use CPU
            
        try:
            # Try initializing a text generation pipeline
            self.pipeline = pipeline(
                "text-generation",
                model=self.model_name,
                tokenizer=self.model_name,
                device=device
            )
            
            # Also initialize tokenizer and model separately for more control
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            # Add padding token if it doesn't exist
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
        except Exception as e:
            print(f"Could not initialize local model {self.model_name}: {e}")
            # Try with a simpler model
            try:
                self.model_name = "gpt2"
                self.pipeline = pipeline(
                    "text-generation",
                    model=self.model_name,
                    tokenizer=self.model_name,
                    device=device
                )
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
                
                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token
                    
            except Exception as e2:
                print(f"Could not initialize fallback model: {e2}")
    
    async def generate_text(self, prompt: str, max_tokens: int = None, temperature: float = None) -> str:
        """
        Generate text using either local model or Hugging Face Inference API
        """
        # Use default values from config if not provided
        if max_tokens is None:
            max_tokens = self.max_tokens
        if temperature is None:
            temperature = self.temperature

        # Prepare the input for chat-based models
        input_text = f"User: {prompt}\nAssistant:"

        # First, try using local model if available
        if self.pipeline is not None:
            try:
                # Format for conversational models
                sequences = self.pipeline(
                    input_text,
                    max_length=len(self.tokenizer.encode(input_text)) + max_tokens,
                    num_return_sequences=1,
                    temperature=temperature,
                    pad_token_id=self.tokenizer.eos_token_id,
                    truncation=True
                )

                # Extract the generated part (after the input)
                generated_text = sequences[0]['generated_text'][len(input_text):]

                # Clean up the response
                # Stop at the first occurrence of "User:" to prevent model continuing the conversation
                if "User:" in generated_text:
                    generated_text = generated_text.split("User:")[0]

                return generated_text.strip()
            except Exception as e:
                print(f"Local model generation failed: {e}")

        # If local model fails or isn't available, try using the HF Inference API
        if self.client is not None:
            try:
                response = self.client.text_generation(
                    prompt=input_text,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    return_full_text=False  # Only return the generated part
                )
                return response.strip()
            except Exception as e:
                print(f"HF Inference API failed: {e}")

        # If everything fails, return a default response
        return "I'm sorry, I couldn't generate a response at the moment. Please try again later."
    
    async def chat_completion(self, messages: List[Dict[str, str]], max_tokens: int = None, temperature: float = None) -> str:
        """
        Generate a chat completion using the conversation history
        """
        # Use default values from config if not provided
        if max_tokens is None:
            max_tokens = self.max_tokens
        if temperature is None:
            temperature = self.temperature

        # Convert messages to a single prompt
        conversation = ""
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role.lower() == "user":
                conversation += f"User: {content}\n"
            elif role.lower() == "assistant":
                conversation += f"Assistant: {content}\n"
            else:
                conversation += f"{role.capitalize()}: {content}\n"

        # Add the prompt for the assistant to respond
        conversation += "Assistant:"

        # First, try using local model if available
        if self.pipeline is not None:
            try:
                sequences = self.pipeline(
                    conversation,
                    max_length=len(self.tokenizer.encode(conversation)) + max_tokens,
                    num_return_sequences=1,
                    temperature=temperature,
                    pad_token_id=self.tokenizer.eos_token_id,
                    truncation=True
                )

                # Extract only the generated part
                generated_text = sequences[0]['generated_text'][len(conversation):]

                # Clean up the response
                if "User:" in generated_text:
                    generated_text = generated_text.split("User:")[0]

                return generated_text.strip()
            except Exception as e:
                print(f"Local model chat completion failed: {e}")

        # If local model fails, try using the HF Inference API
        if self.client is not None:
            try:
                # Format for chat models
                formatted_messages = []
                for msg in messages:
                    formatted_messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})

                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=formatted_messages,
                    max_tokens=max_tokens,
                    temperature=temperature
                )

                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"HF Inference API chat completion failed: {e}")

        # If everything fails, return a default response
        return "I'm sorry, I couldn't generate a response at the moment. Please try again later."
    
    def is_available(self) -> bool:
        """
        Check if the service is properly initialized and available
        """
        return self.pipeline is not None or self.client is not None


# Global instance
hf_mcp_service = HFMCPService()