from ddgs import DDGS


def google_search(query:str) -> dict[str, list[str]]:
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=5)
        search_results = [f"{result['title']}\n{result['body']}\n\n" for result in results]
    return {"status": "success", "report": search_results}
