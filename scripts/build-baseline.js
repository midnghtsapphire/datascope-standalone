const { spawnSync } = require('node:child_process');

const FRONTEND_DIR = 'cybersecurity-threat-dashboard';
const FRONTEND_PNPM_VERSION = '10.4.1';

function runOrExit(command, args) {
  const result = spawnSync(command, args, {
    stdio: 'inherit',
  });

  if (result.error) {
    console.error(result.error);
    process.exit(1);
  }

  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }
}

const pythonCommands = ['python3', 'python'];
let selectedPython = null;
let lastPythonEnoent = null;

for (const pythonCommand of pythonCommands) {
  const result = spawnSync(pythonCommand, ['setup.py', 'check'], {
    stdio: 'inherit',
  });

  if (result.error) {
    if (result.error.code === 'ENOENT') {
      lastPythonEnoent = result.error;
      continue;
    }

    console.error(result.error);
    process.exit(1);
  }

  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }

  selectedPython = pythonCommand;
  break;
}

if (!selectedPython) {
  if (lastPythonEnoent) {
    console.error(lastPythonEnoent);
  }
  process.exit(1);
}

runOrExit(selectedPython, ['--version']);
runOrExit('corepack', ['enable']);
runOrExit('corepack', ['prepare', `pnpm@${FRONTEND_PNPM_VERSION}`, '--activate']);
runOrExit('pnpm', ['--dir', FRONTEND_DIR, 'install', '--frozen-lockfile']);
runOrExit('pnpm', ['--dir', FRONTEND_DIR, 'build']);

console.log('Baseline build validation passed.');
process.exit(0);
