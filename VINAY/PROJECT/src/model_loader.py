import requests

def load_model():
    """
    In the new Ollama setup, we don't 'load' the model into Python memory.
    Instead, we check if the Ollama service is running.
    """
    try:
        # Check if the Ollama API is responding
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        
        if response.status_code == 200:
            print("✅ Ollama Service detected!")
            # Check if phi3 is actually downloaded
            models = [m['name'] for m in response.json().get('models', [])]
            if any("phi3" in m for m in models):
                print("✅ Phi-3 model is ready to use.")
                return "Ollama", "phi3"
            else:
                print("⚠️ Ollama is running, but Phi-3 is missing. Run 'ollama run phi3' in terminal.")
                return None, None
        return None, None
    except Exception as e:
        print(f"❌ Connection Error: Ensure Ollama is running in the taskbar. ({e})")
        return None, None

if __name__ == "__main__":
    # Test the connection
    load_model()