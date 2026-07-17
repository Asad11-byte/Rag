import csv
from pathlib import Path

from app.services.rag_service import RagService

from evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
    mean_reciprocal_rank,
    ndcg_at_k,
)

DATASET = Path("evaluation/evaluation_dataset.csv")
RESULTS = Path("evaluation/results.csv")

K = 5


def parse_pages(page_string: str):

    return [
        int(page.strip())
        for page in page_string.split(";")
        if page.strip()
    ]


def main():

    rag = RagService()

    rows = []

    reciprocal_ranks = []

    precision_scores = []

    recall_scores = []

    ndcg_scores = []

    with open(
        DATASET,
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        for sample in reader:

            question = sample["question"]

            relevant_pages = parse_pages(
                sample["relevant_pages"]
            )

            retrieval = rag.retrieve(
                question,
                limit=K,
            )

            retrieved_pages = [
                item["page"]
                for item in retrieval["retrieved"]
            ]

            p = precision_at_k(
                retrieved_pages,
                relevant_pages,
                K,
            )

            r = recall_at_k(
                retrieved_pages,
                relevant_pages,
                K,
            )

            rr = reciprocal_rank(
                retrieved_pages,
                relevant_pages,
            )

            n = ndcg_at_k(
                retrieved_pages,
                relevant_pages,
                K,
            )

            precision_scores.append(p)

            recall_scores.append(r)

            reciprocal_ranks.append(rr)

            ndcg_scores.append(n)

            rows.append(
                {
                    "question": question,
                    "retrieved": str(retrieved_pages),
                    "expected": str(relevant_pages),
                    "precision@5": round(p, 3),
                    "recall@5": round(r, 3),
                    "rr": round(rr, 3),
                    "ndcg@5": round(n, 3),
                }
            )

    with open(
        RESULTS,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys(),
        )

        writer.writeheader()

        writer.writerows(rows)

    print("\n========== FINAL RESULTS ==========\n")

    print(
        f"Precision@{K}: "
        f"{sum(precision_scores)/len(precision_scores):.3f}"
    )

    print(
        f"Recall@{K}: "
        f"{sum(recall_scores)/len(recall_scores):.3f}"
    )

    print(
        f"MRR: "
        f"{mean_reciprocal_rank(reciprocal_ranks):.3f}"
    )

    print(
        f"nDCG@{K}: "
        f"{sum(ndcg_scores)/len(ndcg_scores):.3f}"
    )

    print("\nresults.csv generated successfully.")


if __name__ == "__main__":
    main()