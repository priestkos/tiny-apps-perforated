// Behaviour tests for the inline album script. Run: node --test tests/
// The page script runs in a vm with a minimal DOM stub, fake timers and a controlled fetch.
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const html = readFileSync(new URL('../index.html', import.meta.url), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];

function el() {
  const classes = new Set();
  return {
    classList: { add: c => classes.add(c), remove: c => classes.delete(c), contains: c => classes.has(c),
      toggle: (c, on) => (on ? classes.add(c) : classes.delete(c)) },
    style: { setProperty() {} }, setAttribute() {}, insertAdjacentHTML() {}, appendChild() {},
    addEventListener() {}, focus() {}, querySelector: () => el(), innerHTML: '', textContent: '',
  };
}

function load() {
  const els = {}, timers = [], pings = [];
  const ctx = {
    document: {
      documentElement: el(), body: el(), activeElement: null,
      getElementById: id => (els[id] ??= el()), createElement: () => el(), querySelectorAll: () => [],
    },
    setTimeout: (fn, ms) => timers.push({ fn, ms }), clearTimeout() {}, addEventListener() {}, innerWidth: 1000, innerHeight: 800,
    matchMedia: () => ({ matches: false }), performance, AbortController,
    fetch: () => new Promise(resolve => pings.push(resolve)),
  };
  ctx.window = ctx;
  vm.runInNewContext(script, ctx);
  const fire = ms => timers.splice(0).forEach(t => (t.ms === ms ? t.fn() : timers.push(t)));
  return { ctx, els, fire, pings, get: expr => vm.runInContext(expr, ctx) };
}

const flush = () => new Promise(r => setImmediate(r));

test('a ping answering after the 9s sweep does not un-finish the roll call', async () => {
  const page = load();
  page.fire(9000);  // the sweep marks every unanswered app silent
  assert.ok(page.els.roll.classList.contains('done'));
  page.pings[0]();  // one fetch resolves late
  await flush();
  assert.ok(page.els.roll.classList.contains('done'), 'banner stuck on "Franking..."');
  assert.equal(page.get('answered + silent'), page.get('ALL.length'));
});
