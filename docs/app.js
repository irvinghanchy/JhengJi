// JhengJi Fonts Interactive Script

document.addEventListener('DOMContentLoaded', () => {
  // 1. Playground Controls
  const previewEditor = document.getElementById('previewEditor');
  const fontSelect = document.getElementById('fontSelect');
  const weightSelect = document.getElementById('weightSelect');
  const sizeSlider = document.getElementById('sizeSlider');
  const sizeValue = document.getElementById('sizeValue');
  const charCount = document.getElementById('charCount');

  // Responsive default font size for mobile
  if (window.innerWidth <= 480 && sizeSlider.value === '48') {
    sizeSlider.value = '36';
  }

  // 0. Mobile Navigation Menu Toggle
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const navMenu = document.getElementById('navMenu');
  const navOverlay = document.getElementById('navOverlay');

  function toggleMobileMenu(open) {
    const isOpen = open !== undefined ? open : !navMenu.classList.contains('active');
    navMenu.classList.toggle('active', isOpen);
    navOverlay.classList.toggle('active', isOpen);
    mobileMenuBtn.classList.toggle('active', isOpen);
    mobileMenuBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    document.body.classList.toggle('nav-open', isOpen);
  }

  if (mobileMenuBtn && navMenu && navOverlay) {
    mobileMenuBtn.addEventListener('click', () => toggleMobileMenu());
    navOverlay.addEventListener('click', () => toggleMobileMenu(false));

    // Close mobile menu when clicking any nav link
    const navLinks = navMenu.querySelectorAll('a');
    navLinks.forEach(link => {
      link.addEventListener('click', () => toggleMobileMenu(false));
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && navMenu.classList.contains('active')) {
        toggleMobileMenu(false);
      }
    });

    if (window.location.hash === '#menu') {
      toggleMobileMenu(true);
    }
  }

  function updatePlaygroundStyle() {
    const font = fontSelect.value;
    if (font === 'kai') {
      previewEditor.style.fontFamily = "'JhengJi Kai', cursive";
      previewEditor.style.fontWeight = '400';
      weightSelect.disabled = true;
    } else {
      previewEditor.style.fontFamily = "'JhengJi Song', serif";
      previewEditor.style.fontWeight = weightSelect.value;
      weightSelect.disabled = false;
    }

    const size = sizeSlider.value;
    previewEditor.style.fontSize = `${size}px`;
    sizeValue.textContent = `${size}px`;

    charCount.textContent = previewEditor.value.length;
  }

  fontSelect.addEventListener('change', updatePlaygroundStyle);
  weightSelect.addEventListener('change', updatePlaygroundStyle);
  sizeSlider.addEventListener('input', updatePlaygroundStyle);
  previewEditor.addEventListener('input', () => {
    charCount.textContent = previewEditor.value.length;
  });

  // Sample Chips
  const sampleChips = document.querySelectorAll('.sample-chip');
  sampleChips.forEach(chip => {
    chip.addEventListener('click', () => {
      previewEditor.value = chip.dataset.sample;
      updatePlaygroundStyle();
    });
  });

  // 2. Interactive Tally Counter
  let currentCount = 18;
  const countNum = document.getElementById('countNum');
  const tallyOutput = document.getElementById('tallyOutput');
  const btnPlus1 = document.getElementById('btnPlus1');
  const btnPlus5 = document.getElementById('btnPlus5');
  const btnReset = document.getElementById('btnReset');
  const counterFontSelect = document.getElementById('counterFontSelect');

  function formatTally(count) {
    if (count <= 0) return '（點擊＋１開始計數）';
    const full = Math.floor(count / 5);
    const rem = count % 5;
    let s = '5'.repeat(full);
    if (rem > 0) {
      s += rem.toString();
    }
    return s;
  }

  function updateCounter() {
    countNum.textContent = currentCount;
    const tallyStr = formatTally(currentCount);
    tallyOutput.textContent = tallyStr;

    if (counterFontSelect.value === 'kai') {
      tallyOutput.style.fontFamily = "'JhengJi Kai', cursive";
      tallyOutput.style.fontWeight = '400';
    } else {
      tallyOutput.style.fontFamily = "'JhengJi Song', serif";
      tallyOutput.style.fontWeight = '600';
    }
  }

  btnPlus1.addEventListener('click', () => {
    currentCount += 1;
    updateCounter();
  });

  btnPlus5.addEventListener('click', () => {
    currentCount += 5;
    updateCounter();
  });

  btnReset.addEventListener('click', () => {
    currentCount = 0;
    updateCounter();
  });

  counterFontSelect.addEventListener('change', updateCounter);

  // 3. Copy Code Buttons
  const copyBtns = document.querySelectorAll('.copy-btn');
  copyBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const codeId = btn.dataset.target;
      const codeEl = document.getElementById(codeId);
      if (codeEl) {
        navigator.clipboard.writeText(codeEl.textContent.trim()).then(() => {
          const original = btn.textContent;
          btn.textContent = '已複製！';
          setTimeout(() => {
            btn.textContent = original;
          }, 2000);
        });
      }
    });
  });

  // Initial runs
  updatePlaygroundStyle();
  updateCounter();
});
