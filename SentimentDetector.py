import tkinter as tk
from tkinter import ttk
import re

# --- Sentiment lexicon ---

POSITIVE_WORDS = {
    "good", "great", "excellent", "happy", "joy", "love", "like", "awesome",
    "fantastic", "amazing", "wonderful", "positive", "nice", "pleasant",
    "satisfied", "delighted", "enjoy", "enthusiastic", "glad", "smile"
}

NEGATIVE_WORDS = {
    "bad", "terrible", "awful", "sad", "angry", "hate", "dislike", "horrible",
    "disgusting", "upset", "unhappy", "negative", "worse", "worst", "annoyed",
    "frustrated", "depressed", "miserable", "cry", "pain"
}

def get_sentiment_score(text: str) -> float:
    tokens = re.findall(r"\b\w+\b", text.lower())
    if not tokens:
        return 0.0

    pos_count = 0
    neg_count = 0

    for token in tokens:
        if token in POSITIVE_WORDS:
            pos_count += 1
        elif token in NEGATIVE_WORDS:
            neg_count += 1

    total_sentiment_words = pos_count + neg_count
    if total_sentiment_words == 0:
        return 0.0

    score = (pos_count - neg_count) / total_sentiment_words
    return score

def interpret_score(score: float) -> str:
    if score > 0.5:
        return "Strongly positive"
    elif score > 0.1:
        return "Slightly positive"
    elif score >= -0.1:
        return "Neutral or mixed"
    elif score >= -0.5:
        return "Slightly negative"
    else:
        return "Strongly negative"

# --- GUI logic ---

def analyze_sentiment():
    text = text_input.get("1.0", tk.END).strip()
    score = get_sentiment_score(text)
    interpretation = interpret_score(score)

    score_var.set(f"{score:.2f}")
    label_var.set(interpretation)

    # Color feedback in the “badge” label
    if score > 0.1:
        result_label.config(foreground="#0c7c0c")   # green
    elif score < -0.1:
        result_label.config(foreground="#b01010")   # red
    else:
        result_label.config(foreground="#333333")   # neutral

def clear_text():
    text_input.delete("1.0", tk.END)
    score_var.set("--")
    label_var.set("No analysis yet")

def center_window(root, width=700, height=400):
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

def main():
    global text_input, score_var, label_var, result_label

    root = tk.Tk()
    root.title("Sentiment Analyzer")

    # Use a nicer ttk theme if available
    style = ttk.Style()
    # This will pick the OS default, but we can try 'clam', 'alt', etc.
    if "clam" in style.theme_names():
        style.theme_use("clam")

    # Base font tweaks (optional)
    default_font = ("Segoe UI", 10)       # Windows-like
    header_font = ("Segoe UI", 14, "bold")
    style.configure("TLabel", font=default_font)
    style.configure("TButton", font=default_font)
    style.configure("Heading.TLabel", font=header_font)

    # Overall padding frame
    main_frame = ttk.Frame(root, padding="15 15 15 15")
    main_frame.grid(row=0, column=0, sticky="NSEW")

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Title
    title_label = ttk.Label(
        main_frame,
        text="Simple Sentiment Analyzer",
        style="Heading.TLabel"
    )
    title_label.grid(row=0, column=0, columnspan=3, sticky="W")

    subtitle_label = ttk.Label(
        main_frame,
        text="Type or paste text below, then click Analyze to gauge emotional positivity."
    )
    subtitle_label.grid(row=1, column=0, columnspan=3, sticky="W", pady=(2, 10))

    # Text label
    input_label = ttk.Label(main_frame, text="Text to analyze:")
    input_label.grid(row=2, column=0, columnspan=3, sticky="W")

    # Text box with scrollbar
    text_frame = ttk.Frame(main_frame)
    text_frame.grid(row=3, column=0, columnspan=3, sticky="NSEW", pady=(5, 10))

    text_input = tk.Text(
        text_frame,
        width=80,
        height=10,
        wrap="word",
        font=("Segoe UI", 10),
        borderwidth=1,
        relief="solid"
    )
    text_input.grid(row=0, column=0, sticky="NSEW")

    scrollbar = ttk.Scrollbar(
        text_frame,
        orient="vertical",
        command=text_input.yview
    )
    scrollbar.grid(row=0, column=1, sticky="NS")
    text_input.configure(yscrollcommand=scrollbar.set)

    text_frame.columnconfigure(0, weight=1)
    text_frame.rowconfigure(0, weight=1)

    # Buttons row
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=4, column=0, columnspan=3, sticky="EW")

    analyze_button = ttk.Button(button_frame, text="Analyze", command=analyze_sentiment)
    analyze_button.grid(row=0, column=0, padx=(0, 8))

    clear_button = ttk.Button(button_frame, text="Clear", command=clear_text)
    clear_button.grid(row=0, column=1)

    button_frame.columnconfigure(0, weight=0)
    button_frame.columnconfigure(1, weight=0)
    button_frame.columnconfigure(2, weight=1)

    # Result section with a “card” feel
    result_frame = ttk.LabelFrame(main_frame, text="Result", padding="10 8 10 8")
    result_frame.grid(row=5, column=0, columnspan=3, sticky="EW", pady=(12, 0))

    ttk.Label(result_frame, text="Score:").grid(row=0, column=0, sticky="W")
    score_var = tk.StringVar(value="--")
    score_value_label = ttk.Label(result_frame, textvariable=score_var)
    score_value_label.grid(row=0, column=1, sticky="W", padx=(4, 15))

    ttk.Label(result_frame, text="Overall sentiment:").grid(row=0, column=2, sticky="W")
    label_var = tk.StringVar(value="No analysis yet")

    result_label = ttk.Label(result_frame, textvariable=label_var)
    result_label.grid(row=0, column=3, sticky="W", padx=(4, 0))

    # Make result frame expand a bit horizontally
    for i in range(4):
        result_frame.columnconfigure(i, weight=1 if i == 3 else 0)

    # Configure row/column resizing
    main_frame.rowconfigure(3, weight=1)   # text area
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.columnconfigure(2, weight=1)

    center_window(root, width=700, height=430)
    root.mainloop()

if __name__ == "__main__":
    main()
