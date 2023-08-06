import unittest
import torch
from irisml.tasks.get_targets_from_dataset import Task

from utils import FakeDataset


class TestGetTargetsFromDataset(unittest.TestCase):
    def test_simple(self):

        data = [('image0', 0), ('image1', 2), ('image2', 4)]
        inputs = Task.Inputs(FakeDataset(data))
        outputs = Task(Task.Config()).execute(inputs)

        targets = outputs.targets

        self.assertIsInstance(targets, torch.Tensor)
        self.assertEqual(targets.tolist(), [0, 2, 4])
