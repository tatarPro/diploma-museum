-- ============================================================
--  Единая информационная система музея поискового отряда
--  База данных: museum_db
--  СУБД: MySQL 8.0+
--  Кодировка: utf8mb4 (полная поддержка Unicode и эмодзи)
-- ============================================================

CREATE DATABASE IF NOT EXISTS museum_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE museum_db;

-- ============================================================
--  1. ПОЛЬЗОВАТЕЛИ
--  Хранит учётные записи администраторов и модераторов.
--  Пароли хранятся только в виде bcrypt-хешей.
-- ============================================================

CREATE TABLE users (
    id            INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    login         VARCHAR(64)     NOT NULL,
    password_hash VARCHAR(255)    NOT NULL,
    role          ENUM('admin', 'moderator') NOT NULL DEFAULT 'moderator',
    created_at    DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_users_login (login)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Учётные записи сотрудников административной панели';

-- ============================================================
--  2. СТАТЬИ (ИСТОРИИ ЭКСПЕДИЦИЙ)
--  Каждая статья привязана к автору (пользователю).
--  При удалении автора author_id обнуляется (SET NULL),
--  сама статья остаётся в системе.
-- ============================================================

CREATE TABLE articles (
    id                INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    title             VARCHAR(255)    NOT NULL,
    content           LONGTEXT        NOT NULL,
    preview_image_url VARCHAR(512)    NULL     DEFAULT NULL
                      COMMENT 'Относительный путь: /static/images/...',
    main_image_url    VARCHAR(512)    NULL     DEFAULT NULL
                      COMMENT 'Относительный путь: /static/images/...',
    author_id         INT UNSIGNED    NULL     DEFAULT NULL,
    created_at        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    KEY idx_articles_author   (author_id),
    KEY idx_articles_created  (created_at),

    CONSTRAINT fk_articles_author
        FOREIGN KEY (author_id)
        REFERENCES users (id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Статьи об экспедициях поискового отряда';

-- ============================================================
--  3. ИЗОБРАЖЕНИЯ ГАЛЕРЕИ СТАТЬИ
--  Дополнительные фотографии к статье.
--  При удалении статьи все её изображения удаляются каскадно.
-- ============================================================

CREATE TABLE article_images (
    id         INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    url        VARCHAR(512)    NOT NULL
               COMMENT 'Относительный путь: /static/images/...',
    article_id INT UNSIGNED    NOT NULL,

    PRIMARY KEY (id),
    KEY idx_article_images_article (article_id),

    CONSTRAINT fk_article_images_article
        FOREIGN KEY (article_id)
        REFERENCES articles (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Изображения галереи статей';

-- ============================================================
--  4. ЭКСПОНАТЫ
--  Каждый экспонат может иметь фотографию и 3D-модель (GLB).
--  model_url = NULL означает, что модель ещё не загружена.
--  При удалении автора author_id обнуляется (SET NULL).
-- ============================================================

CREATE TABLE exhibits (
    id          INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    title       VARCHAR(255)    NOT NULL,
    description LONGTEXT        NOT NULL,
    photo_url   VARCHAR(512)    NULL     DEFAULT NULL
                COMMENT 'Относительный путь: /static/images/...',
    model_url   VARCHAR(512)    NULL     DEFAULT NULL
                COMMENT 'Относительный путь к GLB-файлу: /static/models/...',
    author_id   INT UNSIGNED    NULL     DEFAULT NULL,
    created_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    KEY idx_exhibits_author  (author_id),
    KEY idx_exhibits_created (created_at),

    CONSTRAINT fk_exhibits_author
        FOREIGN KEY (author_id)
        REFERENCES users (id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Экспонаты музея поискового отряда';

-- ============================================================
--  5. ИЗОБРАЖЕНИЯ ГАЛЕРЕИ ЭКСПОНАТА
--  Дополнительные фотографии к экспонату.
--  При удалении экспоната все его изображения удаляются каскадно.
-- ============================================================

CREATE TABLE exhibit_images (
    id         INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    url        VARCHAR(512)    NOT NULL
               COMMENT 'Относительный путь: /static/images/...',
    exhibit_id INT UNSIGNED    NOT NULL,

    PRIMARY KEY (id),
    KEY idx_exhibit_images_exhibit (exhibit_id),

    CONSTRAINT fk_exhibit_images_exhibit
        FOREIGN KEY (exhibit_id)
        REFERENCES exhibits (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Изображения галереи экспонатов';

-- ============================================================
--  ПРОВЕРКА СТРУКТУРЫ
-- ============================================================

-- Посмотреть все таблицы
-- SHOW TABLES;

-- Посмотреть связи конкретной таблицы
-- SELECT
--     TABLE_NAME,
--     COLUMN_NAME,
--     CONSTRAINT_NAME,
--     REFERENCED_TABLE_NAME,
--     REFERENCED_COLUMN_NAME
-- FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
-- WHERE TABLE_SCHEMA = 'museum_db'
--   AND REFERENCED_TABLE_NAME IS NOT NULL;
