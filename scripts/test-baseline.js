const fs = require('node:fs');
const path = require('node:path');

const requiredFiles = [
  'README.md',
  'CHANGELOG.md',
  'DEPLOYMENT_GUIDE.md',
  'GO_TO_MARKET.md',
  'BRAND_GUIDELINES.md',
  'SECURITY.md',
  'RESEARCH_ENGINES.md',
  'SUGGESTIONS.md',
  'ASSET_INVENTORY.md',
  'ARTIFACTS.md',
];

const missing = requiredFiles.filter((file) => !fs.existsSync(path.resolve(process.cwd(), file)));

if (missing.length > 0) {
  console.error(`Missing required revvel-standards files:\n- ${missing.join('\n- ')}`);
  process.exit(1);
}

console.log('Revvel-standards baseline test passed.');
