// ── NAV SCROLL ──
const nav = document.querySelector('nav');
window.addEventListener('scroll', () => {
  nav?.classList.toggle('scrolled', window.scrollY > 20);
});

// ── SCROLL REVEAL ──
const revealElements = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      setTimeout(() => entry.target.classList.add('visible'), i * 100);
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });
revealElements.forEach(el => observer.observe(el));

// ── ANIMATED COUNTERS ──
function animateCounter(el) {
  const target = parseInt(el.dataset.target || el.textContent, 10);
  if (isNaN(target)) return;
  const duration = 2000;
  const start = performance.now();
  const update = (now) => {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.floor(eased * target).toLocaleString();
    if (progress < 1) requestAnimationFrame(update);
    else el.textContent = target.toLocaleString();
  };
  requestAnimationFrame(update);
}

const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      animateCounter(entry.target);
      counterObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('.stat-number[data-target]').forEach(el => counterObserver.observe(el));

// ── COPY ROOM CODE ──
window.copyCode = function(code) {
  navigator.clipboard.writeText(code).then(() => {
    const btn = document.querySelector('.copy-btn');
    if (btn) {
      const original = btn.innerHTML;
      btn.innerHTML = '✓ Copied!';
      btn.style.color = '#4ade80';
      setTimeout(() => { btn.innerHTML = original; btn.style.color = ''; }, 2000);
    }
  });
};

// ── COPY ROOM LINK ──
window.copyLink = function() {
  navigator.clipboard.writeText(window.location.href).then(() => {
    showToast('Room link copied!', 'success');
  });
};

// ── AUTO-DISMISS ALERTS ──
document.querySelectorAll('.alert').forEach(alert => {
  alert.addEventListener('click', () => alert.remove());
  setTimeout(() => {
    alert.style.transition = 'opacity 0.4s, transform 0.4s';
    alert.style.opacity = '0';
    alert.style.transform = 'translateX(120%)';
    setTimeout(() => alert.remove(), 400);
  }, 4000);
});

// ── TOAST ──
function showToast(msg, type = 'info') {
  const bar = document.querySelector('.messages-bar') || (() => {
    const b = document.createElement('div');
    b.className = 'messages-bar';
    document.body.appendChild(b);
    return b;
  })();
  const toast = document.createElement('div');
  toast.className = `alert alert-${type}`;
  toast.innerHTML = `<span>${type === 'success' ? '✓' : 'ℹ'}</span> ${msg}`;
  bar.appendChild(toast);
  toast.addEventListener('click', () => toast.remove());
  setTimeout(() => { toast.style.opacity = '0'; setTimeout(() => toast.remove(), 400); }, 3500);
}

// ── CODE INPUT AUTO-UPPERCASE ──
const codeInput = document.querySelector('.code-input');
if (codeInput) {
  codeInput.addEventListener('input', e => {
    const pos = e.target.selectionStart;
    e.target.value = e.target.value.toUpperCase();
    e.target.setSelectionRange(pos, pos);
  });
}

// ── PARTICLE EFFECT ON HERO ──
const hero = document.querySelector('.hero');
if (hero) {
  for (let i = 0; i < 20; i++) {
    const particle = document.createElement('div');
    particle.style.cssText = `
      position:absolute;
      width:${Math.random()*3+1}px;
      height:${Math.random()*3+1}px;
      background:rgba(26,108,245,${Math.random()*0.4+0.1});
      border-radius:50%;
      left:${Math.random()*100}%;
      top:${Math.random()*100}%;
      animation: particleFly ${Math.random()*10+8}s linear ${Math.random()*5}s infinite;
      pointer-events:none;
    `;
    hero.appendChild(particle);
  }

  const style = document.createElement('style');
  style.textContent = `
    @keyframes particleFly {
      0% { transform: translateY(0) scale(1); opacity: 0; }
      10% { opacity: 1; }
      90% { opacity: 1; }
      100% { transform: translateY(-80vh) scale(0); opacity: 0; }
    }
  `;
  document.head.appendChild(style);
}
