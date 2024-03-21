#!/usr/bin/env python
import os
import sys
import tkinter as tk
from tkinter import scrolledtext, ttk
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from download_models import download_models

global tokenizer, model

def load_models():
    splash_text.insert(tk.END, "Checking for SuperPrompt-v1 model files...\n")
    window.update()

    # check if we're running from a bundled package
    if getattr(sys, 'frozen', False):
        modelDir = os.path.join(sys._MEIPASS, "model_files")
    else:
        modelDir = os.path.expanduser("~") + "/.superprompter/model_files"

    if not all(os.path.exists(modelDir) for file in modelDir):
        splash_text.insert(tk.END, "Model files not found. Downloading...\n")
        window.update()
        download_models()
    else:
        splash_text.insert(tk.END, "Model files found. Skipping download.\n")
        window.update()

    splash_text.insert(tk.END, "Loading SuperPrompt-v1 model...\n")
    window.update()

    global tokenizer, model
    tokenizer = T5Tokenizer.from_pretrained(modelDir)
    model = T5ForConditionalGeneration.from_pretrained(modelDir, torch_dtype=torch.float16)

    splash_text.insert(tk.END, "SuperPrompt-v1 model loaded successfully.\n")
    window.update()

    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    splash_frame.grid_remove()

def answer():
    input_text = input_text_entry.get("1.0", tk.END).strip()
    max_new_tokens = int(max_new_tokens_entry.get())
    repetition_penalty = float(repetition_penalty_entry.get())
    temperature = float(temperature_entry.get())
    top_p = float(top_p_entry.get())
    top_k = int(top_k_entry.get())
    seed = int(seed_entry.get())

    torch.manual_seed(seed)

    if torch.cuda.is_available():
        device = 'cuda'
    else:
        device = 'cpu'

    input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(device)
    if torch.cuda.is_available():
        model.to('cuda')

    outputs = model.generate(input_ids, max_new_tokens=max_new_tokens, repetition_penalty=repetition_penalty,
                            do_sample=True, temperature=temperature, top_p=top_p, top_k=top_k)

    dirty_text = tokenizer.decode(outputs[0])
    text = dirty_text.replace("<pad>", "").replace("</s>", "").strip()
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, text)

    # Write input parameters and output to a log file
    log_enabled = log_var.get()
    if log_enabled:
        documents_dir = os.path.expanduser("~/")
        log_file = os.path.join(documents_dir, "superprompter_log.txt")
        os.makedirs(documents_dir, exist_ok=True)
        with open(log_file, "a") as file:
            file.write(f"{tk.datetime.datetime.now()}\n")
            file.write("Input Parameters:\n")
            file.write(f"Prompt: {input_text}\n")
            file.write(f"Max New Tokens: {max_new_tokens}\n")
            file.write(f"Repetition Penalty: {repetition_penalty}\n")
            file.write(f"Temperature: {temperature}\n")
            file.write(f"Top P: {top_p}\n")
            file.write(f"Top K: {top_k}\n")
            file.write(f"Seed: {seed}\n")
            file.write("\n")
            file.write("Output:\n")
            file.write(text)
            file.write("\n\n")
        output_text.insert(tk.END, "\n\n- Log file saved to superprompter_log.txt\n")

# Create the main window
window = tk.Tk()
window.title("SuperPrompter")
window.geometry("800x600")  # Set initial window size

# Set the default font for all widgets
window.option_add("*Font", "SF Pro Text 15")
window.option_add("*Font", "SF Pro 15")
window.option_add("*Font", "helvetica 15")
window.option_add("*TCombobox*Listbox*Font", "helvetica 15")
window.option_add("*TCombobox*Listbox*Height", "15")

# Center the window on the screen
window.update_idletasks()  # Update window geometry
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 800
window_height = 600
x_position = int((screen_width - window_width) / 2)
y_position = int((screen_height - window_height) / 2)
window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Configure grid weights for responsive layout
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

# Create a splash frame
splash_frame = ttk.Frame(window, padding="10")
splash_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
splash_frame.columnconfigure(0, weight=1)
splash_frame.rowconfigure(0, weight=1)

# Create a splash text area
splash_text = scrolledtext.ScrolledText(splash_frame, height=10, width=50)
splash_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create a main frame (hidden initially)
main_frame = ttk.Frame(window, padding="10")

# Configure grid weights for responsive layout
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(1, weight=1)  # Expand input text area
main_frame.rowconfigure(10, weight=1)  # Expand output text area

# Create input labels and entries
input_text_label = ttk.Label(main_frame, text="Your Prompt:")
input_text_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
input_text_entry = scrolledtext.ScrolledText(main_frame, height=5, width=50)
input_text_entry.focus()
input_text_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

max_new_tokens_label = ttk.Label(main_frame, text="Max New Tokens:")
max_new_tokens_label.grid(row=2, column=0, sticky=tk.W)
max_new_tokens_entry = ttk.Entry(main_frame)
max_new_tokens_entry.insert(0, "512")
max_new_tokens_entry.grid(row=2, column=1, sticky=tk.W)

repetition_penalty_label = ttk.Label(main_frame, text="Repetition Penalty:")
repetition_penalty_label.grid(row=3, column=0, sticky=tk.W)
repetition_penalty_entry = ttk.Entry(main_frame)
repetition_penalty_entry.insert(0, "1.2")
repetition_penalty_entry.grid(row=3, column=1, sticky=tk.W)

temperature_label = ttk.Label(main_frame, text="Temperature:")
temperature_label.grid(row=4, column=0, sticky=tk.W)
temperature_entry = ttk.Entry(main_frame)
temperature_entry.insert(0, "0.5")
temperature_entry.grid(row=4, column=1, sticky=tk.W)

top_p_label = ttk.Label(main_frame, text="Top P:")
top_p_label.grid(row=5, column=0, sticky=tk.W)
top_p_entry = ttk.Entry(main_frame)
top_p_entry.insert(0, "1")
top_p_entry.grid(row=5, column=1, sticky=tk.W)

top_k_label = ttk.Label(main_frame, text="Top K:")
top_k_label.grid(row=6, column=0, sticky=tk.W)
top_k_entry = ttk.Entry(main_frame)
top_k_entry.insert(0, "1")
top_k_entry.grid(row=6, column=1, sticky=tk.W)

seed_label = ttk.Label(main_frame, text="Seed:")
seed_label.grid(row=7, column=0, sticky=tk.W)
seed_entry = ttk.Entry(main_frame)
seed_entry.insert(0, "42")
seed_entry.grid(row=7, column=1, sticky=tk.W)

# Create a checkbox for enabling/disabling logging
log_var = tk.BooleanVar()
log_checkbox = ttk.Checkbutton(main_frame, text="Enable Logging", variable=log_var)
log_checkbox.grid(row=8, column=0, sticky=tk.W, pady=(10, 0))

# Create generate button
generate_button = ttk.Button(main_frame, text="Generate", command=answer)
generate_button.grid(row=8, column=1, pady=(10, 0))
generate_button.config(width=30)
window.bind('<Return>', lambda event: generate_button.invoke())

# Create output label and text area
output_label = ttk.Label(main_frame, text="Output:")
output_label.grid(row=9, column=0, sticky=tk.W, pady=(10, 5))

output_text = scrolledtext.ScrolledText(main_frame, height=10, width=50)
output_text.grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

# Start the model download in a separate thread
window.after(0, load_models)

# Run the main event loop
window.mainloop()
