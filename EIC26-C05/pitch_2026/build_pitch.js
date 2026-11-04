// AirTransformer EIC Accelerator 2026 interview pitch. Numbers locked to Part B (4 Nov 2026),
// Implementation Plan A17-R2 / GateSync, and Financial Information A18-R5.
const path = require('path');
const pptxgen = require('pptxgenjs');
const SK = process.env.SK;
const { applyTheme } = require(path.join(SK, 'scripts/apply_theme.js'));

const ROOT = path.resolve(__dirname, '..');
const A = (f) => path.join(ROOT, 'assets', f);
const B = (f) => path.join(ROOT, 'assets2', f);
const OUT = process.argv[2] || path.join(ROOT, 'out', 'AirTransformer_EIC2026_Pitch.pptx');

const THEME = {
  name: 'Savery AirTransformer',
  headFontFace: 'Calibri',
  bodyFontFace: 'Calibri',
  colors: {
    dk1: '26313B', lt1: 'FFFFFF', dk2: '1F3A5F', lt2: 'E3F1F2',
    accent1: '2A8C93', accent2: 'D9643A', accent3: '1F3A5F', accent4: '9CC9CC',
    accent5: '6B7785', accent6: 'E8B04B', hlink: '2A8C93', folHlink: '6B7785',
  },
};
// hex copies for hex-only options (charts, gridlines)
const HX = { navy: '1F3A5F', teal: '2A8C93', lteal: 'E3F1F2', orange: 'D9643A', text: '26313B', grey: '6B7785', soft: '9CC9CC', gold: 'E8B04B', grid: 'DDE3E8' };

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
pres.author = 'Savery Tech';
pres.company = 'Savery Tech';
pres.title = 'AirTransformer: EIC Accelerator 2026 pitch';
pres.subject = 'EIC Accelerator 2026, Challenge C05';
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;
const NAVY = C.text2, TEXT = C.text1, WHITE = C.background1, LIGHT = C.background2;
const TEAL = C.accent1, ORANGE = C.accent2, SOFT = C.accent4, GREY = C.accent5, GOLD = C.accent6;
const FONT_CH = '+mn-lt';

// ---------- layouts ----------
pres.defineSlideMaster({
  title: 'AT_CONTENT',
  background: { color: 'FFFFFF' },
  margin: [0.5, 0.6, 0.7, 0.6],
  objects: [
    { image: { x: 11.53, y: 0.47, w: 1.2, h: 0.306, path: A('logo.png'), altText: 'Savery logo' } },
    { text: { text: 'AirTransformer · Savery Tech · EIC Accelerator 2026', options: { x: 0.6, y: 7.02, w: 7, h: 0.3, fontSize: 10, color: GREY, margin: 0 } } },
    { placeholder: { options: { name: 'title', type: 'title', x: 0.6, y: 0.35, w: 10.7, h: 0.75, fontSize: 28, bold: true, color: NAVY, valign: 'middle', align: 'left', margin: 0 }, text: '' } },
    { placeholder: { options: { name: 'lead', type: 'body', x: 0.6, y: 1.1, w: 12.13, h: 0.45, fontSize: 16, color: GREY, valign: 'top', margin: 0 }, text: '' } },
  ],
  slideNumber: { x: 12.23, y: 7.02, w: 0.5, h: 0.3, fontSize: 10, color: '6B7785', align: 'right' },
});
pres.defineSlideMaster({
  title: 'AT_COVER',
  background: { color: HX.navy },
  objects: [
    { placeholder: { options: { name: 'title', type: 'title', x: 0.6, y: 1.65, w: 6.3, h: 0.95, fontSize: 54, bold: true, color: WHITE, valign: 'middle', align: 'left', margin: 0 }, text: '' } },
  ],
});
pres.defineSlideMaster({
  title: 'AT_CLOSE',
  background: { color: HX.navy },
  objects: [
    { placeholder: { options: { name: 'title', type: 'title', x: 0.6, y: 0.55, w: 10.5, h: 0.9, fontSize: 36, bold: true, color: WHITE, valign: 'middle', align: 'left', margin: 0 }, text: '' } },
  ],
  slideNumber: { x: 12.23, y: 7.02, w: 0.5, h: 0.3, fontSize: 10, color: '9CC9CC', align: 'right' },
});

// ---------- helpers ----------
const T = (slide, text, o) => slide.addText(text, Object.assign({ isTextBox: true, margin: 0, color: TEXT, fontSize: 14, valign: 'top' }, o));
const card = (slide, x, y, w, h, fill = LIGHT, line) => slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: fill }, line: line ? { color: line, width: 1 } : { type: 'none' } });
const disc = (slide, x, y, d, label, fill = TEAL, size = 16) => {
  slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { type: 'none' } });
  T(slide, String(label), { x, y, w: d, h: d, align: 'center', valign: 'middle', bold: true, color: WHITE, fontSize: size });
};
const content = (title, lead, section) => {
  const s = pres.addSlide({ masterName: 'AT_CONTENT', sectionTitle: section });
  s.addText(title, { placeholder: 'title' });
  if (lead) s.addText(lead, { placeholder: 'lead' });
  return s;
};
const chartBase = () => ({
  catAxisLabelColor: HX.grey, valAxisLabelColor: HX.grey, catAxisLabelFontSize: 12, valAxisLabelFontSize: 11,
  catAxisLabelFontFace: FONT_CH, valAxisLabelFontFace: FONT_CH, dataLabelFontFace: FONT_CH, titleFontFace: FONT_CH, legendFontFace: FONT_CH,
  valGridLine: { color: HX.grid, size: 0.5 }, catGridLine: { style: 'none' },
  catAxisLineShow: true, valAxisLineShow: false,
  showTitle: true, titleFontSize: 14, titleColor: HX.text, titleBold: true,
});
const lerp = (a, b, t) => Math.round(a + (b - a) * t);
const mix = (h1, h2, t) => {
  const p = (h) => [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16));
  const [a, b] = [p(h1), p(h2)];
  return a.map((v, i) => lerp(v, b[i], t).toString(16).padStart(2, '0')).join('').toUpperCase();
};

// ===================== 1. COVER =====================
pres.addSection({ title: 'Opening' });
{
  const s = pres.addSlide({ masterName: 'AT_COVER', sectionTitle: 'Opening' });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 0.55, w: 2.0, h: 0.62, rectRadius: 0.08, fill: { color: WHITE }, line: { type: 'none' } });
  s.addImage({ path: A('logo.png'), x: 0.75, y: 0.645, w: 1.7, h: 0.434, altText: 'Savery logo' });
  s.addText('AirTransformer', { placeholder: 'title' });
  T(s, 'Heat-driven cooling for climate-resilient data centres', { x: 0.6, y: 2.7, w: 6.0, h: 1.0, fontSize: 26, color: SOFT });
  T(s, 'EIC Accelerator 2026 · Challenge C05', { x: 0.6, y: 3.75, w: 6.2, h: 0.32, fontSize: 16, bold: true, color: WHITE });
  T(s, 'Deep Tech for Climate Adaptation', { x: 0.6, y: 4.07, w: 6.2, h: 0.32, fontSize: 16, color: WHITE });
  T(s, 'Savery Tech, France · Frédéric Cui, founder and CEO', { x: 0.6, y: 4.5, w: 6.2, h: 0.32, fontSize: 16, color: SOFT });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.95, y: 1.6, w: 5.8, h: 2.95, rectRadius: 0.1, fill: { color: WHITE }, line: { type: 'none' } });
  s.addImage({ path: B('hero.png'), x: 7.05, y: 1.78, w: 5.6, h: 2.593, altText: 'Concept of AirTransformer installed beside a liquid-cooled data hall' });
  const tiles = [
    ['COP 20', 'measured with 60 °C waste heat, 2025 EN test'],
    ['TRL6 → TRL8', 'qualified pre-series product by March 2029'],
    ['€4.49m EIC', '€2.49m grant + €2m equity in an €8m Seed'],
  ];
  tiles.forEach(([big, small], i) => {
    const x = 0.6 + i * 4.135;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 5.15, w: 3.87, h: 1.5, rectRadius: 0.08, fill: { color: TEAL }, line: { type: 'none' } });
    T(s, big, { x: x + 0.25, y: 5.3, w: 3.4, h: 0.6, fontSize: 30, bold: true, color: WHITE, valign: 'middle' });
    T(s, small, { x: x + 0.25, y: 5.92, w: 3.4, h: 0.6, fontSize: 14, color: WHITE });
  });
  s.addNotes('Good morning. I am Frédéric Cui, founder and CEO of Savery Tech. AirTransformer turns the low-temperature heat that data centres already reject into cooling, without a compressor. Our complete machine is at TRL6 and measured an electrical COP of 20 with 60-degree waste heat. With the EIC, we will qualify it as a manufacturable TRL8 product by March 2029.');
}

// ===================== 2. PROBLEM =====================
{
  const s = content('Heatwaves push cooling into grid and water limits', 'Electricity and water demand peak exactly when both are scarcest, while low-grade heat goes unused.', 'Opening');
  s.addImage({ path: B('problem.png'), x: 0.6, y: 1.8, w: 4.94, h: 4.75, altText: 'Data hall overheating while rooftop chillers run at full load' });
  const cards = [
    ['EER ≈ 3', 'In a heatwave, compression cooling draws 333 kW of electricity per MW of cooling, at the hours of peak grid stress.', ORANGE],
    ['Power-limited', 'Q1 2026 inventory grew 33% in the four largest North American markets and 18.9% in Europe; power availability now limits where sites go (CBRE, June 2026).', NAVY],
    ['Water', 'Evaporative cooling needs make-up water that competes with cities when drought restrictions apply.', TEAL],
    ['PUE ≤ 1.2', 'Germany’s EnEfG requires data centres entering service from July 2026 to reach it within two years.', NAVY],
  ];
  cards.forEach(([big, body, col], i) => {
    const x = 5.85 + (i % 2) * 3.54, y = 1.8 + Math.floor(i / 2) * 2.27;
    card(s, x, y, 3.34, 2.1);
    T(s, big, { x: x + 0.22, y: y + 0.18, w: 2.9, h: 0.5, fontSize: 24, bold: true, color: col, valign: 'middle' });
    T(s, body, { x: x + 0.22, y: y + 0.75, w: 2.92, h: 1.3, fontSize: 14 });
  });
  T(s, 'Meanwhile, liquid-cooled racks reject 40–70 °C heat that nobody uses.', { x: 5.85, y: 6.42, w: 6.88, h: 0.4, fontSize: 16, bold: true, color: ORANGE, valign: 'middle' });
  s.addNotes('Cooling is where climate stress hits digital infrastructure. In a heatwave, compression cooling falls to an EER of about 3: a third of a megawatt of electricity for every megawatt of cooling, at the hours when the grid is tightest. Power availability already limits where data centres can be built, evaporative systems draw water just when drought restrictions apply, and Germany now requires new sites to reach a PUE of 1.2. Meanwhile, liquid-cooled racks reject 40 to 70-degree heat that nobody uses.');
}

// ===================== 3. SOLUTION =====================
pres.addSection({ title: 'Technology' });
{
  const s = content('Rack heat in, cooling out: no vapour compression', 'Waste heat dries the air in staged MOF contactors; a cooling heat exchanger delivers the cooling.', 'Technology');
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 1.8, w: 7.6, h: 4.15, fill: { color: WHITE }, line: { color: HX.grid, width: 1 } });
  s.addImage({ path: A('schematic.png'), x: 0.65, y: 1.85, w: 7.5, h: 3.985, altText: 'AirTransformer functional schematic: waste heat regenerates staged MOF contactors; dry air passes a cooling heat exchanger cooled by a separate wet working-air stream' });
  T(s, 'Regenerates at 50–70 °C with water recovery and 40–50 °C without. Installs beside existing cooling; the site keeps its isolation, fallback and supervision.', { x: 0.6, y: 6.08, w: 7.6, h: 0.75, fontSize: 13, color: GREY });
  const stats = [
    ['COP 20', 'machine electrical COP with 60 °C waste heat (2025 EN test); 8–20 installed', TEAL],
    ['−60–70%', 'electricity at equal cooling: action qualification target', TEAL],
    ['−40–60%', 'external make-up water at equal cooling', TEAL],
    ['20 → 600 kW', '20 kW thermal module, 600 kW container configuration', NAVY],
  ];
  stats.forEach(([big, lab, col], i) => {
    const y = 1.8 + i * 1.27;
    T(s, big, { x: 8.6, y, w: 4.13, h: 0.55, fontSize: 30, bold: true, color: col, valign: 'middle' });
    T(s, lab, { x: 8.6, y: y + 0.56, w: 4.13, h: 0.55, fontSize: 13, color: TEXT });
    if (i < 3) s.addShape(pres.shapes.LINE, { x: 8.6, y: y + 1.17, w: 4.13, h: 0, line: { color: SOFT, width: 1 } });
  });
  s.addNotes('AirTransformer uses that heat. Staged MOF contactors dry the process air, and waste heat regenerates them. The dry air then passes a cooling heat exchanger, where water evaporates into a separate working-air stream without mixing. There is no vapour compression: electricity only drives fans, pumps and controls. The machine reached COP 20 in our 2025 EN test, and 8 to 20 installed. The product is a 20-kilowatt module, assembled into 600-kilowatt containers beside the existing cooling.');
}

// ===================== 4. DEEP TECH =====================
{
  const s = content('Material, cycle and machine engineered as one', 'Molecular sorption becomes sustained cooling only when contactor, heat exchange and timing are co-designed.', 'Technology');
  s.addImage({ path: A('iso3.png'), x: 0.6, y: 1.8, w: 4.35, h: 4.277, altText: 'Water-uptake isotherms of tandem MOFs with steep steps placed at the operating boundaries' });
  T(s, 'Tandem MOF isotherms: uptake steps placed at the machine’s operating boundaries.', { x: 0.6, y: 6.15, w: 4.35, h: 0.6, fontSize: 12, color: GREY });
  const rows = [
    ['Material', 'Aluminium-based CAU-family MOFs (Kiel University) take up and release water in steep, low-temperature steps; each stage uses a different window as the air dries.'],
    ['Contactor', 'Coated fins and fluid-carrying tubes remove adsorption heat as it forms. This staged arrangement is protected by the 2025 family FR2508386.'],
    ['Cycle', 'Finite-time design sets switching, regeneration and heat recovery for useful cooling per cycle, building on Henninger et al., co-authored by F. Cui.'],
    ['Control', 'Model-predictive supervision inside independent safety limits and deterministic fallback; operators keep override.'],
  ];
  rows.forEach(([h, b], i) => {
    const y = 1.85 + i * 1.24;
    disc(s, 5.35, y + 0.05, 0.55, i + 1);
    T(s, h, { x: 6.1, y, w: 6.6, h: 0.38, fontSize: 18, bold: true, color: NAVY, valign: 'middle' });
    T(s, b, { x: 6.1, y: y + 0.4, w: 6.6, h: 0.75, fontSize: 14 });
  });
  s.addNotes('The breakthrough is not one material; it is matching material, contactor, cycle and control. Our aluminium-based CAU MOFs from Kiel University switch their water uptake in steep, low-temperature steps, and each stage uses a different step as the air dries. Coated fins and fluid tubes remove adsorption heat as it forms: that is our 2025 patent family. Finite-time design, from my published work with Henninger, sets switching and regeneration, and a model-predictive controller runs inside hard safety limits.');
}

// ===================== 5. PROOF =====================
{
  const s = content('Ten years of prototypes, one complete TRL6 machine', '2025 EN test: sensible-cooling electrical COP 20 with 60 °C waste heat.', 'Technology');
  const items = [
    ['poc1.jpg', 'PoC 1 · 2017'], ['proto1.jpg', '1 kW prototype · 2019'], ['poc2.jpg', 'PoC 2 · 2021'], ['poc3.jpg', 'PoC 3 · 2022'],
    ['proto2.jpg', '15 kW prototype · 2023'], ['proto3.jpg', '25 kW prototype · 2024'],
  ];
  const w = 1.6, g = 0.155, h = 1.85;
  items.forEach(([f, lab], i) => {
    const x = 0.6 + i * (w + g);
    s.addImage({ path: B(f), x, y: 1.75, w, h, altText: lab });
    T(s, lab, { x, y: 3.64, w, h: 0.3, fontSize: 12, color: GREY, align: 'center' });
  });
  const x7 = 0.6 + 6 * (w + g);
  s.addShape(pres.shapes.RECTANGLE, { x: x7, y: 1.75, w, h, fill: { color: NAVY }, line: { type: 'none' } });
  T(s, 'COP 20', { x: x7, y: 2.2, w, h: 0.55, fontSize: 26, bold: true, color: WHITE, align: 'center', valign: 'middle' });
  T(s, 'complete machine, EN test, 60 °C heat', { x: x7 + 0.12, y: 2.8, w: w - 0.24, h: 0.65, fontSize: 12, color: WHITE, align: 'center' });
  T(s, 'TRL6 machine · 2025', { x: x7, y: 3.64, w, h: 0.3, fontSize: 12, bold: true, color: NAVY, align: 'center' });
  s.addShape(pres.shapes.LINE, { x: 0.6, y: 4.08, w: 12.13, h: 0, line: { color: SOFT, width: 1 } });

  // native heat map table
  T(s, 'Machine COP map at 60 °C source: ambient temperature × relative humidity', { x: 0.6, y: 4.22, w: 6.4, h: 0.32, fontSize: 13, bold: true, color: NAVY });
  const amb = ['20 °C', '25 °C', '30 °C', '35 °C', '40 °C'];
  const map = { 'RH 30%': [18, 16, 16, 16, 14], 'RH 40%': [18, 18, 17, 16, 16], 'RH 50%': [18, 17, 16, 16, 15], 'RH 60%': [19, 19, 18, 17, 17], 'RH 70%': [18, 18, 16, 16, 16] };
  const hdr = [{ text: '', options: { fill: { color: WHITE } } }].concat(amb.map((a) => ({ text: a, options: { bold: true, color: NAVY, align: 'center', fill: { color: WHITE } } })));
  const rows = [hdr];
  Object.entries(map).forEach(([rh, vals]) => {
    rows.push([{ text: rh, options: { bold: true, color: NAVY, fill: { color: WHITE } } }].concat(vals.map((v) => {
      const t = (v - 14) / 5;
      return { text: String(v), options: { align: 'center', bold: true, color: v >= 17 ? 'FFFFFF' : HX.text, fill: { color: mix(HX.lteal, HX.teal, t) } } };
    })));
  });
  s.addTable(rows, { x: 0.6, y: 4.6, w: 6.4, colW: [1.4, 1.0, 1.0, 1.0, 1.0, 1.0], rowH: 0.35, fontSize: 13, valign: 'middle', border: { type: 'solid', pt: 1, color: 'FFFFFF' }, margin: 0.03 });

  const pts = [
    ['14–19', 'COP across 20–40 °C ambient and 30–70% RH: performance holds in the heat'],
    ['Fans, pumps, controls', 'are the only electrical inputs; no compressor in the cooling cycle'],
    ['8–20 installed', 'Site comparisons include the circulating pump and every affected auxiliary, which the EN test boundary excluded'],
  ];
  pts.forEach(([b, t], i) => {
    const y = 4.25 + i * 0.86;
    s.addShape(pres.shapes.RECTANGLE, { x: 7.4, y: y + 0.05, w: 0.08, h: 0.68, fill: { color: TEAL }, line: { type: 'none' } });
    T(s, [{ text: b + '  ', options: { bold: true, color: NAVY } }, { text: t }], { x: 7.65, y, w: 5.08, h: 0.8, fontSize: 14, valign: 'middle' });
  });
  s.addNotes('Ten years of iteration: three proofs of concept and three prototypes, from 1 kilowatt in 2019 to 25 kilowatts in 2024, led to a complete TRL6 machine. In the 2025 EN test it delivered sensible cooling at an electrical COP of 20 with 60-degree heat. Across 20 to 40 degrees ambient and 30 to 70 percent humidity, COP stays between 14 and 19: performance holds in the heat. Site comparisons include every pump and auxiliary, so we quote 8 to 20 installed.');
}

// ===================== 6. WHAT CHANGED =====================
{
  const s = content('What changed since the 2025 evaluation', 'Each change answers a point raised by the 2025 evaluators.', 'Technology');
  const cols = [
    ['chg1.png', 'Intellectual property', 'All three patent families filed by Savery Tech: FR2508386 with its PCT extension, EP26301484.7 (October 2026) and EP3825627A1. Product-specific FTO maps BASF, NuMat, Framergy, AirJoule and Kiel/Fraunhofer process rights.'],
    ['chg2.png', 'Funding and research', '€400k raised through BSA-AIR. CETP 2026–2029 research programme awarded, with HPE Labs contributing data-centre integration expertise.'],
    ['chg3.png', 'Team and governance', 'Two engineers and an interim CFO in post. Board with two Corps des Mines engineers and a data-centre executive; scientific board with Kiel University and CNRS IRCELYON. Target: ≥40% women among all new hires by March 2029.'],
    ['chg4.png', 'Product focus', 'One platform for urban liquid-cooled data centres in Europe and North America. Complete TRL6 machine, COP 20 measured in 2025. Four reference units planned with two prospective customers in 2027.'],
  ];
  cols.forEach(([img, h, b], i) => {
    const x = 0.6 + i * 3.087;
    card(s, x, 1.75, 2.88, 5.1);
    s.addImage({ path: B(img), x: x + 0.69, y: 1.88, w: 1.5, h: 1.5, altText: h });
    T(s, h, { x: x + 0.2, y: 3.5, w: 2.48, h: 0.4, fontSize: 18, bold: true, color: NAVY, valign: 'middle' });
    T(s, b, { x: x + 0.2, y: 3.95, w: 2.48, h: 2.8, fontSize: 14 });
  });
  s.addNotes('Since 2025, we have answered both points the evaluators raised. On IP, every family is now filed by Savery Tech, and our freedom-to-operate work names the rights we map. On the team, two engineers and an interim CFO have joined, both boards are in place, and we target at least 40 percent women among all new hires. We raised 400 thousand euros through BSA-AIR, won the CETP programme with HPE Labs, and focused on one product and one beachhead.');
}

// ===================== 7. IP & FTO =====================
{
  const s = content('Savery owns its IP; FTO follows the CAU route', 'Patents protect the staged exchanger and system architecture; know-how protects the process.', 'Technology');
  const H = (t) => ({ text: t, options: { bold: true, color: 'FFFFFF', fill: { color: HX.navy } } });
  const rows = [
    [H('Family (applicant Savery Tech)'), H('Filing'), H('What it protects')],
    [{ text: 'Heat-and-mass exchanger, 2025', options: { bold: true, color: HX.navy } }, 'FR2508386, 21 July 2025; PCT filed 20 July 2026', 'Staged MOFs with decreasing water-adsorption thresholds, coated fins and integrated heat-transfer tubes: the core of the product'],
    [{ text: 'Sorption heat pump, 2026', options: { bold: true, color: HX.navy } }, 'EP26301484.7, 9 October 2026', 'Routable vapour circulation with compression assist: the heating extension (COP 6–10)'],
    [{ text: 'System family, 2019', options: { bold: true, color: HX.navy } }, 'EP3825627A1, pending', 'Earlier system architecture'],
  ];
  s.addTable(rows, { x: 0.6, y: 1.8, w: 7.3, colW: [2.1, 2.2, 3.0], fontSize: 13, color: HX.text, valign: 'middle', border: { type: 'solid', pt: 0.75, color: HX.grid }, fill: { color: 'FFFFFF' }, margin: [0.06, 0.08, 0.06, 0.08], rowH: [0.42, 1.0, 0.85, 0.5] });
  card(s, 0.6, 4.95, 7.3, 1.85);
  T(s, 'Know-how kept in-house', { x: 0.85, y: 5.08, w: 6.8, h: 0.38, fontSize: 18, bold: true, color: NAVY, valign: 'middle' });
  T(s, 'Coating windows, tolerances, calibration, release tests and control parameters stay trade secrets. Supplier agreements define permitted use, improvements and continuing access for production and replacement supply.', { x: 0.85, y: 5.5, w: 6.85, h: 1.2, fontSize: 14 });

  T(s, 'Product-specific freedom to operate', { x: 8.3, y: 1.8, w: 4.43, h: 0.4, fontSize: 18, bold: true, color: NAVY, valign: 'middle' });
  const steps = [
    'Screening leads mapped: BASF, NuMat, Framergy, Montana/AirJoule; Kiel/Fraunhofer MOF-process patents EP3350151B1 and US10696704B2.',
    'Specialist review compares the selected CAU synthesis or supply route with each claim, by jurisdiction.',
    'Disposition (supply or licence, design change, or territory) recorded at the M12 gate, before manufacturing transfer and each release.',
    'PCT extension and follow-on filings track the European and North American manufacturing and sales plan.',
  ];
  steps.forEach((t, i) => {
    const y = 2.35 + i * 1.12;
    disc(s, 8.3, y + 0.05, 0.45, i + 1, TEAL, 14);
    T(s, t, { x: 8.9, y, w: 3.83, h: 1.05, fontSize: 14 });
  });
  s.addNotes('Savery owns three patent families. The 2025 family protects staged MOFs with decreasing adsorption thresholds and integrated heat exchange, the core of the product, with a PCT extension filed in July. The 2026 European application covers a sorption heat pump with routable vapour circulation, our heating extension. Freedom to operate follows the exact CAU route we manufacture: we have mapped BASF, NuMat, Framergy, AirJoule and the Kiel-Fraunhofer process patents, and each disposition is recorded at the M12 gate, before manufacturing transfer. Process know-how stays in-house.');
}

// ===================== 8. MARKET =====================
pres.addSection({ title: 'Market and impact' });
{
  const s = content('A €15bn market, entered through liquid-cooled sites', 'Beachhead: urban liquid-cooled data centres with 50–70 °C rack heat, in Europe and North America.', 'Market and impact');
  s.addImage({ path: B('beachhead.png'), x: 0.6, y: 1.95, w: 4.3, h: 3.963, altText: 'Data-centre campus as the beachhead, with industrial sites as later applications' });
  const tiles = [
    ['€15bn', 'data-centre cooling opportunity, company planning estimate', NAVY, WHITE],
    ['USD 20.5bn', 'worldwide data-centre cooling, 2025 (Global Market Insights)', TEAL, WHITE],
    ['€75m → €181m', 'Savery revenue 2031 → 2032: 0.5% → 1.2% of the €15bn reference', ORANGE, WHITE],
  ];
  tiles.forEach(([b, t, f, c], i) => {
    const y = 1.85 + i * 1.65;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 5.25, y, w: 3.75, h: 1.5, rectRadius: 0.08, fill: { color: f }, line: { type: 'none' } });
    T(s, b, { x: 5.45, y: y + 0.15, w: 3.35, h: 0.55, fontSize: 28, bold: true, color: c, valign: 'middle' });
    T(s, t, { x: 5.45, y: y + 0.75, w: 3.35, h: 0.65, fontSize: 13, color: c });
  });
  T(s, 'Entry sequence', { x: 9.35, y: 1.85, w: 3.38, h: 0.4, fontSize: 18, bold: true, color: NAVY, valign: 'middle' });
  const seq = [
    ['2027', 'Four reference units with two prospective customers'],
    ['2028–2032', 'Liquid-cooled data centres in Europe and North America: 1,498 units in 2032'],
    ['Next', 'Industrial 40–50 °C waste heat and urban critical facilities, via the 600 kW container'],
  ];
  seq.forEach(([k, t], i) => {
    const y = 2.4 + i * 1.47;
    s.addShape(pres.shapes.RECTANGLE, { x: 9.35, y, w: 0.08, h: 1.25, fill: { color: i === 2 ? GREY : TEAL }, line: { type: 'none' } });
    T(s, k, { x: 9.6, y, w: 3.1, h: 0.35, fontSize: 16, bold: true, color: i === 2 ? GREY : TEAL });
    T(s, t, { x: 9.6, y: y + 0.38, w: 3.13, h: 0.9, fontSize: 14 });
  });
  s.addNotes('We plan against a 15-billion-euro data-centre cooling opportunity; independent analysts put the global market at 20.5 billion dollars. We start where heat, grid limits and liquid cooling meet: urban liquid-cooled data centres in Europe and North America, with 50 to 70-degree rack heat. Four reference units with two prospective customers come in 2027. By 2032 we plan 1,498 units and 181 million euros of revenue, about 1.2 percent of our planning reference. Industrial 40 to 50-degree waste heat follows.');
}

// ===================== 9. DIFFERENTIATION =====================
{
  const s = content('Cooling from waste heat, without compressor or vacuum', 'Compared at equal useful cooling, including all auxiliaries.', 'Market and impact');
  const H = (t, al = 'left') => ({ text: t, options: { bold: true, color: 'FFFFFF', fill: { color: HX.navy }, align: al } });
  const at = (t) => ({ text: t, options: { color: HX.text, fill: { color: HX.lteal } } });
  const alt = (t) => ({ text: t, options: { bold: true, color: HX.navy } });
  const rows = [
    [H('Alternative'), H('Limit for the operator'), H('AirTransformer')],
    [alt('Compression cooling with free cooling'), 'Free-cooling hours fall in a heatwave; compressor input peaks at EER ≈ 3 (333 kW per MW)', at('Waste heat replaces compressor work: 50–125 kW per MW at installed COP 8–20')],
    [alt('Desiccant systems with mechanical post-cooling'), 'Drying still needs a vapour-compression stage to deliver the cooling', at('Staged adsorption cooling delivers the duty without vapour compression')],
    [alt('Closed-cycle adsorption chillers (silica gel, zeolite)'), 'Vacuum vessels make chilled water that still needs air handling', at('Open-cycle contactors treat the air directly at atmospheric pressure')],
    [alt('Atmospheric water harvesting or dehumidification (e.g. AirJoule)'), 'Built to produce water or dry air, not to carry a facility cooling duty', at('Built around the cooling duty; water recovery is an operating mode')],
  ];
  s.addTable(rows, { x: 0.6, y: 1.8, w: 12.13, colW: [3.4, 4.2, 4.53], fontSize: 14, color: HX.text, valign: 'middle', border: { type: 'solid', pt: 0.75, color: HX.grid }, margin: [0.08, 0.12, 0.08, 0.12], rowH: [0.45, 0.95, 0.85, 0.85, 0.95] });
  disc(s, 0.6, 6.12, 0.5, '§', ORANGE, 16);
  T(s, 'The staged MOF exchanger with integrated heat removal is the subject of Savery’s 2025 family FR2508386 and its PCT extension.', { x: 1.25, y: 6.1, w: 11.4, h: 0.55, fontSize: 14, color: NAVY, valign: 'middle' });
  s.addNotes('Customers compare us with four alternatives. Compression with free cooling loses its free hours in a heatwave. Desiccant systems still need mechanical post-cooling. Closed-cycle adsorption chillers use vacuum vessels and make chilled water that still needs air handling. Water-harvesting and dehumidification systems such as AirJoule are built for water or drying. AirTransformer treats the air directly at atmospheric pressure and delivers the cooling duty without vapour compression, with water recovery as a mode. That staged architecture is what our 2025 family protects.');
}

// ===================== 10. VALUE PER MW =====================
{
  const s = content('Per MW: 208–283 kW of grid headroom in a heatwave', 'Engineering comparison against compression at EER 3, at 8,000 effective hours per year.', 'Market and impact');
  const labels = ['Compression\nEER 3', 'AirTransformer\nCOP 8', 'AirTransformer\nCOP 10', 'AirTransformer\nCOP 20'];
  s.addChart(pres.charts.BAR, [
    { name: 'Compression', labels, values: [333.3, 0, 0, 0] },
    { name: 'AirTransformer', labels, values: [0, 125, 100, 50] },
  ], Object.assign(chartBase(), {
    x: 0.6, y: 1.75, w: 6.3, h: 4.75, barDir: 'col', barGrouping: 'stacked', barGapWidthPct: 55,
    chartColors: [HX.orange, HX.teal], showLegend: false,
    title: 'Electrical input for 1 MW of cooling (kW)',
    showValue: true, dataLabelPosition: 'inEnd', dataLabelColor: 'FFFFFF', dataLabelFontSize: 14, dataLabelFontBold: true, dataLabelFormatCode: '0;;;',
    valAxisMaxVal: 350, valAxisMinVal: 0, valAxisMajorUnit: 50, valAxisLabelFormatCode: '0', catAxisLabelFontSize: 11,
  }));
  const tiles = [
    ['208–283 kW', 'grid capacity released per MW of cooling', TEAL],
    ['1.7–2.3 GWh', 'electricity saved per MW each year', TEAL],
    ['4,800–7,200 m³', 'external water saved per MW each year', TEAL],
    ['25–35 months', 'customer payback at €0.25/kWh; 35–48% cash ROI a year', ORANGE],
  ];
  tiles.forEach(([b, t, col], i) => {
    const x = 7.25 + (i % 2) * 2.79, y = 1.8 + Math.floor(i / 2) * 2.05;
    card(s, x, y, 2.69, 1.88);
    T(s, b, { x: x + 0.18, y: y + 0.2, w: 2.4, h: 0.6, fontSize: 24, bold: true, color: col, valign: 'middle' });
    T(s, t, { x: x + 0.18, y: y + 0.85, w: 2.38, h: 0.95, fontSize: 14 });
  });
  s.addShape(pres.shapes.RECTANGLE, { x: 7.25, y: 5.98, w: 0.08, h: 0.82, fill: { color: NAVY }, line: { type: 'none' } });
  T(s, [{ text: 'C05 outcome: ', options: { bold: true, color: NAVY } }, { text: 'urban cooling that keeps its duty in extreme heat with less electricity and water, verified by matched-service tests at M24.' }], { x: 7.5, y: 5.98, w: 5.23, h: 0.82, fontSize: 14, valign: 'middle' });
  s.addNotes('Per megawatt of cooling, compression at EER 3 draws 333 kilowatts; AirTransformer draws 50 to 125. That frees 208 to 283 kilowatts of grid capacity at the hottest hours, and saves 1.7 to 2.3 gigawatt-hours and 4,800 to 7,200 cubic metres of water a year. For the customer, at 25 cents per kilowatt-hour, a 120-thousand-euro unit per 100 kilowatts pays back in 25 to 35 months. This is the C05 outcome: urban cooling that keeps running in extreme heat with less electricity and water.');
}

// ===================== 11. BUSINESS MODEL =====================
{
  const s = content('Sold on acceptance, grown by replication', '€120k per unit: €110k equipment, €8k installation, €2k engineering; then maintenance at 3% a year.', 'Market and impact');
  s.addChart(pres.charts.BAR, [{ name: 'Accepted units', labels: ['2027', '2028', '2029', '2030', '2031', '2032'], values: [4, 13, 71, 222, 624, 1498] }], Object.assign(chartBase(), {
    x: 0.6, y: 1.75, w: 5.5, h: 4.75, barDir: 'col', barGapWidthPct: 50, chartColors: [HX.teal], showLegend: false,
    title: 'Accepted units per year (company forecast)',
    showValue: true, dataLabelPosition: 'outEnd', dataLabelColor: HX.text, dataLabelFontSize: 12, dataLabelFormatCode: '#,##0',
    valAxisHidden: true, valGridLine: { style: 'none' }, valAxisMaxVal: 1700,
  }));
  const boxes = [
    ['Revenue model', 'Billing 20% on order, 20% on completion, 55% on acceptance, 5% after six months. Maintenance from month 12: 60% attachment, 90% renewal.'],
    ['Acquisition and replication', 'Pods of one account executive and one application engineer: eight qualified accounts a year, half convert after a 12-month validation. Each acceptance leads to more units on site, then further sites and regions.'],
    ['Channel ecosystem', 'Design offices, installers, distributors, maintainers, integrators and site operators (e.g. Cap Ingelec, Rexel, Dalkia, HLRS, Cineca). Discovery so far: 60 conversations, 20 in-depth.'],
  ];
  boxes.forEach(([h, b], i) => {
    const y = 1.8 + i * 1.7;
    card(s, 6.45, y, 6.28, 1.58);
    T(s, h, { x: 6.67, y: y + 0.12, w: 5.9, h: 0.36, fontSize: 16, bold: true, color: NAVY, valign: 'middle' });
    T(s, b, { x: 6.67, y: y + 0.5, w: 5.88, h: 1.02, fontSize: 14 });
  });
  s.addNotes('We sell equipment, installation and engineering at 120 thousand euros per unit, then maintenance at 3 percent of equipment value per year. Billing is tied to acceptance, so delivery quality drives cash. Each acquisition pod pairs an account executive with an application engineer, and an acceptance at one site leads to more units there, then further sites and regions. Our channel ecosystem covers design offices, installers, distributors, maintainers and operators. Units grow from 4 in 2027 to 1,498 in 2032, paced by factory and field capacity.');
}

// ===================== 12. EIC ACTION =====================
pres.addSection({ title: 'Execution' });
{
  const s = content('TRL6 machine to qualified TRL8 product in 24 months', 'April 2027 – March 2029 · 258 person-months · €3.55m eligible cost · seven evidence gates', 'Execution');
  const X0 = 3.55, X1 = 12.73, M = 36, mw = (X1 - X0) / M;
  const mx = (m) => X0 + (m - 1) * mw; // start of month m
  // axis
  [1, 6, 12, 18, 24, 30, 36].forEach((m) => {
    T(s, 'M' + m, { x: mx(m) - 0.3 + mw / 2, y: 1.72, w: 0.6, h: 0.28, fontSize: 11, color: GREY, align: 'center' });
  });
  s.addShape(pres.shapes.RECTANGLE, { x: X0, y: 2.02, w: mx(25) - X0, h: 0.06, fill: { color: TEAL }, line: { type: 'none' } });
  s.addShape(pres.shapes.RECTANGLE, { x: mx(25), y: 2.02, w: X1 - mx(25), h: 0.06, fill: { color: GOLD }, line: { type: 'none' } });
  const wps = [
    ['WP1 Requirements and engineering baseline', 1, 6, '€0.28m', TEAL],
    ['WP2 Manufacturing transfer and batch qualification', 1, 18, '€0.91m', TEAL],
    ['WP3 Reliability, controls and conformity', 3, 21, '€1.21m', TEAL],
    ['WP4 Product qualification and deployment', 6, 24, '€1.01m', TEAL],
    ['WP5 Management, data, IP and exploitation', 1, 24, '€0.14m', SOFT],
    ['WP6 Manufacturing deployment and service (EIC investment)', 12, 36, '€2.11m', GOLD],
  ];
  wps.forEach(([lab, a, b, cost, col], i) => {
    const y = 2.22 + i * 0.47;
    T(s, lab, { x: 0.6, y, w: 2.85, h: 0.4, fontSize: 11, color: TEXT, valign: 'middle' });
    s.addShape(pres.shapes.RECTANGLE, { x: X0, y: y + 0.04, w: X1 - X0, h: 0.32, fill: { color: 'F4F6F8' }, line: { type: 'none' } });
    s.addShape(pres.shapes.RECTANGLE, { x: mx(a), y: y + 0.04, w: (b - a + 1) * mw, h: 0.32, fill: { color: col }, line: { type: 'none' } });
    T(s, cost, { x: mx(a) + 0.08, y: y + 0.04, w: 1.0, h: 0.32, fontSize: 11, bold: true, color: col === GOLD || col === SOFT ? TEXT : WHITE, valign: 'middle' });
  });
  const gates = [[6, 'M6'], [12, 'M12'], [18, 'M18'], [21, 'M21'], [24, 'M24'], [26, 'M26'], [36, 'M36']];
  gates.forEach(([m]) => {
    s.addShape(pres.shapes.LINE, { x: mx(m) + mw, y: 2.2, w: 0, h: 2.85, line: { color: NAVY, width: 0.75, dashType: 'dash' } });
    s.addShape(pres.shapes.DIAMOND, { x: mx(m) + mw - 0.09, y: 5.0, w: 0.18, h: 0.18, fill: { color: m <= 24 ? NAVY : GOLD }, line: { type: 'none' } });
  });
  T(s, 'TRL6', { x: X0 - 0.02, y: 5.0, w: 0.6, h: 0.22, fontSize: 11, bold: true, color: TEAL });
  const tiles = [
    ['M6', 'Specification, verification protocol and test plan approved'],
    ['M12', 'Drawings and process window released; rights disposition recorded'],
    ['M18', 'Six batches, 12 contactors qualified; 1,200 independent fixture-hours'],
    ['M21', '4,000 endurance hours; conformity file and software released'],
    ['M24 · TRL8', '1,600 field hours; ≥60% less electricity, ≥40% less water verified'],
    ['M26', 'Serial tooling and manufacturing partner qualified'],
    ['M36', 'Five installation and service packages delivered'],
  ];
  const tw = (12.13 - 6 * 0.1) / 7;
  tiles.forEach(([h, b], i) => {
    const x = 0.6 + i * (tw + 0.1);
    const inv = i >= 5;
    card(s, x, 5.35, tw, 1.5, i === 4 ? NAVY : LIGHT);
    T(s, h, { x: x + 0.1, y: 5.42, w: tw - 0.2, h: 0.3, fontSize: 14, bold: true, color: i === 4 ? WHITE : inv ? ORANGE : NAVY });
    T(s, b, { x: x + 0.1, y: 5.74, w: tw - 0.2, h: 1.08, fontSize: 12, color: i === 4 ? WHITE : TEXT });
  });
  s.addNotes('The EIC action runs from April 2027 to March 2029: 258 person-months across five work packages. It closes the gap between a working machine and a product: controlled manufacture, reliability, conformity and field acceptance. Every gate has a number. By M18, six qualified batches and 1,200 independent fixture-hours; by M21, 4,000 endurance hours and conformity release; at M24, 1,600 field hours and verified savings of at least 60 percent electricity and 40 percent water, our TRL8 decision. The investment work package then readies serial production.');
}

// ===================== 13. TEAM =====================
{
  const s = content('The team to build, qualify and sell the product', 'Core team full-time, two engineers in post, eleven roles planned against work-package needs.', 'Execution');
  const core = [
    ['p_frederic.jpg', 'Frédéric Cui', 'Founder and CEO, technology and product', 'Sorption and thermal modelling, prototype validation, industrial transfer; TU Eindhoven, ARMINES'],
    ['p_qin.jpg', 'Qin Yu', 'Engineering and production lead', 'HVAC installation, supplier qualification, commissioning, QHSE'],
    ['p_ina.jpg', 'Ina Wang', 'Commercial lead', '15+ years B2B: pricing, enterprise accounts, cross-border sales'],
    ['p_nicolas.jpg', 'Nicolas Paris', 'Interim CFO (30%)', 'Financial planning, energy markets, investment funds'],
  ];
  core.forEach(([img, n, r, d], i) => {
    const x = 0.6 + i * 3.08;
    s.addImage({ path: B(img), x, y: 1.8, w: 1.1, h: 1.1, rounding: true, altText: n });
    T(s, n, { x: x + 1.22, y: 1.8, w: 1.78, h: 0.32, fontSize: 16, bold: true, color: NAVY });
    T(s, r, { x: x + 1.22, y: 2.13, w: 1.78, h: 0.75, fontSize: 12, color: TEAL, bold: true });
    T(s, d, { x, y: 3.0, w: 2.9, h: 0.75, fontSize: 12, color: TEXT });
  });
  const panel = (x, title, people) => {
    card(s, x, 3.95, 5.96, 2.9);
    T(s, title, { x: x + 0.22, y: 4.05, w: 5.5, h: 0.36, fontSize: 16, bold: true, color: NAVY, valign: 'middle' });
    people.forEach(([img, n, d], i) => {
      const y = 4.5 + i * 0.77;
      if (img) s.addImage({ path: B(img), x: x + 0.22, y, w: 0.62, h: 0.62, rounding: true, altText: n });
      else disc(s, x + 0.22, y, 0.62, n.split(' ').filter((w) => /^[A-Z]/.test(w) && !/^(Dr|Prof)/.test(w)).map((w) => w[0]).join(''), TEAL, 14);
      T(s, [{ text: n, options: { bold: true, color: NAVY, breakLine: true } }, { text: d, options: { color: TEXT } }], { x: x + 1.0, y: y - 0.02, w: 4.8, h: 0.68, fontSize: 12, valign: 'middle' });
    });
  };
  panel(0.6, 'Company board', [
    ['p_christian.jpg', 'Christian Houzé', 'Engineer of the Corps des Mines; international scientific and industrial experience'],
    ['p_francois.jpg', 'François Giger', 'Engineer of the Corps des Mines; international scientific and industrial experience'],
    ['p_olivier.jpg', 'Olivier Labbé', 'Data-centre design, construction and commercialisation'],
  ]);
  panel(6.77, 'Scientific board', [
    [null, 'Prof. Norbert Stock', 'Kiel University, Institute of Inorganic Chemistry: CAU materials'],
    [null, 'Dr Aline Auroux', 'Emeritus CNRS Research Director, IRCELYON: adsorption calorimetry'],
    ['p_driss.jpg', 'Driss Stitou', 'Solid–gas sorption and thermal-energy conversion'],
  ]);
  s.addNotes('I lead architecture and product, from a background in sorption, thermal modelling and industrial transfer. Qin leads engineering and production; Ina leads sales with 15 years of B2B experience; Nicolas is our interim CFO. Two engineers are in post, and eleven planned roles map to work-package needs. Our board brings two Corps des Mines engineers and a data-centre executive; our scientific board brings Professor Stock, whose Kiel group created the CAU materials, Dr Auroux and Driss Stitou.');
}

// ===================== 14. FINANCIALS =====================
{
  const s = content('€75m revenue in 2031 as factory capacity scales', 'Company forecast, nominal €m. The EIC grant co-finances costs already in the business plan.', 'Execution');
  const yrs = ['2027', '2028', '2029', '2030', '2031'];
  s.addChart(pres.charts.BAR, [
    { name: 'Revenue', labels: yrs, values: [0.48, 1.56, 8.54, 26.72, 75.24] },
    { name: 'EBITDA', labels: yrs, values: [-1.37, -6.62, -8.06, -14.03, -7.64] },
  ], Object.assign(chartBase(), {
    x: 0.6, y: 1.75, w: 6.9, h: 5.0, barDir: 'col', barGrouping: 'clustered', barGapWidthPct: 60,
    chartColors: [HX.teal, HX.orange], title: 'Revenue and EBITDA (€m)',
    showLegend: true, legendPos: 'b', legendFontSize: 12, legendColor: HX.text,
    showValue: true, dataLabelPosition: 'outEnd', dataLabelColor: HX.text, dataLabelFontSize: 11, dataLabelFormatCode: '0.0',
    valAxisMinVal: -20, valAxisMaxVal: 80, valAxisMajorUnit: 20, valAxisLabelFormatCode: '0',
  }));
  T(s, 'Funding path', { x: 7.85, y: 1.8, w: 4.88, h: 0.38, fontSize: 18, bold: true, color: NAVY, valign: 'middle' });
  const H = (t, al = 'left') => ({ text: t, options: { bold: true, color: 'FFFFFF', fill: { color: HX.navy }, align: al } });
  const R = (t) => ({ text: t, options: { align: 'right', bold: true, color: HX.navy } });
  s.addTable([
    [H('Round'), H('Timing'), H('Amount', 'right')],
    ['Seed, incl. €2m EIC', 'Sep–Nov 2027', R('€8m')],
    ['Series A: pilot factory', 'April 2028', R('€25m')],
    ['Series B: replication', 'January 2030', R('€70m')],
    ['Series C: regional capacity', 'January 2032', R('€35m')],
  ], { x: 7.85, y: 2.25, w: 4.88, colW: [2.28, 1.6, 1.0], fontSize: 13, color: HX.text, valign: 'middle', rowH: 0.38, border: { type: 'solid', pt: 0.75, color: HX.grid }, margin: [0.04, 0.08, 0.04, 0.08] });
  const st = [
    ['€95m', 'cash needed to reach operating break-even; Seed, A and B raise €101m net by 2030'],
    ['€181m', '2032 revenue, 1,498 accepted units'],
    ['> 0', 'cash balance in every month of the plan'],
  ];
  st.forEach(([b, t], i) => {
    const y = 4.35 + i * 0.83;
    T(s, b, { x: 7.85, y, w: 1.35, h: 0.7, fontSize: 24, bold: true, color: i === 0 ? ORANGE : TEAL, valign: 'middle' });
    T(s, t, { x: 9.25, y, w: 3.48, h: 0.7, fontSize: 13, valign: 'middle' });
  });
  s.addNotes('Revenue grows from 0.5 million euros in 2027 to 75 million in 2031 and 181 million in 2032. EBITDA stays negative while we build factory and field capacity. We need about 95 million euros to reach operating break-even, and the Seed, Series A and Series B raise 101 million net. Cash stays positive in every month. The EIC grant co-finances costs that are already in our business plan; it adds no new spending.');
}

// ===================== 15. THE ASK =====================
pres.addSection({ title: 'Ask' });
{
  const s = content('The ask: €4.49m to qualify the product and scale', '€2.49m grant (70% of €3.55m) + €2m EIC investment anchoring an €8m Seed, closing November 2027.', 'Ask');
  s.addChart(pres.charts.DOUGHNUT, [{
    name: 'Eligible cost', labels: ['WP1 Baseline', 'WP2 Manufacturing', 'WP3 Reliability and conformity', 'WP4 Qualification', 'WP5 Management and IP'],
    values: [0.28, 0.91, 1.21, 1.01, 0.14],
  }], Object.assign(chartBase(), {
    x: 0.6, y: 1.75, w: 5.6, h: 5.0, holeSize: 55, chartColors: [HX.soft, HX.teal, HX.navy, HX.orange, HX.gold],
    title: 'Grant action: €3.55m eligible cost by work package (€m)',
    showLegend: true, legendPos: 'b', legendFontSize: 12, legendColor: HX.text,
    showValue: true, showPercent: false, showLabel: false, dataLabelColor: 'FFFFFF', dataLabelFontSize: 12, dataLabelFontBold: true, dataLabelFormatCode: '0.00',
  }));
  const rows = [
    ['€2.49m', 'EIC grant', '70% of the €3.55m productisation action: manufacture, reliability, conformity and field qualification to TRL8', TEAL],
    ['€2.0m', 'EIC investment', '€1.9m to manufacturing deployment and service (tooling, partner, application engineering, first packages); €0.1m to action co-financing', NAVY],
    ['€6.0m', 'Other Seed investors', 'Launch September 2027, close November 2027; co-finances the action and the company’s wider growth plan', GREY],
  ];
  rows.forEach(([b, h, t, col], i) => {
    const y = 1.8 + i * 1.18;
    T(s, b, { x: 6.55, y, w: 1.6, h: 0.5, fontSize: 26, bold: true, color: col, valign: 'middle' });
    T(s, h, { x: 8.25, y, w: 4.48, h: 0.35, fontSize: 16, bold: true, color: NAVY, valign: 'middle' });
    T(s, t, { x: 8.25, y: y + 0.37, w: 4.48, h: 0.75, fontSize: 13 });
  });
  card(s, 6.55, 5.4, 6.18, 1.45, NAVY);
  T(s, [{ text: 'Why the EIC: ', options: { bold: true, color: SOFT } }, { text: 'qualification risk sits before revenue. Blended finance retires it, and EIC equity signals that to the industrial investors of the Seed and Series A.', options: { color: WHITE } }], { x: 6.8, y: 5.5, w: 5.75, h: 1.25, fontSize: 14, valign: 'middle' });
  s.addNotes('We ask the EIC for 4.49 million euros: a 2.49-million grant, 70 percent of the 3.55-million action, and 2 million in equity. The equity anchors an 8-million Seed with 6 million from other investors, launching in September 2027 and closing in November. Of the EIC investment, 1.9 million goes to manufacturing deployment and service capacity and 100 thousand co-finances the action. The EIC is the right partner because qualification risk comes before revenue, and EIC participation signals to investors that this risk is being retired.');
}

// ===================== 16. CLOSE =====================
{
  const s = pres.addSlide({ masterName: 'AT_CLOSE', sectionTitle: 'Ask' });
  s.addText('Waste heat in, resilient cooling out', { placeholder: 'title' });
  const cols = [
    ['Why now', 'Heatwaves, grid limits and PUE rules are hitting data centres now, and liquid cooling has made 50–70 °C rack heat available at scale.'],
    ['Why us', 'Ten years from proof of concept to a complete TRL6 machine at COP 20; Savery-owned IP; a team covering science, engineering and sales.'],
    ['Why the EIC', '€4.49m of blended finance turns the machine into a qualified TRL8 European product and anchors the €8m Seed.'],
  ];
  cols.forEach(([h, b], i) => {
    const x = 0.6 + i * 4.135;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.95, w: 3.87, h: 3.3, rectRadius: 0.08, fill: { color: WHITE, transparency: 90 }, line: { color: SOFT, width: 1 } });
    T(s, h, { x: x + 0.28, y: 2.15, w: 3.3, h: 0.5, fontSize: 22, bold: true, color: SOFT, valign: 'middle' });
    T(s, b, { x: x + 0.28, y: 2.8, w: 3.3, h: 2.3, fontSize: 16, color: WHITE });
  });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 5.75, w: 2.0, h: 0.62, rectRadius: 0.08, fill: { color: WHITE }, line: { type: 'none' } });
  s.addImage({ path: A('logo.png'), x: 0.75, y: 5.845, w: 1.7, h: 0.434, altText: 'Savery logo' });
  T(s, 'Frédéric Cui · founder and CEO, Savery Tech · AirTransformer', { x: 2.9, y: 5.75, w: 8.5, h: 0.62, fontSize: 16, color: WHITE, valign: 'middle' });
  s.addNotes('To close: heatwaves, grid limits and efficiency rules are hitting data centres now, and liquid cooling has made their waste heat usable. We have the machine, the IP and the team. With the EIC, we turn a COP-20 machine into a qualified European product that keeps urban digital infrastructure cool in extreme heat. Thank you.');
}

// ===================== B1. RATING & ECONOMICS =====================
pres.addSection({ title: 'Backup' });
{
  const s = content('Backup: rating basis and customer economics', 'For questions on the COP figures and the payback range.', 'Backup');
  card(s, 0.6, 1.8, 5.2, 4.0);
  T(s, 'Rating basis', { x: 0.82, y: 1.92, w: 4.8, h: 0.38, fontSize: 18, bold: true, color: NAVY, valign: 'middle' });
  T(s, [
    { text: 'Machine COP 20: delivered sensible cooling ÷ electrical input, 60 °C waste heat, 2025 EN test.', options: { bullet: true, breakLine: true, paraSpaceAfter: 6 } },
    { text: 'The EN heat loops ran at static pressure, so the circulating pump was outside the test input.', options: { bullet: true, breakLine: true, paraSpaceAfter: 6 } },
    { text: 'Installed COP 8–20: site pumps, fans, controls and water treatment included.', options: { bullet: true, breakLine: true, paraSpaceAfter: 6 } },
    { text: 'Regeneration heat and electrical COP are reported separately at every rating point.', options: { bullet: true, breakLine: true, paraSpaceAfter: 6 } },
    { text: 'ΔP = Q × (1/EER ref − 1/COP installed)', options: { bold: true, color: NAVY } },
  ], { x: 0.82, y: 2.4, w: 4.8, h: 3.3, fontSize: 14 });
  const H = (t, al = 'left') => ({ text: t, options: { bold: true, color: 'FFFFFF', fill: { color: HX.navy }, align: al } });
  const r = (t) => ({ text: t, options: { align: 'right' } });
  s.addTable([
    [H('Scenario per 100 kW of cooling'), H('Net saving / yr', 'right'), H('Payback', 'right'), H('Cash ROI / yr', 'right')],
    ['€120k installed, €0.25/kWh (main)', r('€42–58k'), r('25–35 months'), r('35–48%')],
    ['€120k installed, €0.20/kWh', r('€33–46k'), r('31–43 months'), r('28–39%')],
    ['€100k installed, €0.20/kWh (future cost)', r('€33–46k'), r('26–36 months'), r('33–46%')],
  ], { x: 6.15, y: 1.8, w: 6.58, colW: [2.7, 1.3, 1.4, 1.18], fontSize: 13, color: HX.text, valign: 'middle', rowH: [0.5, 0.55, 0.55, 0.55], border: { type: 'solid', pt: 0.75, color: HX.grid }, margin: [0.04, 0.08, 0.04, 0.08] });
  T(s, 'Assumptions: 100 kW useful cooling; 8,000 effective hours a year of displaced compression; reference EER 3; installed COP 8–20; waste heat at zero marginal cost; baseline external water 1.5 L/kWh of cooling at €4/m³ with a 40–60% make-up reduction (€1,920–2,880 a year); incremental service €2,000 a year.', { x: 6.15, y: 4.25, w: 6.58, h: 1.4, fontSize: 13, color: GREY });
  T(s, 'Electrical headroom and cooling continuity add value beyond the cash saving.', { x: 6.15, y: 5.85, w: 6.58, h: 0.5, fontSize: 14, bold: true, color: TEAL });
  s.addNotes('Backup for questions on how COP 20 relates to installed performance and on customer payback.');
}

// ===================== B2. RISKS =====================
{
  const s = content('Backup: delivery risks and responses', 'Each risk has an owner and a review point in the Implementation Plan.', 'Backup');
  const H = (t) => ({ text: t, options: { bold: true, color: 'FFFFFF', fill: { color: HX.navy } } });
  const k = (t) => ({ text: t, options: { bold: true, color: HX.navy } });
  s.addTable([
    [H('Risk'), H('Response and owner'), H('Review point')],
    [k('Recruitment delays on the 213 planned-role PM'), 'Frédéric and Qin prioritise M1 posts, assign deputies, rephase dependencies; scoped specialist services', 'Before M1, then monthly'],
    [k('CAU processing reduces output, consistency or life'), 'Batch traceability, after-shaping tests, ageing and contamination checks, quarantined lots', 'Batch releases; M12 and M18'],
    [k('A rating point does not transfer to a site'), 'Verify source, sink and auxiliaries; revise the released operating domain; repeat the matched-service test', 'M6 and each campaign'],
    [k('Conformity or third-party rights need a design change'), 'Quality lead and Frédéric obtain the assessment, record the design change or rights, close findings', 'Before each release'],
    [k('Financing or grant payments arrive late'), 'Phase hiring, procurement and deployment against available funds', 'Monthly cash review'],
    [k('Orders or acceptances arrive later than planned'), 'Ina leads account qualification, reference-site evidence and staged offers', 'Quarterly pipeline review'],
  ], { x: 0.6, y: 1.8, w: 12.13, colW: [3.9, 5.83, 2.4], fontSize: 13, color: HX.text, valign: 'middle', rowH: [0.42, 0.72, 0.72, 0.72, 0.72, 0.6, 0.6], border: { type: 'solid', pt: 0.75, color: HX.grid }, margin: [0.05, 0.1, 0.05, 0.1] });
  s.addNotes('Backup for risk questions; the full register is in Part B section 3.3 and the Implementation Plan.');
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log('wrote', OUT);
})();
