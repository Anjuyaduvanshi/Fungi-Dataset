import os
import json
import torch
from transformers import pipeline
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Function to load the model
def load_model(model_path, device_ids="0,1", precision=torch.float16):
    """
    Load the text generation model with device mapping and FP16 precision.
    """
    os.environ["CUDA_VISIBLE_DEVICES"] = device_ids  # Specify GPUs to use
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model path does not exist: {model_path}")
    logging.info(f"Loading model from {model_path}...")
    return pipeline(
        "text-generation",
        model=model_path,
        torch_dtype=precision,
        device_map="auto",
    )

# Function to generate captions for a specific class label
def refine_fungi_caption(generator, class_label, num_captions=50, min_length=10, max_new_tokens=50):
    """
    Generate captions for a given fungal growth stage with token constraints.

    Args:
    - generator: The text generation pipeline object.
    - class_label: The fungal growth stage (spore, hyphae, mycelium).
    - num_captions: Number of distinct captions to generate in each batch.
    - min_length: Minimum length for generated captions.
    - max_new_tokens: Maximum number of new tokens to generate after the prompt.

    Returns:
    - A list of generated captions.
    """
    prompts = {
        "spore": (
            "Early fungal spore"
        ),
        "hyphae": (
            "Growing hyphae structure"
        ),
        "mycelium": (
            "Mature fungal network"
        ),
    }

    prompt = prompts.get(class_label, "Describe the fungal growth process.")
    
    try:
        logging.info(f"Generating captions for: {class_label}")
        results = generator(
            prompt,
            max_new_tokens=max_new_tokens,
            num_return_sequences=num_captions,
            temperature=0.75,  # Increased randomness
            top_p=0.9,        # Increased top_p for more diverse outputs
            top_k=50,         # Consider more tokens for randomness
            do_sample=True,
        )
    except RuntimeError as e:
        if "out of memory" in str(e):
            logging.warning("CUDA out of memory. Clearing cache and retrying...")
            torch.cuda.empty_cache()
            results = generator(
                prompt,
                max_new_tokens=max_new_tokens,
                num_return_sequences=num_captions,
                temperature=0.75,
                top_p=0.9,
                top_k=50,
                do_sample=True,
            )
        else:
            raise e

    refined_captions = []
    for result in results:
        text = result["generated_text"].replace("\n", " ").strip()
        if not text.endswith((".", "!", "?")):
            text += "."
        if min_length <= len(text.split()):
            refined_captions.append(text)
    return refined_captions

# Function to generate captions for all fungal growth stages
def generate_captions_for_all_labels(generator, num_captions_per_label, min_length=10, max_length=70, batch_size=5):
    """
    Generate captions for all fungal growth stages in batches to avoid memory issues.

    Args:
    - generator: The text generation pipeline object.
    - num_captions_per_label: Total number of captions to generate for each class label.
    - min_length: Minimum length for each caption.
    - max_length: Maximum length for each caption.
    - batch_size: Number of captions to generate in each batch.

    Returns:
    - A list of dictionaries containing captions and their class labels.
    """
    class_labels = ["spore", "hyphae", "mycelium"]
    all_captions = []

    for class_label in class_labels:
        for batch_start in range(0, num_captions_per_label, batch_size):
            captions = refine_fungi_caption(generator, class_label, batch_size, min_length, max_length)
            torch.cuda.empty_cache()  # Clear GPU memory after each batch
            for caption in captions:
                all_captions.append({"description": caption, "class_label": class_label})
    return all_captions

# Save captions incrementally to JSON
def save_partial_results(captions, file_path):
    """
    Save captions incrementally to a JSON file.

    Args:
    - captions: List of captions to save.
    - file_path: Path to the JSON file.
    """
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    existing_data.extend(captions)

    with open(file_path, "w") as file:
        json.dump(existing_data, file, indent=4)
    logging.info(f"Saved {len(captions)} captions to {file_path}")

# Main function
def main():
    model_path = "/home/models/llama2/Llama-2-13b-chat-hf"
    output_file_path = "/home/generated_captions_13B.json"
    num_captions_per_label = 1000
    min_caption_length = 10
    max_caption_length = 70
    batch_size = 5

    # Initialize captions to avoid UnboundLocalError
    captions = []

    generator = load_model(model_path)

    try:
        captions = generate_captions_for_all_labels(
            generator, num_captions_per_label, min_caption_length, max_caption_length, batch_size
        )
        save_partial_results(captions, output_file_path)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        # Save whatever captions have been generated so far
        if captions:
            save_partial_results(captions, output_file_path)

if __name__ == "__main__":
    main()
