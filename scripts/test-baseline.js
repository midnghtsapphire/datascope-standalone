const { spawnSync } = require('node:child_process');
const { existsSync } = require('node:fs');
const { join } = require('node:path');

const requiredFiles = [
  'README.md',
  'CHANGELOG.md',
  'DEPLOYMENT_GUIDE.md',
  'GO_TO_MARKET.md',
  'BRAND_GUIDELINES.md',
  'SECURITY.md',
  'requirements.txt',
  'docker-compose.yml'
];

const missing = requiredFiles.filter((file) => !existsSync(join(process.cwd(), file)));
if (missing.length) {
  console.error('Missing required files:\n' + missing.join('\n'));
  process.exit(1);
}

const compile = spawnSync('python', ['-m', 'compileall', '-q', 'main.py', 'enhanced_main.py'], {
  stdio: 'inherit'
});

if (compile.status !== 0) {
  process.exit(compile.status ?? 1);
}

console.log('Baseline test checks passed.');
