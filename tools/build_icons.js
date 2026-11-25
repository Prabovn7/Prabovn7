// Builds assets/icons/*.svg (monochrome, local) and tools/icon_paths.json.
// Run from /tmp/iconsrc (has simple-icons + lucide-static):  node build_icons.js <profileDir>
const fs = require('fs'), path = require('path');
const si = require('simple-icons');
const profile = process.argv[2];
const GRAY = '#8b8b8b';
const brands = { python:'siPython', java:'siOpenjdk', c:'siC', javascript:'siJavascript', typescript:'siTypescript',
  fastapi:'siFastapi', flask:'siFlask', spring:'siSpring', nodejs:'siNodedotjs', postgresql:'siPostgresql',
  sqlite:'siSqlite', redis:'siRedis', docker:'siDocker', git:'siGit', github:'siGithub',
  'github-actions':'siGithubactions', pytest:'siPytest', sqlalchemy:'siSqlalchemy', jwt:'siJsonwebtokens' };
const lucide = { vscode:'code-xml', linkedin:'link', terminal:'terminal', folder:'folder-git-2', layers:'layers',
  clock:'clock', activity:'activity', mail:'mail', user:'user', shield:'shield-check', rocket:'rocket',
  map:'map', database:'database', server:'server', lock:'lock', cpu:'cpu', briefcase:'briefcase', bus:'bus',
  truck:'truck', weather:'cloud-sun', key:'key-round', route:'route', wrench:'wrench', zap:'zap',
  branch:'git-branch', history:'history', sparkles:'sparkles', target:'target', package:'package', globe:'globe',
  chart:'chart-column', book:'book-open', flame:'flame', badge:'badge-check', grad:'graduation-cap' };
const out = {}, dir = path.join(profile, 'assets', 'icons');
fs.mkdirSync(dir, { recursive: true });
for (const [name, key] of Object.entries(brands)) {
  const p = si[key].path;
  out[name] = { type: 'brand', path: p, hex: '#' + si[key].hex };
}
for (const [name, file] of Object.entries(lucide)) {
  const raw = fs.readFileSync(path.join('node_modules/lucide-static/icons', file + '.svg'), 'utf8');
  const inner = raw.replace(/^[\s\S]*?<svg[^>]*>/, '').replace(/<\/svg>\s*$/, '').replace(/<!--[\s\S]*?-->/g, '').trim();
  out[name] = { type: 'lucide', inner };
}
fs.writeFileSync(path.join(profile, 'tools', 'icon_paths.json'), JSON.stringify(out, null, 1));
console.log(Object.keys(out).length, 'icons');
