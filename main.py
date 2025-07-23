from facade import PolicyNavigatorFacade
from rich.console import Console

def main():
    console = Console()
    facade = PolicyNavigatorFacade()  # Facade provides a unified interface to all agents/tools
    console.print("[bold green]Welcome to the Agentic RAG System![/bold green]")
    while True:
        # Show the selection menu for query type
        console.print("\n[bold yellow]Select query type:[/bold yellow]\n1. Commercial Code\n2. EPA\n3. Federal Register\n4. CourtListener\n5. Upload Document or Specify URL\n6. Query Uploaded Documents\n7. Exit")
        choice = console.input("[bold blue]Enter choice (1-7): [/bold blue]")
        if choice.strip() in ["7", "exit", "quit"]:
            break
        if choice == "5":
            path_or_url = console.input("[bold blue]Enter file path or public URL: [/bold blue]")
            try:
                result = facade.handle_upload(path_or_url)
                console.print(f"[green]Document/URL Ingestion response:[/green]\n{result}")
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
            continue
        if choice == "6":
            query = console.input("[bold blue]Enter your question about uploaded documents: [/bold blue]")
            try:
                # Directly use the UploadedDocHandler (no prefix needed)
                from handlers.uploaded_doc import UploadedDocHandler
                handler = UploadedDocHandler()
                result = handler.run(query)
                console.print(f"[green]Uploaded Document response:[/green]\n{result}")
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
            continue
        query = console.input("[bold blue]Enter your query: [/bold blue]")
        try:
            # Route the query to the correct agent/tool based on user selection
            if choice == "1":
                result = facade.handle_query("commercial code: " + query)
                console.print(f"[green]Commercial Code Agent response:[/green]\n{result}")
            elif choice == "2":
                result = facade.handle_query("epa: " + query)
                console.print(f"[green]EPA Agent response:[/green]\n{result}")
            elif choice == "3":
                result = facade.handle_query("federal register: " + query)
                console.print(f"[green]Federal Register Tool response:[/green]\n{result}")
            elif choice == "4":
                result = facade.handle_query("court: " + query)
                console.print(f"[green]CourtListener Tool response:[/green]\n{result}")
            else:
                console.print("[red]Invalid choice. Please select 1-7.[/red]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    main() 