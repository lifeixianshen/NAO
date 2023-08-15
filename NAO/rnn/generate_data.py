import os
import sys
import numpy as np

dag_folder='search/scripts'
score_folder='search/logs/scores'

inputs = []
targets = []

all_data = range(1,1509)
for index in all_data:
  with open(os.path.join(dag_folder, f'{index}.arch'), 'r') as f:
    arch = f.readline().split()
    arch = list(map(int, arch))
    for i, e in enumerate(arch):
      arch[i] = arch[i] + 1 if i % 2 == 0 else arch[i] + 12
    arch = ' '.join(list(map(str, arch)))

  with open(os.path.join(score_folder, f'{index}.score'), 'r') as f:
    all_ppl = f.read().splitlines()
    all_ppl = list(map(float, all_ppl))
    try:
      min_all_ppl = np.min(all_ppl)
      inputs.append(arch)
      targets.append(min_all_ppl)
    except:
      print(f'{index}.score failed')

print(f'{len(inputs)} valid data in total')

min_val = min(targets)
max_val = max(targets)

print(min_val, np.argmin(targets))
print(max_val, np.argmax(targets))

norm_targets = [(i-min_val)/(max_val-min_val) for i in targets]

N = len(inputs)
assert len(targets) == N

train_input = open('train.input', 'w')
train_target = open('train.target', 'w')
train_gt_target = open('train.target.ground_truth', 'w')
test_input = open('test.input', 'w')
test_target = open('test.target', 'w')
test_gt_target = open('test.target.ground_truth', 'w')

for i in range(N):
  if i < 50:
    test_input.write(f'{inputs[i]}\n')
    test_target.write(f'{norm_targets[i]}\n')
    test_gt_target.write(f'{targets[i]}\n')
  else:
    train_input.write(f'{inputs[i]}\n')
    train_target.write(f'{norm_targets[i]}\n')
    train_gt_target.write(f'{targets[i]}\n')
