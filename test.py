from dataset_generator import produceSpeechDataset
from dataset_generator import create_histogram
objects = produceSpeechDataset('sansone', 'en', '/Users/cirosannino/Downloads/Dataset - Sansone ML (EN)/', 'output_dataset_en/', 12, 40, 5, 15)
create_histogram(objects)