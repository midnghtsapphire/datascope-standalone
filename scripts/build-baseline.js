const { spawnSync } = require('node:child_process');

const pythonCommands = ['python3', 'python'];
let selectedPython = null;
let lastPythonError = null;

for (const pythonCommand of pythonCommands) {
  const result = spawnSync(pythonCommand, ['--version'], {
    stdio: 'inherit',
  });

  if (result.error) {
    if (result.error.code === 'ENOENT') {
      lastPythonError = result.error;
      continue;
    }

    console.error(result.error);
    process.exit(result.status ?? 1);
  }

  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }

  selectedPython = pythonCommand;
  break;
}

if (!selectedPython) {
  if (lastPythonError) {
    console.error(lastPythonError);
  }
  process.exit(1);
}

const pythonBuildCheck = spawnSync(selectedPython, ['setup.py', 'check'], {
  stdio: 'inherit',
});

if (pythonBuildCheck.error) {
  console.error(pythonBuildCheck.error);
  process.exit(pythonBuildCheck.status ?? 1);
}

if (pythonBuildCheck.status !== 0) {
  process.exit(pythonBuildCheck.status ?? 1);
}

const corepackEnable = spawnSync('corepack', ['enable'], {
  stdio: 'inherit',
});

if (corepackEnable.error) {
  console.error(corepackEnable.error);
  process.exit(corepackEnable.status ?? 1);
}

if (corepackEnable.status !== 0) {
  process.exit(corepackEnable.status ?? 1);
}

const corepackPrepare = spawnSync('corepack', ['prepare', 'pnpm@10.4.1', '--activate'], {
  stdio: 'inherit',
});

if (corepackPrepare.error) {
  console.error(corepackPrepare.error);
  process.exit(corepackPrepare.status ?? 1);
}

if (corepackPrepare.status !== 0) {
  process.exit(corepackPrepare.status ?? 1);
}

const frontendInstall = spawnSync(
  'pnpm',
  ['--dir', 'cybersecurity-threat-dashboard', 'install', '--frozen-lockfile'],
  { stdio: 'inherit' },
);

if (frontendInstall.error) {
  console.error(frontendInstall.error);
  process.exit(frontendInstall.status ?? 1);
}

if (frontendInstall.status !== 0) {
  process.exit(frontendInstall.status ?? 1);
}

const frontendBuild = spawnSync('pnpm', ['--dir', 'cybersecurity-threat-dashboard', 'build'], {
  stdio: 'inherit',
});

if (frontendBuild.error) {
  console.error(frontendBuild.error);
  process.exit(frontendBuild.status ?? 1);
}

if (frontendBuild.status !== 0) {
  process.exit(frontendBuild.status ?? 1);
}

console.log('Baseline build validation passed.');
process.exit(0);
