const { spawnSync } = require('node:child_process');

const build = spawnSync('npm', ['--prefix', 'cybersecurity-threat-dashboard', 'run', 'build'], {
  stdio: 'inherit'
});

if (build.status !== 0) {
  process.exit(build.status ?? 1);
}

console.log('Baseline build check passed.');
