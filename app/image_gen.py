import asyncio
import httpx
import urllib.parse
import logging

logger = logging.getLogger(__name__)

async def mock_generate_image(prompt: str) -> str:
    """
    Mock image generation function.
    In a real scenario, this would call an API like Stable Diffusion, DALL-E, etc.
    For now, it returns a placeholder image URL.
    """
    # Simulate a delay for image generation
    await asyncio.sleep(2)
    
    # Return a random placeholder image
    return "https://picsum.photos/seed/prompt2shot/800/600"

async def generate_image(prompt: str) -> str:
    """
    Generate an image using Pollinations.ai's free API.
    Falls back to mock_generate_image if the request fails.
    """
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=600&nologo=true"
    
    try:
        # Use httpx to verify the URL resolves to a valid image
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url)
            
            if response.status_code == 200 and response.headers.get("content-type", "").startswith("image/"):
                logger.info(f"Successfully generated image via Pollinations.ai")
                return url
            else:
                logger.warning(f"Pollinations API returned status {response.status_code} or invalid content type. Falling back to mock.")
                return await mock_generate_image(prompt)
    except Exception as e:
        logger.warning(f"Error calling Pollinations API: {str(e)}. Falling back to mock.")
        return await mock_generate_image(prompt)
