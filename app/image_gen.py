import asyncio

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
