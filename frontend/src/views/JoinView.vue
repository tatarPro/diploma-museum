<template>
  <div class="join-page">
    <TheNavbar />

    <!-- Заголовок -->
    <section class="page-hero">
      <div class="container">
        <p class="page-hero__eyebrow">Стань частью команды</p>
        <h1 class="page-hero__title">Вступить в отряд</h1>
      </div>
    </section>

    <div class="container join-layout">

      <!-- Блок 1: О вступлении -->
      <section class="join-section fade-up">
        <h2 class="join-section__title">Кто может вступить</h2>
        <div class="join-text">
          <p>
            В поисковый отряд приглашаются студенты учебного заведения, а также
            все желающие в возрасте от 14 лет, разделяющие ценности сохранения
            исторической памяти и готовые к активной работе.
          </p>
          <p>
            Специальной подготовки не требуется — всему необходимому мы обучаем
            в ходе подготовительных занятий. Главное — желание, ответственность
            и готовность работать в команде.
          </p>

          <h3>Что вас ждёт</h3>
          <ul class="join-list">
            <li>Участие в полевых поисковых экспедициях</li>
            <li>Архивная и исследовательская работа</li>
            <li>Работа с музейными экспонатами и фондами</li>
            <li>Участие в памятных мероприятиях и вахтах памяти</li>
            <li>Взаимодействие с региональными и федеральными поисковыми организациями</li>
            <li>Живое профессиональное сообщество и поддержка опытных участников</li>
          </ul>

          <h3>Как вступить</h3>
          <ol class="join-steps">
            <li>
              <span class="step-num">1</span>
              <div>
                <strong>Свяжитесь с нами</strong>
                <p>Напишите на электронную почту или позвоните по телефону, указанным ниже. Кратко расскажите о себе и своём интересе к поисковой работе.</p>
              </div>
            </li>
            <li>
              <span class="step-num">2</span>
              <div>
                <strong>Знакомство с отрядом</strong>
                <p>Мы пригласим вас на встречу с действующими участниками отряда, где вы сможете задать любые вопросы и познакомиться с нашей деятельностью.</p>
              </div>
            </li>
            <li>
              <span class="step-num">3</span>
              <div>
                <strong>Подготовительный курс</strong>
                <p>Новые участники проходят вводный курс по методике поисковой работы, основам полевой безопасности и работе с документацией.</p>
              </div>
            </li>
            <li>
              <span class="step-num">4</span>
              <div>
                <strong>Первая экспедиция</strong>
                <p>После подготовки вы участвуете в ближайшей экспедиции в составе основного отряда под руководством опытных поисковиков.</p>
              </div>
            </li>
          </ol>
        </div>
      </section>

      <!-- Блок 2: Контакты -->
      <section class="join-section fade-up" style="animation-delay: 0.1s">
        <h2 class="join-section__title">Контактные данные</h2>
        <div class="contacts-grid">
          <div class="contact-card">
            <div class="contact-card__icon-wrap">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
            </div>
            <div>
              <p class="contact-card__label">Электронная почта</p>
              <a href="mailto:poisk@example.ru" class="contact-card__value">poisk@example.ru</a>
            </div>
          </div>

          <div class="contact-card">
            <div class="contact-card__icon-wrap">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81 19.79 19.79 0 01.07 1.18 2 2 0 012.07 0h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/>
              </svg>
            </div>
            <div>
              <p class="contact-card__label">Телефон</p>
              <a href="tel:+79001234567" class="contact-card__value">+7 (900) 123-45-67</a>
            </div>
          </div>

          <div class="contact-card">
            <div class="contact-card__icon-wrap">
              <!-- VK icon -->
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M15.07 2H8.93C3.33 2 2 3.33 2 8.93v6.14C2 20.67 3.33 22 8.93 22h6.14C20.67 22 22 20.67 22 15.07V8.93C22 3.33 20.67 2 15.07 2zm3.08 13.67h-1.72c-.65 0-.85-.52-2.01-1.69-.99-.99-1.43-.99-1.43-.99s-.18 0-.18.63v1.54c0 .45-.14.63-1.18.63-1.76 0-3.7-1.07-5.07-3.07-2.06-2.89-2.62-5.04-2.62-5.48 0-.24.09-.45.54-.45h1.72c.4 0 .55.18.71.63.78 2.24 2.08 4.2 2.61 4.2.2 0 .29-.09.29-.58V9.76c-.06-1.04-.61-1.13-.61-1.5 0-.18.14-.36.38-.36h2.7c.33 0 .45.18.45.54v2.92c0 .33.15.45.24.45.2 0 .38-.12.76-.51 1.17-1.31 2-3.33 2-3.33.11-.24.31-.45.72-.45h1.72c.51 0 .63.27.51.54-.21 1-.89 2.08-2.13 3.74-.22.3-.31.45 0 .78.22.24.96.93 1.45 1.5.9 1.01 1.58 1.86 1.76 2.44.2.57-.1.87-.6.87z"/>
              </svg>
            </div>
            <div>
              <p class="contact-card__label">ВКонтакте</p>
              <a href="https://vk.com/club13035025" target="_blank" rel="noopener noreferrer" class="contact-card__value">Группа в ВК</a>
            </div>
          </div>

          <div class="contact-card">
            <div class="contact-card__icon-wrap">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                <path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
            </div>
            <div>
              <p class="contact-card__label">Адрес</p>
              <p class="contact-card__value contact-card__value--text">
                г. Сургут, ул. Пушкина, д. 10,<br>каб. 30
              </p>
            </div>
          </div>

          <div class="contact-card">
            <div class="contact-card__icon-wrap">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 6v6l4 2"/>
              </svg>
            </div>
            <div>
              <p class="contact-card__label">Часы работы</p>
              <p class="contact-card__value contact-card__value--text">
                Пн–Пт: 9:00 – 17:00<br>
                Сб: 11:00 – 15:00
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Блок 3: Карта -->
      <section class="join-section fade-up" style="animation-delay: 0.2s">
        <h2 class="join-section__title">Как нас найти</h2>
        <div class="map-wrapper">
          <!--
            Замените src на реальный iframe-код из Яндекс.Карт:
            1. Откройте maps.yandex.ru
            2. Найдите нужный адрес
            3. Нажмите «Поделиться» → «Встроить на сайт»
            4. Скопируйте код iframe и вставьте сюда
          -->
            <iframe src="https://yandex.ru/map-widget/v1/?ll=73.415335%2C61.262759&mode=poi&poi%5Bpoint%5D=73.412539%2C61.262886&poi%5Buri%5D=ymapsbm1%3A%2F%2Forg%3Foid%3D56105853521&z=16.8" width="850" height="410" frameborder="1" allowfullscreen="true" style="position:relative;">
            </iframe>
        </div>
        <p class="map-hint">
          Ближайшая остановка: Школа. Вход со стороны главного корпуса учебного заведения.
        </p>
      </section>

    </div><!-- /container -->

    <footer class="footer">
      <div class="container footer__inner">
        <span>© {{ new Date().getFullYear() }} Поисковый отряд "НОРД"</span>
      </div>
    </footer>
  </div>
</template>

<script setup>
import TheNavbar from '@/components/TheNavbar.vue'
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

/* ─── Layout ──────────────────────────────────────────────────────────────── */
.join-layout {
  padding-top: 64px;
  padding-bottom: 80px;
  display: flex;
  flex-direction: column;
  gap: 80px;
  max-width: 900px;
}

.join-section__title {
  font-size: 1.55rem;
  margin-bottom: 28px;
  padding-bottom: 14px;
  border-bottom: 2px solid var(--color-accent);
  display: inline-block;
}

/* ─── Текст ───────────────────────────────────────────────────────────────── */
.join-text p {
  color: var(--color-text-muted);
  line-height: 1.8;
  margin-bottom: 20px;
  font-size: 1rem;
}

.join-text h3 {
  font-size: 1.1rem;
  margin: 32px 0 14px;
  color: var(--color-text);
}

/* ─── Список преимуществ ─────────────────────────────────────────────────── */
.join-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 8px;
}
.join-list li {
  color: var(--color-text-muted);
  font-size: 0.95rem;
  line-height: 1.6;
  padding-left: 20px;
  position: relative;
}
.join-list li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 9px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-accent);
}

/* ─── Шаги ────────────────────────────────────────────────────────────────── */
.join-steps {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.join-steps li {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}
.step-num {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--color-accent);
  color: #fff;
  font-weight: 700;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 2px;
}
.join-steps li div strong {
  display: block;
  font-size: 0.95rem;
  margin-bottom: 6px;
  color: var(--color-text);
}
.join-steps li div p {
  font-size: 0.9rem;
  color: var(--color-text-muted);
  line-height: 1.65;
  margin: 0;
}

/* ─── Контакты ────────────────────────────────────────────────────────────── */
.contacts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.contact-card {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 20px 24px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  transition: box-shadow var(--transition), border-color var(--transition);
}
.contact-card:hover {
  box-shadow: var(--shadow-md);
  border-color: var(--color-accent);
}

.contact-card__icon-wrap {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-sm);
  background: rgba(139,69,19,0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-accent);
  margin-top: 2px;
}
.contact-card__icon-wrap svg {
  width: 20px;
  height: 20px;
}

.contact-card__label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: 5px;
}

.contact-card__value {
  font-size: 0.95rem;
  color: var(--color-text);
  font-weight: 500;
  text-decoration: none;
  transition: color var(--transition);
  display: block;
}
a.contact-card__value:hover { color: var(--color-accent); }
.contact-card__value--text {
  line-height: 1.6;
}

/* ─── Карта ───────────────────────────────────────────────────────────────── */
.map-wrapper {
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
}

.map-iframe {
  width: 100%;
  height: 420px;
  border: none;
  display: block;
}

.map-hint {
  margin-top: 14px;
  font-size: 0.875rem;
  color: var(--color-text-muted);
  line-height: 1.6;
}

/* ─── Footer ─────────────────────────────────────────────────────────────── */
.footer {
  background: var(--color-surface);
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
@media (max-width: 600px) {
  .contacts-grid { grid-template-columns: 1fr; }
  .map-iframe { height: 300px; }
  .join-steps li { flex-direction: column; gap: 10px; }
}
</style>
