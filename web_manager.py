from duckduckgo_search import DDGS

class WebManager:
    """Provides local, API-key-less web searching capabilities to Ultron."""
    
    def search(self, query, max_results=3):
        """Searches DuckDuckGo and returns a summary of the top results."""
        print(f"[*] WebManager: Searching the web for '{query}'...")
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
                
            if not results:
                return f"No web results found for '{query}'."
                
            summary = []
            for i, res in enumerate(results):
                summary.append(f"Result {i+1}: {res.get('title')}\n{res.get('body')}")
                
            return "\n\n".join(summary)
        except Exception as e:
            return f"Error performing web search: {e}"

if __name__ == "__main__":
    wm = WebManager()
    print(wm.search("What is the capital of France?"))
