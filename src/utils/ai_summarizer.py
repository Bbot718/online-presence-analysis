from llama_cpp import Llama

class AISummarizer:
    def __init__(self):
        # Initialize Llama 2 model
        self.llm = Llama(
            model_path="./models/llama-2-7b-chat.gguf",  # Download from HuggingFace
            n_ctx=2048,  # Context window
            n_threads=4  # Adjust based on your CPU
        )

    def generate_summary(self, data: dict, section_name: str) -> str:
        """Generate summary using local Llama 2 model"""
        try:
            prompt = f"""Analyze the following {section_name} data and provide a 
            concise, professional summary highlighting key insights:
            {str(data)}
            
            Format the response in clear, bullet-point insights."""
            
            response = self.llm(
                prompt,
                max_tokens=500,
                temperature=0.7,
                stop=["###"]
            )
            
            return response['choices'][0]['text'].strip()
        except Exception as e:
            return f"Unable to generate summary: {str(e)}" 