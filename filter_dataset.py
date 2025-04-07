import pandas as pd
import re
import os


def filter_atc_dataset(csv_path, output_csv_path, audio_dir=None, min_words=5, min_duration=1.5):
    """
    Filter ATC radio transcriptions to find usable clips.
    
    Parameters:
        csv_path: Path to CSV file with transcriptions and file paths
        output_csv_path: Path to save filtered dataset
        audio_dir: Optional directory containing audio files (if paths in CSV are relative)
        min_words: Minimum number of words for a usable clip
        min_duration: Minimum duration in seconds for a usable clip
    """
    # Load the dataset
    print(f"Loading dataset from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    print(f"Original dataset size: {len(df)} clips")
    
    # Add a column for word count
    df['word_count'] = df['text'].apply(lambda x: len(str(x).split()))
    
    # Filter by word count first (fast operation)
    df_filtered = df[df['word_count'] >= min_words].copy()
    print(f"After word count filtering: {len(df_filtered)} clips")
    
    # Identify potential questions based on transcription patterns
    # Note: This is a heuristic approach and will need manual verification
    question_patterns = [
        r'\?',                    # Question mark
        r'\b(?:what|where|when|why|who|how|which)\b',  # WH-questions
        r'\b(?:do|does|did|is|are|was|were|have|has|had|can|could|will|would|should|may|might)\s+(?:\w+\s+)+\?',  # Yes/no questions
        r'\b(?:right|correct|copy|roger)\?',  # Common ATC confirmation questions
        r'say again',             # Common in ATC for clarification
        r'request',               # Often indicates a question in ATC context
        r'confirm',               # Confirmation requests
    ]
    
    # Create a combined pattern for detecting questions
    combined_pattern = '|'.join(question_patterns)
    
    # Mark potential questions
    df_filtered['potential_question'] = df_filtered['text'].apply(
        lambda x: bool(re.search(combined_pattern, str(x).lower())) if pd.notna(x) else False
    )
    
    # Mark potential statements (everything else)
    df_filtered['potential_statement'] = ~df_filtered['potential_question']
    
    # Save filtered dataset
    df_filtered.to_csv(output_csv_path, index=False)
    
    print(f"Filtered dataset saved to {output_csv_path}")
    print(f"Potential questions: {sum(df_filtered['potential_question'])}")
    print(f"Potential statements: {sum(df_filtered['potential_statement'])}")
    
    return df_filtered

def suggest_sample_clips(df, n_questions=5, n_statements=5):
    """
    Suggest sample clips for manual review
    """
    questions = df[df['potential_question']].head(n_questions)
    statements = df[df['potential_statement']].head(n_statements)
    
    print("\nSample potential questions:")
    for i, (_, row) in enumerate(questions.iterrows(), 1):
        print(f"{i}. {row['transcription']} (words: {row['word_count']})")
    
    print("\nSample potential statements:")
    for i, (_, row) in enumerate(statements.iterrows(), 1):
        print(f"{i}. {row['transcription']} (words: {row['word_count']})")

# Example usage
if __name__ == "__main__":
    # Replace with your actual paths
    csv_path = "train_data.csv"
    output_path = "filtered_train_data.csv"
    audio_directory = "path/to/audio/files"  # Optional
    
    filtered_df = filter_atc_dataset(
        csv_path, 
        output_path,
        audio_dir=None,
        min_words=2,
        min_duration=1.5
    )
    
    #suggest_sample_clips(filtered_df)  