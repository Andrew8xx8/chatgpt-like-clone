def read_prompt(name):
    with open(f"prompts/{name}.md", "r", encoding="utf-8") as file:
        return file.read()


GPTs = [
    {
        "id": "gpt-4",
        "name": "GPT-4",
        "image": "assets/gpt-4.png",
        "inital_messages": [{"role": "system", "content": read_prompt("gpt-4")}],
    },
    {
        "id": "python",
        "name": "Guido van Rossum (Python)",
        "image": "assets/python.png",
        "inital_messages": [{"role": "system", "content": read_prompt("python")}],
    },
    {
        "id": "ruby",
        "name": "Matz (Ruby)",
        "image": "assets/ruby.png",
        "inital_messages": [{"role": "system", "content": read_prompt("ruby")}],
    },
    {
        "id": "node",
        "name": "Ryan Dahl (NodeJS)",
        "image": "assets/node.png",
        "inital_messages": [{"role": "system", "content": read_prompt("node")}],
    },
    {
        "id": "react",
        "name": "Jordan Walke (React)",
        "image": "assets/react.png",
        "inital_messages": [{"role": "system", "content": read_prompt("react")}],
    },
]
