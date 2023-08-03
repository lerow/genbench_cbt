import re
from typing import Any, Dict, List

import datasets

from genbench import Task
from genbench.utils.logging import get_logger


logger = get_logger(__name__)


class QuantifierUnderstandingTask(Task):
    def parse_output(s: str) -> str:
        # if true return 1 else return 0

        s = s.strip().split()

        for token in s:
            if len(token) < 7:
                token = re.sub(r"[^a-zA-Z]", "", token).lower()
                if token == "true":
                    return "true"
                if token == "false":
                    return "false"

        return "false"

    def evaluate_predictions(
        self, *, predictions: List[Dict[str, Any]] = None, gold: datasets.Dataset = None
    ) -> float:
        preds = [pred["target"] for pred in predictions]
        gold_labels = [g["target"] for g in gold]

        count = 0
        total = len(preds)

        for n in range(total):
            label = self.parse_output(preds[n])
            if label == gold_labels[n]:
                count += 1

        return count / total
