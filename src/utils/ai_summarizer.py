from llama_cpp import Llama
import json
import os
from datetime import datetime

class AISummarizer:
    def __init__(self):
        # Initialize Llama 2 model
        self.llm = Llama(
            model_path="./models/llama-2-7b-chat.gguf",  
            n_ctx=2048,  # Context window
            n_threads=4  # Adjust based on your CPU
        )

        # Create reports directory if it doesn't exist
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)

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
            
            summary = response['choices'][0]['text'].strip()
            
            # Save the report to JSON
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_data = {
                "timestamp": timestamp,
                "section_name": section_name,
                "input_data": data,
                "summary": summary
            }
            
            filename = f"report_{timestamp}.json"
            filepath = os.path.join(self.reports_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=4)
            
            return summary
        except Exception as e:
            return f"Unable to generate summary: {str(e)}" 