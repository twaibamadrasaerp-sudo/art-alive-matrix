import json

with open('programmes_clean.json', 'r', encoding='utf-8') as f:
    programmes = json.load(f)

# Ensure each programme has all needed fields and normalize aliases
for i, p in enumerate(programmes):
    p['id'] = p.get('id', f'prog-{i}')
    aliases = set(p.get('aliases', []))
    aliases.add(p['name'])
    if p.get('nameEn'):
        aliases.add(p['nameEn'])
        aliases.add(p['nameEn'].lower())
    p['aliases'] = list(aliases)

programmes_js = "const programmes = " + json.dumps(programmes, ensure_ascii=False, indent=2) + ";\n"

script_tail = '''
const sectionInfo = {
  ai: { ml: 'എഐ & പ്രോംപ്റ്റിങ്', en: 'AI & Prompting', aliases: ['ai', 'എഐ', 'എ ഐ', 'prompting', 'പ്രോംപ്റ്റിങ്', 'പ്രോംപ്റ്റിംഗ്'] },
  tech: { ml: 'ടെക് ക്രിയേറ്റീവ്', en: 'Tech Creative', aliases: ['tech', 'technology', 'ടെക്', 'ടെക്നിക്കൽ', 'creative'] },
  presentation: { ml: 'പ്രസന്റേഷൻ', en: 'Presentation', aliases: ['presentation', 'പ്രസന്റേഷൻ', 'speech', 'talk', 'പ്രസംഗം'] },
  vocal: { ml: 'വോക്കൽ', en: 'Vocal', aliases: ['vocal', 'വോക്കൽ', 'song', 'പാട്ട്', 'ഗാനം'] },
  writings: { ml: 'റൈറ്റിങ്സ്', en: 'Writings', aliases: ['writing', 'writings', 'റൈറ്റിംഗ്', 'രചന', 'essay', 'poem', 'story'] },
  iq: { ml: 'ഐക്യു സ്കിൽ', en: 'IQ Skill', aliases: ['iq', 'quiz', 'ഐക്യു', 'ടെസ്റ്റ്', 'ക്വിസ്'] },
  makthaba: { ml: 'മക്തബ', en: 'Makthaba', aliases: ['makthaba', 'makthab', 'മക്തബ'] },
  general: { ml: 'പൊതു നിർദേശങ്ങൾ', en: 'General Guide', aliases: ['general rules', 'general guide', 'rules', 'നിയമങ്ങൾ', 'പൊതുനിയമങ്ങൾ', 'നിർദേശങ്ങൾ'] }
};

const els = {
  landing: document.querySelector('#landing'),
  chat: document.querySelector('#chatScreen'),
  start: document.querySelector('#startChat'),
  home: document.querySelector('#goHome'),
  conversation: document.querySelector('#conversation'),
  form: document.querySelector('#composer'),
  prompt: document.querySelector('#prompt'),
  send: document.querySelector('.send-button'),
  clear: document.querySelector('#clearChat'),
  installButtons: document.querySelectorAll('.install-button, #installChat'),
  installDialog: document.querySelector('#installDialog'),
  closeInstall: document.querySelector('#closeInstall'),
  installInstructions: document.querySelector('#installInstructions'),
  language: document.querySelector('#languageToggle'),
  theme: document.querySelector('#themeToggle'),
  status: document.querySelector('#statusLine em'),
  suggestions: document.querySelector('#suggestions'),
  promptLabel: document.querySelector('#promptLabel'),
  privacy: document.querySelector('#privacyNote'),
  landingTitle: document.querySelector('#landing-title'),
  landingIntro: document.querySelector('#landingIntro'),
  landingOverline: document.querySelector('#landingOverline'),
  orbInstruction: document.querySelector('#orbInstruction'),
  installLanding: document.querySelector('#installLanding'),
  openNameModal: document.querySelector('#openNameModal'),
  namePillAvatar: document.querySelector('#namePillAvatar'),
  namePillText: document.querySelector('#namePillText'),
  nameDialog: document.querySelector('#nameDialog'),
  closeNameDialog: document.querySelector('#closeNameDialog'),
  nameForm: document.querySelector('#nameForm'),
  userNameInput: document.querySelector('#userNameInput'),
  skipNameBtn: document.querySelector('#skipNameBtn'),
  devTriggers: document.querySelectorAll('.dev-trigger'),
  devDialog: document.querySelector('#devDialog'),
  closeDevDialog: document.querySelector('#closeDevDialog'),
  dismissDevDialog: document.querySelector('#dismissDevDialog')
};

let deferredInstall = null;
let isReplying = false;
let language = localStorage.getItem('matrix-language') || 'en';
let theme = localStorage.getItem('matrix-theme') || 'dark';
let userName = localStorage.getItem('matrix-user-name') || '';
let pendingChatAfterName = false;

const copy = {
  ml: {
    title: 'Your<br />programme. Your<br /><span>rules.</span>',
    intro: 'Send a programme, section, or level. Find MATRIX 26 rules and details instantly.',
    orb: 'Tap to begin',
    install: 'Install',
    status: 'റൂൾബുക്ക് കണക്റ്റഡ്',
    prompt: 'പരിപാടി, വിഭാഗം, അല്ലെങ്കിൽ ലെവൽ നൽകുക',
    privacy: 'വിവരങ്ങളിൽ തെറ്റുകൾ സംഭവിച്ചേക്കാം; സ്ഥിരീകരണത്തിന് ഒഫീഷ്യൽ സർക്കുലർ പരിശോധിക്കുക.',
    welcome: 'നമസ്കാരം. പരിപാടിയുടെ പേര്, <strong>ക്യാപ്ഷൻ സോങ്</strong>, <strong>AI</strong>, <strong>വോക്കൽ</strong>, അല്ലെങ്കിൽ <strong>സീനിയർ</strong> എന്ന് അയക്കൂ. ഞാന്‍ ഔദ്യോഗിക നിയമങ്ങൾ നൽകാം.',
    example: 'ഉദാഹരണം:',
    you: 'നിങ്ങൾ',
    searching: 'തിരയുന്നു',
    ready: 'തയ്യാർ',
    results: 'കണ്ടെത്തിയ പരിപാടികൾ',
    choose: 'നിയമങ്ങൾ കാണാൻ ഒരു ഇനം തിരഞ്ഞെടുക്കൂ.',
    noResults: 'പരിപാടി കണ്ടെത്താനായില്ല',
    noResultsText: query => `“${query}” എന്നതുമായി പൊരുത്തപ്പെടുന്ന ഇനം കണ്ടെത്താനായില്ല. പേര്, വിഭാഗം, അല്ലെങ്കിൽ ലെവൽ വീണ്ടും ശ്രമിക്കൂ.`,
    source: 'നിയമാവലി',
    page: 'പേജ്',
    level: 'ലെവൽ'
  },
  en: {
    title: 'Your<br />programme. Your<br /><span>rules.</span>',
    intro: 'Send a programme, section, or level. Find MATRIX 26 rules and details instantly.',
    orb: 'Tap to begin',
    install: 'Install',
    status: 'RULEBOOK CONNECTED',
    prompt: 'Search programme, section, or level',
    privacy: 'Responses may contain errors. Cross-verify with the official circular PDF for confirmation.',
    welcome: 'Hello. Send a programme name, <strong>Caption Song</strong>, <strong>AI</strong>, <strong>Vocal</strong>, or <strong>Senior</strong>. I will provide the official rules.',
    example: 'Try:',
    you: 'YOU',
    searching: 'SEARCHING',
    ready: 'READY',
    results: 'Matching programmes',
    choose: 'Select an event to view its full rules.',
    noResults: 'No programme found',
    noResultsText: query => `No event matched “${query}”. Try a programme name, section, or level.`,
    source: 'RULEBOOK',
    page: 'PAGE',
    level: 'LEVEL'
  }
};

function escapeHtml(text) {
  return String(text).replace(/[&<>'"]/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#039;', '"': '&quot;' }[char]));
}

function normalise(value) {
  return String(value)
    .toLocaleLowerCase('ml-IN')
    .normalize('NFD')
    .replace(/[^\\p{L}\\p{M}\\p{N}]/gu, '');
}

function tokenise(value) {
  return String(value)
    .toLocaleLowerCase('ml-IN')
    .split(/[^\\p{L}\\p{M}\\p{N}]+/gu)
    .map(normalise)
    .filter(token => token.length > 1);
}

function editSimilarity(first, second) {
  if (!first || !second) return 0;
  if (first === second) return 1;
  const a = Array.from(first);
  const b = Array.from(second);
  const previous = Array.from({ length: b.length + 1 }, (_, index) => index);
  for (let row = 1; row <= a.length; row += 1) {
    let diagonal = previous[0];
    previous[0] = row;
    for (let column = 1; column <= b.length; column += 1) {
      const saved = previous[column];
      previous[column] = Math.min(
        previous[column] + 1,
        previous[column - 1] + 1,
        diagonal + (a[row - 1] === b[column - 1] ? 0 : 1)
      );
      diagonal = saved;
    }
  }
  return 1 - (previous[b.length] / Math.max(a.length, b.length));
}

function rankProgrammes(query) {
  const input = normalise(query);
  const inputTokens = tokenise(query);
  return programmes.map(programme => {
    let score = 0;
    const candidates = [programme.name, programme.nameEn, ...(programme.aliases || [])].filter(Boolean);
    candidates.forEach(alias => {
      const candidate = normalise(alias);
      const candidateTokens = tokenise(alias);
      let nextScore = 0;
      if (input === candidate) nextScore = 100;
      else if (input.includes(candidate) || candidate.includes(input)) nextScore = 82 + Math.min(14, Math.min(candidate.length, input.length));
      else {
        const fullMatch = editSimilarity(input, candidate);
        const bestTokenMatch = inputTokens.reduce((highest, inputToken) => Math.max(
          highest,
          ...candidateTokens.map(candidateToken => editSimilarity(inputToken, candidateToken))
        ), 0);
        const matchedTokens = inputTokens.filter(inputToken => candidateTokens.some(candidateToken => editSimilarity(inputToken, candidateToken) >= .8)).length;
        nextScore = Math.max(fullMatch * 76, bestTokenMatch * 58 + matchedTokens * 10);
      }
      score = Math.max(score, nextScore);
    });
    return { programme, score };
  }).filter(match => match.score >= 57).sort((first, second) => second.score - first.score);
}

function findCollection(query) {
  const input = normalise(query);
  const tokens = tokenise(query).map(normalise);
  const levelMap = { junior: ['junior', 'ജൂനിയർ'], senior: ['senior', 'സീനിയർ'], general: ['general', 'ജനറൽ'] };
  const languageMap = { ml: ['malayalam', 'മലയാളം'], en: ['english', 'ഇംഗ്ലീഷ്'], ar: ['arabic', 'അറബിക്'] };
  const selectedLevels = Object.entries(levelMap).filter(([, aliases]) => aliases.some(alias => input === normalise(alias) || tokens.includes(normalise(alias)))).map(([level]) => level);
  const selectedLanguages = Object.entries(languageMap).filter(([, aliases]) => aliases.some(alias => input === normalise(alias) || tokens.includes(normalise(alias)))).map(([lang]) => lang);
  const selectedSection = Object.entries(sectionInfo).find(([, section]) => section.aliases.some(alias => input === normalise(alias) || tokens.includes(normalise(alias))));
  if (!selectedLevels.length && !selectedLanguages.length && !selectedSection) return null;

  let matches = programmes.filter(programme => {
    const sectionMatch = !selectedSection || programme.section === selectedSection[0] || (selectedSection[0] === 'tech' && programme.section === 'ai');
    const levelMatch = !selectedLevels.length || selectedLevels.some(level => programme.levels.includes(level));
    const languageMatch = !selectedLanguages.length || selectedLanguages.some(lang => (programme.languages || []).includes(lang));
    return sectionMatch && levelMatch && languageMatch;
  });
  if (!matches.length) return null;
  const titleParts = [
    selectedSection ? (language === 'en' ? selectedSection[1].en : selectedSection[1].ml) : '',
    ...selectedLevels.map(level => language === 'en' ? level[0].toUpperCase() + level.slice(1) : ({ junior: 'ജൂനിയർ', senior: 'സീനിയർ', general: 'ജനറൽ' }[level])),
    ...selectedLanguages.map(lang => language === 'en' ? ({ ml: 'Malayalam', en: 'English', ar: 'Arabic' }[lang]) : ({ ml: 'മലയാളം', en: 'ഇംഗ്ലീഷ്', ar: 'അറബിക്' }[lang]))
  ].filter(Boolean);
  return { type: 'collection', title: titleParts.join(' · '), matches };
}

function resolveQuery(query) {
  const matches = rankProgrammes(query);
  if (matches[0]?.score === 100) return { type: 'record', record: matches[0].programme };
  const collection = findCollection(query);
  if (collection) return collection;
  if (!matches.length) return { type: 'record', record: noMatch(query), fallback: true };
  if (matches.length === 1 || (matches[0].score >= 96 && matches[0].score - (matches[1]?.score || 0) > 9)) return { type: 'record', record: matches[0].programme };
  return { type: 'collection', title: copy[language].results, matches: matches.slice(0, 9).map(match => match.programme) };
}

function displayName(programme) {
  return language === 'en' ? (programme.nameEn || programme.name) : programme.name;
}

function displaySection(programme) {
  const section = sectionInfo[programme.section];
  return section ? (language === 'en' ? section.en : section.ml) : programme.categoryMl;
}

function displayLevels(programme) {
  if (!programme.levels?.length) return '';
  return programme.levels.map(level => language === 'en' ? level[0].toUpperCase() + level.slice(1) : ({ junior: 'ജൂനിയർ', senior: 'സീനിയർ', general: 'ജനറൽ' }[level])).join(', ');
}

function scrollToLatest() {
  els.conversation.scrollTo({ top: els.conversation.scrollHeight, behavior: 'smooth' });
}

function updateUserGreeting() {
  userName = localStorage.getItem('matrix-user-name') || '';
  if (userName) {
    els.landingTitle.innerHTML = `Hi, ${escapeHtml(userName)}!<br />Welcome to <span>MATRIX.</span>`;
    if (els.namePillText) els.namePillText.textContent = userName;
    if (els.namePillAvatar) els.namePillAvatar.textContent = userName.charAt(0).toUpperCase();
  } else {
    els.landingTitle.innerHTML = `Hi, Welcome to<br /><span>MATRIX.</span>`;
    if (els.namePillText) els.namePillText.textContent = 'Set your name';
    if (els.namePillAvatar) els.namePillAvatar.textContent = 'M';
  }
}

function updateInterface() {
  const words = copy[language];
  document.documentElement.lang = language;
  updateUserGreeting();
  els.landingIntro.textContent = 'Send a programme, section, or level. Find MATRIX 26 rules and details instantly.';
  els.orbInstruction.textContent = 'Tap to begin';
  els.installLanding.textContent = 'Install';
  els.status.textContent = words.status;
  els.prompt.placeholder = words.prompt;
  els.prompt.setAttribute('aria-label', words.prompt);
  els.promptLabel.textContent = words.prompt;
  if (els.privacy) els.privacy.textContent = words.privacy;
  els.language.classList.toggle('is-english', language === 'en');
  els.language.setAttribute('aria-label', language === 'en' ? 'Switch to Malayalam' : 'Switch to English');
  els.language.title = language === 'en' ? 'മലയാളം' : 'English';
  const prompts = language === 'en' ? ['Caption Song', 'AI', 'Vocal', 'Senior'] : ['ക്യാപ്ഷൻ സോങ്', 'AI', 'വോക്കൽ', 'സീനിയർ'];
  els.suggestions.querySelectorAll('button').forEach((button, index) => {
    button.dataset.prompt = prompts[index];
    button.textContent = prompts[index];
  });
}

function setTheme(nextTheme) {
  theme = nextTheme;
  document.body.dataset.theme = theme;
  localStorage.setItem('matrix-theme', theme);
  document.querySelector('meta[name="theme-color"]').setAttribute('content', theme === 'light' ? '#f4f0ea' : '#080808');
  els.theme.setAttribute('aria-label', theme === 'light' ? 'Use dark theme' : 'Use light theme');
}

function setLanguage(nextLanguage) {
  language = nextLanguage;
  localStorage.setItem('matrix-language', language);
  updateInterface();
  if (!isReplying) resetChat();
}

function appendWelcome() {
  const userGreeting = userName ? escapeHtml(userName) : '';
  const heading = userGreeting ? `Hi, <span>${userGreeting}</span>!` : 'Hi, <span>Welcome to MATRIX</span>';
  const subtext = 'Select a category to explore competitions &amp; rules:';

  const cards = [
    {
      id: 'senior',
      name: 'Senior',
      prompt: 'Senior',
      count: '25 Events',
      desc: 'International Dars, Thanqeeh, Khutbah, Debate &amp; Senior items'
    },
    {
      id: 'junior',
      name: 'Junior',
      prompt: 'Junior',
      count: '25 Events',
      desc: 'Face to Face, Commentary, Live Reporting, Socio Synopsis &amp; Junior items'
    },
    {
      id: 'general',
      name: 'General',
      prompt: 'General',
      count: '43 Events',
      desc: "Va'azh, Voice X, CTF, DPR, Qawwali, Mashup &amp; Open items"
    }
  ];

  const cardsHtml = cards.map(c => `
    <button class="hub-card hub-card-${c.id}" type="button" data-prompt="${c.prompt}">
      <div class="hub-card-top">
        <div class="hub-card-title-group">
          <span class="hub-dot-indicator dot-${c.id}"></span>
          <h3 class="hub-card-name">${c.name}</h3>
        </div>
        <div class="hub-card-badge-wrap">
          <span class="hub-count-tag">${c.count}</span>
          <span class="hub-arrow-icon" aria-hidden="true">
            <svg viewBox="0 0 16 16" width="13" height="13" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 11L11 5M11 5H6M11 5V10"/>
            </svg>
          </span>
        </div>
      </div>
      <p class="hub-card-desc">${c.desc}</p>
    </button>
  `).join('');

  const node = document.createElement('div');
  node.className = 'welcome-hub';
  node.innerHTML = `
    <div class="hub-intro">
      <div class="hub-badge">
        <span class="hub-dot"></span>
        <span class="hub-badge-text">FESTIVAL INTELLIGENCE</span>
      </div>
      <h2 class="hub-heading">${heading}</h2>
      <p class="hub-subtext">${subtext}</p>
    </div>
    <div class="hub-cards-grid">
      ${cardsHtml}
    </div>
  `;
  els.conversation.append(node);
  bindPromptButtons();
  scrollToLatest();
}

function bindPromptButtons() {
  document.querySelectorAll('[data-prompt]').forEach(button => {
    if (button.dataset.bound) return;
    button.dataset.bound = 'true';
    button.addEventListener('click', () => ask(button.dataset.prompt));
  });
}

function bindProgrammeCards() {
  document.querySelectorAll('[data-programme-id]').forEach(button => {
    if (button.dataset.bound) return;
    button.dataset.bound = 'true';
    button.addEventListener('click', () => {
      const programme = programmes.find(item => item.id === button.dataset.programmeId);
      if (programme) ask(displayName(programme), programme);
    });
  });
}

function addUserMessage(text) {
  const node = document.createElement('article');
  node.className = 'message user-message';
  const label = userName ? escapeHtml(userName.toUpperCase()) : copy[language].you;
  node.innerHTML = `<div class="message-top"><time>${label}</time></div><div class="message-body"><p>${escapeHtml(text)}</p></div>`;
  els.conversation.append(node);
  scrollToLatest();
}

function addThinking() {
  const node = document.createElement('article');
  node.className = 'message assistant-message typing';
  node.innerHTML = `<div class="message-top"><span class="assistant-avatar"></span><span>MATRIX GUIDE</span><time>${copy[language].searching}</time></div><div class="message-body"><span class="thinking" aria-label="${copy[language].searching}"><i></i><i></i><i></i></span></div>`;
  els.conversation.append(node);
  scrollToLatest();
  return node;
}

function noMatch(query) {
  const words = copy[language];
  return {
    name: words.noResults,
    nameEn: words.noResults,
    categoryMl: 'MATRIX GUIDE',
    section: 'general',
    page: 8,
    text: words.noResultsText(query),
    textEn: words.noResultsText(query),
    facts: language === 'en' ? [['Help', 'Try a section or level'], ['Source', 'Page 8'], ['Language', 'Malayalam / English']] : [['സഹായം', 'വിഭാഗമോ ലെവലോ ശ്രമിക്കൂ'], ['ഉറവിടം', 'പേജ് 8'], ['ഭാഷ', 'മലയാളം / ഇംഗ്ലീഷ്']],
    factsEn: [['Help', 'Try a section or level'], ['Source', 'Page 8'], ['Language', 'Malayalam / English']]
  };
}

function textFor(record) {
  const facts = language === 'en' ? (record.factsEn || record.facts) : record.facts;
  const desc = (language === 'en' ? record.textEn : record.text) || record.text || record.textEn || '';
  return `${displayName(record)}. ${desc} ${facts.map(([label, value]) => `${label}: ${value}.`).join(' ')}`;
}

function factHtml([label, value]) {
  return `<div class="fact"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></div>`;
}

function richAnswer(record) {
  const facts = language === 'en' ? (record.factsEn || record.facts) : record.facts;
  const text = (language === 'en' ? record.textEn : record.text) || record.text || record.textEn || '';
  const watermarkText = 'ART ALIVE PROGRAMME DESK · MATRIX 26';
  return `
    <div class="answer-card" data-watermark="${watermarkText}">
      <h2 class="answer-title">${escapeHtml(displayName(record))}</h2>
      <p class="answer-subtitle">${escapeHtml(displaySection(record))} · ${copy[language].source}</p>
      <p class="answer-text">${escapeHtml(text)}</p>
      <div class="fact-grid">${facts.map(factHtml).join('')}</div>
      <div class="verified-source-badge">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>
        <span>${copy[language].source} · ${copy[language].page} ${record.page}</span>
        <em>OFFICIAL VERIFIED</em>
      </div>
    </div>
  `;
}

function richCollection(collection) {
  const words = copy[language];
  const title = collection.title || words.results;
  const cards = collection.matches.map(programme => `<button class="programme-card" type="button" data-programme-id="${programme.id}"><span class="programme-card-title${language === 'en' ? ' en' : ''}">${escapeHtml(displayName(programme))}</span><span class="programme-card-tags"><span class="programme-tag">${escapeHtml(displaySection(programme))}</span>${displayLevels(programme) ? `<span class="programme-tag level">${escapeHtml(displayLevels(programme))}</span>` : ''}</span></button>`).join('');
  return `<h2 class="results-heading">${escapeHtml(title)}</h2><p class="results-note">${words.choose}</p><div class="programme-list">${cards}</div>`;
}

function splitGraphemes(text) {
  if (window.Intl && Intl.Segmenter) return [...new Intl.Segmenter('ml', { granularity: 'grapheme' }).segment(text)].map(part => part.segment);
  return Array.from(text);
}

function streamResponse(node, streamText, render) {
  const body = node.querySelector('.message-body');
  const fragments = splitGraphemes(streamText);
  const stream = document.createElement('p');
  stream.className = 'streaming-text';
  body.replaceChildren(stream);
  let index = 0;
  const chunk = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? fragments.length : 3;
  const delay = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 13;
  const timer = () => {
    stream.textContent += fragments.slice(index, index + chunk).join('');
    index += chunk;
    scrollToLatest();
    if (index < fragments.length) window.setTimeout(timer, delay);
    else {
      body.innerHTML = render();
      node.classList.remove('typing');
      isReplying = false;
      els.send.disabled = false;
      bindProgrammeCards();
      scrollToLatest();
    }
  };
  timer();
}

function typeAnswer(node, record) {
  streamResponse(node, textFor(record), () => richAnswer(record));
}

function typeCollection(node, collection) {
  const heading = collection.title || copy[language].results;
  const text = language === 'en' ? `${heading}. ${collection.matches.length} programmes found.` : `${heading}. ${collection.matches.length} പരിപാടികൾ കണ്ടെത്തി.`;
  streamResponse(node, text, () => richCollection(collection));
}

function ask(raw, selectedProgramme) {
  const question = raw.trim();
  if (!question || isReplying) return;
  isReplying = true;
  els.send.disabled = true;

  // Remove welcome hub & all category cards as soon as chat starts
  const welcomeHub = els.conversation.querySelector('.welcome-hub');
  if (welcomeHub) welcomeHub.remove();

  // Hide suggestions bar when chatting for clean conversation view
  if (els.suggestions) els.suggestions.hidden = true;

  // Dismiss keyboard on submit so user can comfortably read incoming response
  els.prompt.blur();

  addUserMessage(question);
  els.prompt.value = '';
  const pending = addThinking();
  const result = selectedProgramme ? { type: 'record', record: selectedProgramme } : resolveQuery(question);
  window.setTimeout(() => {
    if (result.type === 'collection') typeCollection(pending, result);
    else typeAnswer(pending, result.record);
  }, 460);
}

function openChat() {
  els.landing.hidden = true;
  els.chat.hidden = false;
  if (!els.conversation.children.length) {
    appendWelcome();
    if (els.suggestions) els.suggestions.hidden = false;
  }
}

function resetChat() {
  if (isReplying) return;
  els.conversation.replaceChildren();
  appendWelcome();
  if (els.suggestions) els.suggestions.hidden = false;
}

function openInstall() {
  const isEn = language === 'en';
  if (deferredInstall) {
    els.installInstructions.innerHTML = isEn
      ? '<p>If you are using Android or desktop Chrome, tap the button below.</p><button class="install-action" id="nativeInstall" type="button">Install MATRIX 26</button>'
      : '<p>Android അല്ലെങ്കിൽ desktop Chrome ഉപയോഗിക്കുന്നുവെങ്കിൽ താഴെയുള്ള ബട്ടൺ തിരഞ്ഞെടുക്കൂ.</p><button class="install-action" id="nativeInstall" type="button">MATRIX 26 ഇൻസ്റ്റാൾ ചെയ്യുക</button>';
  } else if (/iPhone|iPad|iPod/.test(navigator.userAgent)) {
    els.installInstructions.innerHTML = isEn
      ? '<p>Open this page in Safari. Tap Share, then select <strong>Add to Home Screen</strong>.</p><ol class="install-list"><li>Tap Share</li><li>Select Add to Home Screen</li><li>Tap Add</li></ol>'
      : '<p>Safariയിൽ ഈ പേജ് തുറക്കുക. തുടർന്ന് Share തിരഞ്ഞെടുക്കി <strong>Add to Home Screen</strong> അമർത്തുക.</p><ol class="install-list"><li>Share തുറക്കുക</li><li>Add to Home Screen തിരഞ്ഞെടുക്കുക</li><li>Add അമർത്തുക</li></ol>';
  } else {
    els.installInstructions.innerHTML = isEn
      ? '<p>In your browser menu, select <strong>Install app</strong> or <strong>Add to Home screen</strong>. Once opened, the guide works offline.</p>'
      : '<p>ബ്രൗസർ മെനുവിൽ <strong>Install app</strong> അല്ലെങ്കിൽ <strong>Add to Home screen</strong> തിരഞ്ഞെടുക്കുക. ഒരിക്കൽ തുറന്നശേഷം ഗൈഡ് ഓഫ്ലൈനിലും ലഭ്യമാകും.</p>';
  }
  els.installDialog.showModal();
  document.querySelector('#nativeInstall')?.addEventListener('click', async () => {
    deferredInstall.prompt();
    await deferredInstall.userChoice;
    deferredInstall = null;
    els.installDialog.close();
  }, { once: true });
}

function openNameModal(shouldOpenChat = false) {
  pendingChatAfterName = shouldOpenChat;
  if (els.userNameInput) els.userNameInput.value = userName || '';
  els.nameDialog?.showModal();
  window.setTimeout(() => els.userNameInput?.focus(), 100);
}

function saveName(name) {
  const clean = String(name || '').trim();
  if (clean) {
    localStorage.setItem('matrix-user-name', clean);
    userName = clean;
  } else {
    localStorage.removeItem('matrix-user-name');
    userName = '';
  }
  updateUserGreeting();
  els.nameDialog?.close();
  if (pendingChatAfterName) {
    pendingChatAfterName = false;
    openChat();
  }
}

function skipName() {
  localStorage.setItem('matrix-name-skipped', 'true');
  els.nameDialog?.close();
  if (pendingChatAfterName) {
    pendingChatAfterName = false;
    openChat();
  }
}

function handleStartChat() {
  if (!userName && !localStorage.getItem('matrix-name-skipped')) {
    openNameModal(true);
  } else {
    openChat();
  }
}

els.start.addEventListener('click', handleStartChat);
els.openNameModal?.addEventListener('click', () => openNameModal(false));
els.closeNameDialog?.addEventListener('click', () => els.nameDialog?.close());
els.skipNameBtn?.addEventListener('click', skipName);
els.nameForm?.addEventListener('submit', event => {
  event.preventDefault();
  saveName(els.userNameInput.value);
});
els.home.addEventListener('click', () => { els.chat.hidden = true; els.landing.hidden = false; });
els.form.addEventListener('submit', event => { event.preventDefault(); ask(els.prompt.value); });
els.clear.addEventListener('click', resetChat);
document.querySelectorAll('.suggestions button').forEach(button => button.addEventListener('click', () => ask(button.dataset.prompt)));
els.language.addEventListener('click', () => setLanguage(language === 'ml' ? 'en' : 'ml'));
els.theme.addEventListener('click', () => setTheme(theme === 'dark' ? 'light' : 'dark'));
els.installButtons.forEach(button => button.addEventListener('click', openInstall));
els.closeInstall.addEventListener('click', () => els.installDialog.close());
els.devTriggers.forEach(button => button.addEventListener('click', () => els.devDialog?.showModal()));
els.closeDevDialog?.addEventListener('click', () => els.devDialog?.close());
els.dismissDevDialog?.addEventListener('click', () => els.devDialog?.close());
window.addEventListener('beforeinstallprompt', event => { event.preventDefault(); deferredInstall = event; });
window.addEventListener('appinstalled', () => { deferredInstall = null; els.installDialog.close(); });

// =========================================================================
// SECURITY & PRIVACY PROTECTION SUITE
// Anti-copy, Anti-screenshot, Anti-inspect, and Dynamic Watermarking
// =========================================================================
function activatePrivacyShield(showNotice = false) {
  document.querySelector('.app-shell')?.classList.add('security-blur');
  if (showNotice) {
    const shield = document.querySelector('#securityShield');
    if (shield) shield.classList.add('is-active');
  }
}

function deactivatePrivacyShield() {
  document.querySelector('.app-shell')?.classList.remove('security-blur');
  const shield = document.querySelector('#securityShield');
  if (shield) shield.classList.remove('is-active');
}

window.addEventListener('blur', () => activatePrivacyShield(true));
window.addEventListener('focus', () => deactivatePrivacyShield());
document.addEventListener('visibilitychange', () => {
  if (document.hidden) activatePrivacyShield(true);
  else deactivatePrivacyShield();
});

window.addEventListener('keyup', event => {
  if (event.key === 'PrintScreen' || event.keyCode === 44) {
    activatePrivacyShield(true);
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText('MATRIX 26 Official Festival Guide — Confidential & Protected Content');
    }
    window.setTimeout(() => deactivatePrivacyShield(), 1200);
  }
});

window.addEventListener('keydown', event => {
  const isCtrlOrCmd = event.ctrlKey || event.metaKey;
  if (event.key === 'PrintScreen' || event.keyCode === 44) {
    activatePrivacyShield(true);
    window.setTimeout(() => deactivatePrivacyShield(), 1200);
    event.preventDefault();
    return;
  }
  if (isCtrlOrCmd && (event.key === 's' || event.key === 'S')) {
    event.preventDefault();
    return false;
  }
  if (isCtrlOrCmd && (event.key === 'p' || event.key === 'P')) {
    event.preventDefault();
    return false;
  }
  if (isCtrlOrCmd && (event.key === 'u' || event.key === 'U')) {
    event.preventDefault();
    return false;
  }
  if (
    event.key === 'F12' ||
    (isCtrlOrCmd && event.shiftKey && ['i', 'I', 'j', 'J', 'c', 'C'].includes(event.key))
  ) {
    event.preventDefault();
    return false;
  }
});

document.addEventListener('contextmenu', event => event.preventDefault());
document.addEventListener('copy', event => event.preventDefault());
document.addEventListener('cut', event => event.preventDefault());
document.addEventListener('dragstart', event => event.preventDefault());

setTheme(theme);
updateInterface();

if ('serviceWorker' in navigator && location.protocol !== 'file:') {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js?v=28').then(reg => {
      reg.update();
    }).catch(err => console.warn('SW registration warning:', err));
  });
  let refreshing = false;
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    if (!refreshing) {
      refreshing = true;
      window.location.reload();
    }
  });
}
'''

full_app_code = programmes_js + script_tail

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(full_app_code)

print('app.js successfully generated! Size:', len(full_app_code), 'bytes')
