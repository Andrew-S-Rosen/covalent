# Copyright 2021 Agnostiq Inc.
#
# This file is part of Covalent.
#
# Licensed under the Apache License 2.0 (the "License"). A copy of the
# License may be obtained with this software package or at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Use of this file is prohibited except in compliance with the License.
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Workflow with both cpu and mem intensive tasks, all independent
# Graph looks like
# e e e ...

import math
import os
import time

import numpy as np
import scipy.fft as fft
import yaml

import covalent as ct

benchmark_name = "parallel_cpumem"
benchmark_dir = f"benchmark_results/{benchmark_name}/current"

if not os.path.isdir(benchmark_dir):
    os.makedirs(benchmark_dir)

widths = [2**i for i in range(4)]
trials_per_width = 3


# Single layer of independent electrons; half cpu and half mem
# e e e ...


def fft_test(width, n_iterations):
    gen = np.random.default_rng()
    X = gen.random(width)
    nX = np.sqrt(np.sum(X * X))
    X /= nX
    for i in range(n_iterations):
        res = fft.fft(X)

    res = fft.ifft(res)
    return np.max(np.abs(X - res))


# This uses about 600 MB on my system and completes in 3s
def sample_mem_task(*args, **kwargs):
    fft_test(10000000, 3)


def sample_task(*args, **kwargs):
    return 1


def test_prime(n):
    m = int(math.floor(math.sqrt(n)))
    for d in range(2, m + 1):
        if n % d == 0:
            return False
    return True


# This takes 9s on my system
def sample_cpu_task(*args, **kwargs):
    res = []
    for i in range(2, 1000000):
        res.append(test_prime(i))
    return res


# General workflow with a feedforward transport graph
# Each task can depend on any number of tasks in the previous layer
def feedforward_workflow(tasks, predecessors):
    """General workflow with a feedforward-type transport graph.

    The graph is expressed as a list of task lists. Each task can
    depend on any number of tasks in the previous layer as specified
    by `predecessors`. The top layer of tasks is assumed to accept no
    inputs. For instance,

    tasks = [ [task00, task01], [task10, task11], [task20, task21]]
    predecessors = [ [[0, 1], [0]], [[1], [1]] ]

    expresses a transport graph in which task10 depends on task00 and task01,
    task11 depends on task00, and task20 and task21 each depend only task11.

    """
    electrons = [[ct.electron(tasks[0][j])() for j in range(len(tasks[0]))]]
    for i in range(1, len(tasks)):
        next_electrons = []
        for j in range(len(tasks[i])):
            args = [electrons[i - 1][k] for k in predecessors[i - 1][j]]
            next_electrons.append(ct.electron(tasks[i][j])(*args))
        electrons.append(next_electrons)
    return 1


# Without covalent
for w in widths:
    tasks = [[sample_cpu_task for i in range(w)]]
    for i in range(int(w / 2), w):
        tasks[0][i] = sample_mem_task

    deps = []
    for i in range(trials_per_width):
        workflow = ct.lattice(feedforward_workflow)

        start = time.time()
        res = workflow(tasks, deps)
        end = time.time()

        outfile = f"{benchmark_dir}/no_ct_width_{w}_trial_{i}"
        with open(outfile, "w") as f:
            yaml.dump({"test": benchmark_name, "ct": False, "width": w, "runtime": end - start}, f)
        print("(w/o ct) runtime for width {}: {} seconds".format(w, end - start))

time.sleep(3)

# With covalent
for w in widths:
    tasks = [[sample_cpu_task for i in range(w)]]
    for i in range(int(w / 2), w):
        tasks[0][i] = sample_mem_task

    deps = []
    for i in range(trials_per_width):
        workflow = ct.lattice(feedforward_workflow)

        result = ct.dispatch_sync(workflow)(tasks, deps)

        assert result.status == ct.status.COMPLETED

        outfile = f"{benchmark_dir}/{result.dispatch_id}"
        with open(outfile, "w") as f:
            yaml.dump(
                {
                    "test": benchmark_name,
                    "ct": True,
                    "dispatch_id": result.dispatch_id,
                    "width": w,
                    "runtime": (result.end_time - result.start_time).total_seconds(),
                },
                f,
            )
        print("runtime for width {}: {} seconds".format(w, result.end_time - result.start_time))
