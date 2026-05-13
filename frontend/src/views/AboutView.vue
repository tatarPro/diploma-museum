<template>
  <div class="about-page">
    <TheNavbar />

    <!-- Заголовок страницы -->
    <section class="page-hero">
      <div class="container">
        <p class="page-hero__eyebrow">История отряда</p>
        <h1 class="page-hero__title">О нас</h1>
      </div>
    </section>

    <!-- Основной контент: шкала слева + текст справа -->
    <section class="timeline-section">
      <div class="container timeline-layout">

        <!-- Левая колонка: фиксированная шкала годов -->
        <aside class="year-rail" ref="yearRailEl">
          <div class="year-rail__track">
            <div
              v-for="(milestone, index) in milestones"
              :key="milestone.year"
              class="year-rail__item"
              :class="{ active: activeIndex === index }"
              @click="scrollToMilestone(index)"
            >
              <span class="year-rail__dot"></span>
              <span class="year-rail__label">{{ milestone.year }}</span>
            </div>
            <!-- Вертикальная линия -->
            <div class="year-rail__line">
              <div
                class="year-rail__progress"
                :style="{ height: progressPercent + '%' }"
              ></div>
            </div>
          </div>
        </aside>

        <!-- Правая колонка: карточки вех -->
        <div class="milestones-list" ref="milestonesListEl">
          <article
            v-for="(milestone, index) in milestones"
            :key="milestone.year"
            class="milestone-card"
            :ref="el => { if (el) milestoneEls[index] = el }"
            :class="{ 'milestone-card--visible': visibleSet.has(index) }"
          >
            <div class="milestone-card__year">{{ milestone.year }}</div>
            <h2 class="milestone-card__title">{{ milestone.title }}</h2>
            <p class="milestone-card__text">{{ milestone.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- Блок «Наша миссия» -->
    <section class="mission-section">
      <div class="container mission-inner">
        <div class="mission-text">
          <h2>Наша миссия</h2>
          <p>
            Студенческий поисковый отряд "НОРД" ведёт работу по увековечению памяти
            погибших в годы Великой Отечественной войны. Мы организуем
            полевые экспедиции, проводим архивные исследования и занимаемся
            патриотическим воспитанием молодёжи.
          </p>
          <p>
            За годы работы отряд принял участие в десятках экспедиций,
            установил судьбы сотен бойцов и вернул их имена истории.
          </p>
          <router-link to="/join" class="btn btn-primary" style="margin-top: 8px">
            Вступить в отряд
          </router-link>
        </div>
        <div class="mission-stats">
          <div class="stat">
            <span class="stat__number">30+</span>
            <span class="stat__label">лет поискового движения</span>
          </div>
          <div class="stat">
            <span class="stat__number">20+</span>
            <span class="stat__label">полевых экспедиций</span>
          </div>
          <div class="stat">
            <span class="stat__number">100+</span>
            <span class="stat__label">установленных имён</span>
          </div>
        </div>
      </div>
    </section>

    <footer class="footer">
      <div class="container footer__inner">
        <span>© {{ new Date().getFullYear() }} Музей студенческого поискового отряда "НОРД"</span>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount, computed } from 'vue'
import TheNavbar from '@/components/TheNavbar.vue'

// ─── Вехи истории ─────────────────────────────────────────────────────────────
const milestones = [
  {
    year: 1996,
    title: 'Создание отряда и первая экспедиция',
    text: 'Поисковый отряд был основан в учебном заведении. В том же году состоялась первая полевая экспедиция — начало большого пути по сохранению исторической памяти о павших защитниках Отечества.',
  },
  {
    year: 2002,
    title: 'Основание нового отряда',
    text: 'В связи со сменой места базирования был основан новый отряд, принявший эстафету от предшественников. Накопленный опыт и традиции были сохранены и приумножены.',
  },
  {
    year: 2003,
    title: 'Первая экспедиция нового отряда',
    text: 'Обновлённый состав отряда провёл первую самостоятельную экспедицию. Были заложены новые методики работы, укреплено взаимодействие с региональными поисковыми объединениями.',
  },
  {
    year: 2019,
    title: 'Создание некоммерческой организации',
    text: 'Поисковая деятельность обрела новый юридический статус — была зарегистрирована некоммерческая организация. Это открыло возможности для участия в федеральных грантовых программах и расширения географии работы.',
  },
  {
    year: 2026,
    title: '30 лет поисковому движению',
    text: 'Юбилейный год — три десятилетия поискового движения в учебном заведении. За это время сложилась устойчивая традиция студенческого поиска, воспитаны сотни неравнодушных к истории молодых людей.',
  },
]

// ─── Refs и состояние ─────────────────────────────────────────────────────────
const milestoneEls    = reactive([])
const milestonesListEl = ref(null)
const activeIndex     = ref(0)
const visibleSet      = reactive(new Set())

// Прогресс линии (0–100%)
const progressPercent = computed(() => {
  if (milestones.length <= 1) return 100
  return (activeIndex.value / (milestones.length - 1)) * 100
})

// ─── Intersection Observer — отслеживаем видимость карточек ──────────────────
let observer = null

onMounted(() => {
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const idx = milestoneEls.findIndex(el => el === entry.target)
        if (idx === -1) return

        if (entry.isIntersecting) {
          visibleSet.add(idx)
          // Активный год = самый нижний видимый элемент в верхней половине вьюпорта
          if (entry.boundingClientRect.top < window.innerHeight * 0.55) {
            activeIndex.value = idx
          }
        }
      })
    },
    {
      threshold: 0.25,
      rootMargin: '0px 0px -15% 0px',
    },
  )

  milestoneEls.forEach(el => { if (el) observer.observe(el) })
})

onBeforeUnmount(() => {
  if (observer) observer.disconnect()
})

// ─── Скролл к вехе при клике на год ──────────────────────────────────────────
function scrollToMilestone(index) {
  const el = milestoneEls[index]
  if (!el) return
  el.scrollIntoView({ behavior: 'smooth', block: 'center' })
}
</script>

<style scoped>
/* ─── Page hero ───────────────────────────────────────────────────────────── */
.page-hero {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  padding: 56px 0 40px;
}
.page-hero__eyebrow {
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--color-accent);
  margin-bottom: 10px;
}
.page-hero__title {
  font-size: clamp(2rem, 4vw, 3rem);
  color: var(--color-text);
}

/* ─── Timeline section ────────────────────────────────────────────────────── */
.timeline-section {
  padding: 80px 0 100px;
}

.timeline-layout {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 0 64px;
  align-items: start;
}

/* ─── Year rail (левая фиксированная колонка) ────────────────────────────── */
.year-rail {
  position: sticky;
  top: 88px; /* высота навбара + отступ */
  align-self: start;
}

.year-rail__track {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0;
  padding-left: 28px; /* место для линии */
}

/* Вертикальная линия-трек */
.year-rail__line {
  position: absolute;
  left: 8px;
  top: 8px;
  bottom: 8px;
  width: 2px;
  background: var(--color-border);
  border-radius: 2px;
  overflow: hidden;
}

/* Заполненная часть линии */
.year-rail__progress {
  width: 100%;
  background: var(--color-accent);
  border-radius: 2px;
  transition: height 0.45s cubic-bezier(0.4, 0, 0.2, 1);
  min-height: 0;
}

.year-rail__item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 0;
  cursor: pointer;
  position: relative;
}

.year-rail__dot {
  position: absolute;
  left: -24px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--color-border);
  border: 2px solid var(--color-surface);
  box-shadow: 0 0 0 1px var(--color-border);
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.year-rail__item.active .year-rail__dot {
  background: var(--color-accent);
  box-shadow: 0 0 0 3px rgba(139,69,19,0.2);
  transform: scale(1.25);
}

.year-rail__label {
  font-family: var(--font-display);
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--color-text-muted);
  transition: color 0.3s ease, transform 0.3s ease;
  line-height: 1;
}

.year-rail__item.active .year-rail__label {
  color: var(--color-accent);
  font-size: 1.15rem;
  transform: translateX(2px);
}

.year-rail__item:hover .year-rail__label {
  color: var(--color-text);
}

/* ─── Milestone cards (правая колонка) ───────────────────────────────────── */
.milestones-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.milestone-card {
  padding: 56px 0 56px;
  border-bottom: 1px solid var(--color-border);
  opacity: 0;
  transform: translateY(32px);
  transition: opacity 0.55s ease, transform 0.55s ease;
}
.milestone-card:last-child { border-bottom: none; }

.milestone-card--visible {
  opacity: 1;
  transform: translateY(0);
}

/* Задержка для каждой карточки */
.milestone-card:nth-child(1) { transition-delay: 0s; }
.milestone-card:nth-child(2) { transition-delay: 0.08s; }
.milestone-card:nth-child(3) { transition-delay: 0.12s; }
.milestone-card:nth-child(4) { transition-delay: 0.16s; }
.milestone-card:nth-child(5) { transition-delay: 0.20s; }

.milestone-card__year {
  font-family: var(--font-display);
  font-size: 3rem;
  font-weight: 700;
  color: var(--color-accent);
  opacity: 0.18;
  line-height: 1;
  margin-bottom: 12px;
  letter-spacing: -0.02em;
}

.milestone-card__title {
  font-size: 1.45rem;
  margin-bottom: 16px;
  color: var(--color-text);
}

.milestone-card__text {
  font-size: 1rem;
  color: var(--color-text-muted);
  line-height: 1.75;
  max-width: 640px;
}

/* ─── Mission section ─────────────────────────────────────────────────────── */
.mission-section {
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
  padding: 80px 0;
}

.mission-inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 64px;
  align-items: center;
}

.mission-text h2 {
  font-size: 1.8rem;
  margin-bottom: 20px;
}

.mission-text p {
  color: var(--color-text-muted);
  line-height: 1.8;
  margin-bottom: 16px;
}

.mission-stats {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding-left: 20px;
  border-left: 3px solid var(--color-accent);
}

.stat__number {
  font-family: var(--font-display);
  font-size: 2.4rem;
  font-weight: 700;
  color: var(--color-text);
  line-height: 1;
}

.stat__label {
  font-size: 0.88rem;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 500;
}

/* ─── Footer ─────────────────────────────────────────────────────────────── */
.footer {
  background: var(--color-bg);
  border-top: 1px solid var(--color-border);
  padding: 24px;
}
.footer__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  color: var(--color-text-muted);
  font-size: 0.85rem;
}

/* ─── Адаптив ─────────────────────────────────────────────────────────────── */
@media (max-width: 768px) {
  .timeline-layout {
    grid-template-columns: 1fr;
  }

  .year-rail {
    position: static;
    display: flex;
    overflow-x: auto;
    padding-bottom: 12px;
    margin-bottom: 32px;
    border-bottom: 1px solid var(--color-border);
  }

  .year-rail__track {
    flex-direction: row;
    padding-left: 0;
    padding-bottom: 16px;
    gap: 0;
    width: max-content;
  }

  .year-rail__line { display: none; }

  .year-rail__item {
    flex-direction: column;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
  }

  .year-rail__dot {
    position: static;
    width: 8px;
    height: 8px;
  }

  .year-rail__label { font-size: 0.85rem; }
  .year-rail__item.active .year-rail__label { font-size: 0.95rem; transform: none; }

  .mission-inner {
    grid-template-columns: 1fr;
    gap: 40px;
  }
}
</style>
