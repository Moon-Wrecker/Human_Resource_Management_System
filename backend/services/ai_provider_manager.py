"""
AI Provider Manager with Gemini Integration and Fallback
Handles multiple API keys with automatic fallback for reliability
"""
import os
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
import google.generativeai as genai
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


class AIProviderManager:
    """
    Manages Google Gemini API calls with multiple keys and automatic fallback.
    Ensures high availability by trying backup keys if primary fails.
    """
    
    def __init__(self):
        """Initialize provider with multiple API keys from environment"""
        self.providers = [
            {
                "name": "gemini-primary",
                "key": os.getenv("GOOGLE_API_KEY"),
                "model": "gemini-2.0-flash-exp"
            },
            {
                "name": "gemini-backup",
                "key": os.getenv("GOOGLE_API_KEY_1"),
                "model": "gemini-2.0-flash-exp"
            }
        ]
        
        # Validate at least one key is available
        if not any(p["key"] for p in self.providers):
            logger.error("No Google API keys configured!")
            raise ValueError("At least one GOOGLE_API_KEY must be configured")
        
        logger.info(f"AI Provider Manager initialized with {len([p for p in self.providers if p['key']])} available keys")
    
    async def generate_report(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """
        Generate AI report with automatic fallback between API keys.
        
        Args:
            prompt: The prompt to send to AI
            temperature: Creativity level (0.0-1.0)
            max_tokens: Maximum response length
            
        Returns:
            Generated report as markdown string
            
        Raises:
            HTTPException: If all providers fail
        """
        last_error = None
        
        for i, provider in enumerate(self.providers):
            if not provider["key"]:
                logger.debug(f"Skipping provider {i+1}: No API key configured")
                continue
            
            try:
                logger.info(f"Attempting to generate report with provider {i+1}: {provider['name']}")
                
                # Configure Gemini with current key
                genai.configure(api_key=provider["key"])
                
                # Initialize model
                model = genai.GenerativeModel(
                    model_name=provider["model"],
                    generation_config={
                        "temperature": temperature,
                        "max_output_tokens": max_tokens,
                        "top_p": 0.95,
                        "top_k": 40
                    }
                )
                
                # Generate content
                response = model.generate_content(prompt)
                
                # Extract text from response
                if hasattr(response, 'text'):
                    report = response.text
                    logger.info(f"Successfully generated report with provider {i+1} ({len(report)} chars)")
                    return report
                else:
                    raise Exception("No text in response")
                
            except Exception as e:
                last_error = e
                logger.warning(f"Provider {i+1} ({provider['name']}) failed: {str(e)}")
                
                # If this is the last provider, raise error
                if i == len(self.providers) - 1:
                    logger.error(f"All providers failed. Last error: {str(last_error)}")
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail=f"AI report generation service temporarily unavailable. All providers failed. Last error: {str(last_error)}"
                    )
                
                # Continue to next provider
                continue
        
        # Should not reach here, but just in case
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No AI providers available"
        )
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check health status of all configured providers.
        
        Returns:
            Dictionary with provider status information
        """
        status_info = {
            "total_providers": len(self.providers),
            "available_providers": 0,
            "providers": []
        }
        
        for i, provider in enumerate(self.providers):
            provider_info = {
                "name": provider["name"],
                "index": i + 1,
                "model": provider["model"],
                "configured": bool(provider["key"]),
                "status": "available" if provider["key"] else "no_api_key"
            }
            
            if provider["key"]:
                status_info["available_providers"] += 1
            
            status_info["providers"].append(provider_info)
        
        return status_info

