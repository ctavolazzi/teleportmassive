import tkinter as tk
from tkinter import scrolledtext, messagebox
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("No OpenAI API key found in environment variables.")

# Create a client instance
client = OpenAI(api_key=api_key)

# Replace with your actual assistant ID
assistant_id = "asst_oz4KoaXh8AqQWLV8vst32arz"
my_assistant = client.beta.assistants.retrieve(assistant_id)
print(my_assistant)


def log_chat_history(user_input, assistant_response):
    with open("chat_history.log", "a") as log_file:
        log_file.write(f"You: {user_input}\nAssistant: {assistant_response}\n\n")

def send_message_to_assistant():
    user_input = user_input_text.get("1.0", tk.END).strip()
    if not user_input:
        messagebox.showinfo("Empty Message", "Please enter a message.")
        return
    try:
        # Create a thread for the conversation
        thread = client.beta.threads.create()

        # Add the user message to the thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )

        # Run the assistant on the thread
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=my_assistant.id
        )

        # Retrieve the run to get the assistant's response
        run_response = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

        # Assuming the last message in the thread is the assistant's response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        assistant_response = messages.data[-1]['content']['text']['value']

        # Display the response
        display_response(user_input, assistant_response)
        log_chat_history(user_input, assistant_response)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def display_response(user_input, assistant_response):
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "You: " + user_input + "\n")
    chat_history.insert(tk.END, "Assistant: " + assistant_response + "\n\n")
    chat_history.yview(tk.END)
    chat_history.config(state=tk.DISABLED)
    user_input_text.delete("1.0", tk.END)

# Tkinter GUI Setup
root = tk.Tk()
root.title("OpenAI Chat Assistant")

# Chat History Area
chat_history = scrolledtext.ScrolledText(root, state=tk.DISABLED, width=60, height=20)
chat_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# User Input Text Field
user_input_text = tk.Text(root, height=3, width=50)
user_input_text.grid(row=1, column=0, padx=10, pady=10)

# Send Button
send_button = tk.Button(root, text="Send", command=send_message_to_assistant)
send_button.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()
