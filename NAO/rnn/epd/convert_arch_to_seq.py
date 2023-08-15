import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data_dir', type=str, default='data/0iter/')
args = parser.parse_args()

inputs = []

with open(os.path.join(args.data_dir, 'valid_ppl'), 'r') as f:
  targets = f.read().splitlines()
targets = list(map(float, targets))
N=len(targets)
for index in range(1,N+1):
  with open(os.path.join(args.data_dir, f'{index}.arch'), 'r') as f:
    line = f.readline()
  arch = list(map(int, line.strip().split()))
  for i, e in enumerate(arch):
    arch[i] = arch[i] + 1 if i % 2 == 0 else arch[i] + 12
  arch = ' '.join(list(map(str, arch)))
  inputs.append(arch)

min_val = min(targets)
max_val = max(targets)

print(targets.index(min_val), min_val)
print(targets.index(max_val), max_val)

norm_targets = [(i-min_val)/(max_val-min_val) for i in targets]

encoder_train_input = open(os.path.join(args.data_dir, 'encoder.train.input'), 'w')
encoder_train_target = open(os.path.join(args.data_dir, 'encoder.train.target'), 'w')
decoder_train_target = open(os.path.join(args.data_dir, 'decoder.train.target'), 'w')
train_gt_target = open(os.path.join(args.data_dir, 'train.target.ground_truth'), 'w')
encoder_test_input = open(os.path.join(args.data_dir, 'encoder.test.input'), 'w')
encoder_test_target = open(os.path.join(args.data_dir, 'encoder.test.target'), 'w')
decoder_test_target = open(os.path.join(args.data_dir, 'decoder.test.target'), 'w')
test_gt_target = open(os.path.join(args.data_dir, 'test.target.ground_truth'), 'w')

for i in range(N):
  if i < 50:
    encoder_test_input.write(f'{inputs[i]}\n')
    encoder_test_target.write(f'{norm_targets[i]}\n')
    decoder_test_target.write(f'{inputs[i]}\n')
    test_gt_target.write(f'{targets[i]}\n')
  encoder_train_input.write(f'{inputs[i]}\n')
  encoder_train_target.write(f'{norm_targets[i]}\n')
  decoder_train_target.write(f'{inputs[i]}\n')
  train_gt_target.write(f'{targets[i]}\n')
