const { spawnSync } = require('node:child_process');

const pythonCommands = ['python3', 'python'];
let lastError = null;

for (const pythonCommand of pythonCommands) {
  const result = spawnSync(pythonCommand, ['setup.py', '--version'], {
    stdio: 'inherit',
  });

  if (result.error) {
    if (result.error.code === 'ENOENT') {
      lastError = result.error;
      continue;
    }

    console.error(result.error);
    process.exit(result.status ?? 1);
  }

  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }

  console.log('Baseline build validation passed.');
  process.exit(0);
}

if (lastError) {
  console.error(lastError);
}

process.exit(1);
