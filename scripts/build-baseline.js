const { spawnSync } = require('node:child_process');

const result = spawnSync('python', ['setup.py', '--version'], {
  stdio: 'inherit',
});

if (result.status !== 0) {
  process.exit(result.status ?? 1);
}

console.log('Baseline build validation passed.');
