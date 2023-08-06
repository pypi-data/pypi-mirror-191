import dataclasses
import logging
from typing import Optional
import torch.utils.data
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Few-shot sampling of a IC/OD dataset.

    For n-shot, do random sampling until each category exists in at least n images or all images are sampled.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Config:
        n_shot: int
        random_seed: Optional[int] = None

    @dataclasses.dataclass
    class Inputs:
        dataset: torch.utils.data.Dataset

    @dataclasses.dataclass
    class Outputs:
        dataset: torch.utils.data.Dataset

    def execute(self, inputs):
        few_shot_dataset = FewShotDataset(inputs.dataset, self.config.n_shot, self.config.random_seed)
        return self.Outputs(few_shot_dataset)

    def dry_run(self, inputs):
        return self.execute(inputs)


class FewShotDataset(torch.utils.data.Dataset):
    def __init__(self, dataset, n_shots, random_seed):
        self._dataset = dataset
        self._img_ids = []

        import random
        from .make_oversampled_dataset import Task

        classes_by_images = []
        classes = set()
        for sample in dataset:
            image_classes = set(Task._get_class_id(sample))
            classes_by_images.append(image_classes)
            classes = classes.union(image_classes)

        classes_freq = [n_shots] * len(classes)
        # Random sample until satisfying classes_freq.
        ids = list(range(len(dataset)))
        random.Random(random_seed).shuffle(ids)
        self._id_mappings = []
        for i in ids:
            sample_needed = max(int(freq > 0) for freq in classes_freq)
            if sample_needed:
                self._id_mappings.append(i)
                for c in classes_by_images[i]:
                    classes_freq[int(c)] -= 1
            else:
                break

        logger.info(f"Sampled {n_shots}-shot dataset with seed {random_seed}: {len(dataset)} -> {len(self._id_mappings)} samples.")

    def __len__(self):
        return len(self._id_mappings)

    def __getitem__(self, index):
        new_id = self._id_mappings[index]
        assert isinstance(new_id, int)
        return self._dataset[new_id]
