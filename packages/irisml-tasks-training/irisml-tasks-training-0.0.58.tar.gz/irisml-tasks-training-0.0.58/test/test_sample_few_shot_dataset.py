import unittest
from irisml.tasks.sample_few_shot_dataset import Task


class TestSampleFewShotDataset(unittest.TestCase):
    def test_ic_multiclass_few_shot(self):
        dataset = [(None, [1]), (None, [1]), (None, [0])]
        outputs = Task(Task.Config(1, random_seed=2)).execute(Task.Inputs(dataset))
        self.assertEqual(len(outputs.dataset), 2)
        classes = set(t[0] for _, t in outputs.dataset)
        self.assertEqual(len(classes), 2)

    def test_od_few_shot(self):
        dataset = [(None, [[0, 0, 0, 0.5, 0.5], [1, 0.5, 0.5, 1, 1]]), (None, [[1, 0, 0, 0.2, 0.2], [1, 0.2, 0.2, 0.4, 0.4]]), (None, [[0, 0, 0, 1, 1]])]
        outputs = Task(Task.Config(2)).execute(Task.Inputs(dataset))
        self.assertEqual(len(outputs.dataset), 3)

        n_images_by_classes = {0: 0, 1: 0}
        for i in range(len(dataset)):
            target = dataset[i][1]
            classes = set(obj[0] for obj in target)
            for c in classes:
                n_images_by_classes[c] += 1

        for _, n_images in n_images_by_classes.items():
            self.assertGreaterEqual(n_images, 2)
