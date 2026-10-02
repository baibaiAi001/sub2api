#!/usr/bin/env python3
"""Check the approved local extension scope without accessing production."""
from pathlib import Path
import subprocess
root = Path(__file__).resolve().parents[2]
expected = {'image-generation', 'tutorials'}
assert {p.name for p in (root / 'backend/internal/extensions').iterdir() if p.is_dir()} == expected
for name in ('deepseek-harness', 'local-tools', 'pelican', 'model-plaza'):
    assert not (root / 'frontend/src/features' / name).exists(), name
assert not list((root / 'backend/migrations').glob('*_local_pelican_*.sql'))
assert not subprocess.check_output(['git', 'diff', 'production', '--', 'backend/internal/service/model_plaza_service.go', 'backend/internal/service/payment_amounts.go'], cwd=root)
print('Approved four-extension scope verified; native pricing and model plaza retained.')
