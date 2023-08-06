from __future__ import annotations

import unittest
from dataclasses import dataclass
from typing import List, TypedDict

from ..blocks.completion import GPTCompletionBlock

_PROMPT = (
    "You are a test agent responsible for determining which answer to a question is better. "
    "We define better as being most similar to expected answer."
    "Respond with either 0 if first is better or 1 if second is better. \n"
    "The question is {question} \n"
    "The expected answer is {expected_response} \n"
    "The first answer is {first_actual_response} \n"
    "The second answer is {second_actual_response} \n"
    "The better answer is: "
)


class TestExample(TypedDict):
    question: str
    expected_response: str


class TestABPipelines(unittest.TestCase):
    example_list: list[TestExample] = []
    pipeline_response_generator = None
    score_treshold = 0
    gpt_block = None

    @classmethod
    def setUpClass(cls, open_ai_key="", pipeline_response_gen=None, score_threshold=50, examples=[]):
        cls.gpt_block = GPTCompletionBlock(open_ai_key=open_ai_key)
        cls.score_treshold = score_threshold
        cls.example_list = examples

    def test_examples(self):
        for testcase in self.example_list:
            res = self._test_example(testcase)
            self.assertEqual(int(res), 1)
    def _test_example(self, test_case: TestExample):
        generated_response_1 = self.pipeline_response_generator_first(test_case["question"])
        generated_response_2 = self.pipeline_response_generator_second(test_case["question"])
        expected = test_case["expected_response"]
        prompt = _PROMPT.format(
            question=test_case["question"],
            expected_response=expected,
            first_actual_response=generated_response_1,
            second_actual_response=generated_response_2,
        )
        res = self.gpt_block.get_completion(prompt, max_tokens=300, temperature=0)
        return res

