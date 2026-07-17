import math


def precision_at_k(
    retrieved: list,
    relevant: list,
    k: int,
) -> float:
    """
    Precision@K

    retrieved:
        [14, 8, 20, 15, 3]

    relevant:
        [14, 15]
    """

    retrieved_k = retrieved[:k]

    if len(retrieved_k) == 0:
        return 0.0

    hits = sum(
        1
        for page in retrieved_k
        if page in relevant
    )

    return hits / len(retrieved_k)


def recall_at_k(
    retrieved: list,
    relevant: list,
    k: int,
) -> float:
    """
    Recall@K
    """

    if len(relevant) == 0:
        return 0.0

    retrieved_k = retrieved[:k]

    hits = sum(
        1
        for page in retrieved_k
        if page in relevant
    )

    return hits / len(relevant)


def reciprocal_rank(
    retrieved: list,
    relevant: list,
) -> float:
    """
    Reciprocal Rank (RR)

    Example

    retrieved:
    [8,5,14,2]

    relevant:
    [14]

    RR = 1/3
    """

    for rank, page in enumerate(
        retrieved,
        start=1,
    ):

        if page in relevant:
            return 1.0 / rank

    return 0.0


def mean_reciprocal_rank(
    reciprocal_ranks: list[float],
) -> float:
    """
    Mean Reciprocal Rank
    """

    if not reciprocal_ranks:
        return 0.0

    return sum(reciprocal_ranks) / len(reciprocal_ranks)


def dcg_at_k(
    retrieved: list,
    relevant: list,
    k: int,
) -> float:
    """
    Discounted Cumulative Gain
    """

    dcg = 0.0

    for rank, page in enumerate(
        retrieved[:k],
        start=1,
    ):

        if page in relevant:

            dcg += 1 / math.log2(rank + 1)

    return dcg


def idcg_at_k(
    relevant_count: int,
    k: int,
) -> float:
    """
    Ideal DCG
    """

    ideal = min(
        relevant_count,
        k,
    )

    idcg = 0.0

    for rank in range(
        1,
        ideal + 1,
    ):

        idcg += 1 / math.log2(rank + 1)

    return idcg


def ndcg_at_k(
    retrieved: list,
    relevant: list,
    k: int,
) -> float:
    """
    Normalized DCG
    """

    dcg = dcg_at_k(
        retrieved,
        relevant,
        k,
    )

    idcg = idcg_at_k(
        len(relevant),
        k,
    )

    if idcg == 0:
        return 0.0

    return dcg / idcg