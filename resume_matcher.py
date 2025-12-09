import os
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_text_file(path: Path) -> str:
    """Read text from a file and return as string."""
    with path.open("r", encoding="utf-8") as f:
        return f.read()


def load_resumes(resume_dir: Path):
    """
    Load all .txt files from resume_dir.
    Returns:
        - list of file names
        - list of resume texts
    """
    resume_files = sorted(resume_dir.glob("*.txt"))
    names = [f.name for f in resume_files]
    texts = [load_text_file(f) for f in resume_files]
    return names, texts


def rank_resumes(job_description: str, resume_texts: list[str]) -> list[tuple[int, float]]:
    """
    Compute cosine similarity between job description and each resume
    using TF-IDF vectors.

    Returns a list of (index, score) sorted by score descending.
    """
    documents = [job_description] + resume_texts

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    jd_vec = tfidf_matrix[0:1]
    resume_vecs = tfidf_matrix[1:]

    similarities = cosine_similarity(jd_vec, resume_vecs)[0]

    indexed_scores = list(enumerate(similarities))
    ranked = sorted(indexed_scores, key=lambda x: x[1], reverse=True)
    return ranked


def main():
    base_dir = Path(__file__).resolve().parent

    job_desc_path = base_dir / "job_description.txt"
    resume_dir = base_dir / "resumes"

    if not job_desc_path.exists():
        raise FileNotFoundError(f"job_description.txt not found at {job_desc_path}")

    if not resume_dir.exists():
        raise FileNotFoundError(f"resumes folder not found at {resume_dir}")

    job_description = load_text_file(job_desc_path)
    resume_names, resume_texts = load_resumes(resume_dir)

    if not resume_texts:
        print("No resume .txt files found in the resumes folder.")
        return

    ranked = rank_resumes(job_description, resume_texts)

    print("Job description:")
    print(job_description.strip())
    print("\nResume match scores (higher is better):\n")

    for idx, score in ranked:
        print(f"{resume_names[idx]}  ->  similarity: {score:.3f}")

    print("\nTop match:")
    best_idx, best_score = ranked[0]
    print(f"{resume_names[best_idx]} with score {best_score:.3f}")


if __name__ == "__main__":
    main()
