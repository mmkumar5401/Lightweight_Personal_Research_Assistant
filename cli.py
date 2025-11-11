import requests
from rich.console import Console

API_URL = "http://127.0.0.1:8000/ask"
console = Console()

def ask_backend(question: str):
    try:
        res = requests.post(API_URL, json={"question": question})
        if res.status_code != 200:
            console.print(f"[red]Error {res.status_code}:[/red] {res.text}")
            return
        answer = res.json().get("answer", "[No answer]")
        console.print("\n[bold green]🧠 Answer:[/bold green]\n")
        console.print(answer)
        console.print("\n" + "-" * 60 + "\n")
    except Exception as e:
        console.print(f"[red]⚠️ Request failed:[/red] {e}")

def main():
    console.print("[bold cyan]🎓 Thesis Research Copilot (CLI Mode)[/bold cyan]")
    console.print("Type 'exit' to quit.\n")
    while True:
        try:
            question = input("❓ Ask: ").strip()
            if question.lower() in {"exit", "quit"}:
                console.print("[bold yellow]👋 Goodbye.[/bold yellow]")
                break
            if question:
                ask_backend(question)
        except KeyboardInterrupt:
            console.print("\n[bold yellow]👋 Goodbye.[/bold yellow]")
            break

if __name__ == "__main__":
    main()
