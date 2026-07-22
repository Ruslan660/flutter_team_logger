# Session File Logs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** File-based session log storage for `flutter_team_logger`: логи каждой сессии пишутся на диск, переживают краш, отдаются в саппорт по `collectFiles()`.

**Architecture:** Новый publisher `FileLogStorage` поверх `AsyncPublisherBase<Log>` (очередь + последовательный `handle()`). Записи — JSON Lines, сессия разбита на чанки с ротацией (жертвуем началом, храним хвост). Retention чистится при старте. Чистые Dart-модули: options, encoder, naming, retention, storage.

**Tech Stack:** Dart (dart:io, dart:convert), `team_logger` 0.3.0 / `logger_builder` 0.3.1, `package:clock` (тестируемое время), `flutter_test` для тестов (pure Dart tests).

## Global Constraints

- Спека: `docs/specs/2026-07-22-session-file-logs.md` — источник требований.
- Дефолты: maxSessionBytes 2 MiB, chunksPerSession 4, maxSessions 10, maxAge 7 дней, maxTotalBytes 20 MiB, maxRecordBytes 32 KiB.
- Никаких исключений наружу из пути записи; self-disable после 5 подряд IO-ошибок.
- Время в файлах — UTC ISO 8601; возраст сессии — из имени файла.
- Коммиты атомарные, без AI-атрибуции. Комментарии в коде компактные, по-русски не обязательно — как в соседнем коде пакета (там русский в UI-модулях, core — английский; в новом коде — английский).
- Прогон тестов: `fvm flutter test <file>` из корня репо.

---

### Task 1: FileLogStorageOptions

**Files:**
- Create: `lib/src/file_storage/file_log_storage_options.dart`
- Test: `test/file_storage/file_log_storage_options_test.dart`

**Interfaces:**
- Produces: `FileLogStorageOptions({int maxSessionBytes, int chunksPerSession, int maxSessions, Duration maxAge, int maxTotalBytes, int maxRecordBytes, int minLevel, bool Function(Log)? recordFilter, void Function(Object, StackTrace)? onInternalError})`, getter `int chunkBytes => maxSessionBytes ~/ chunksPerSession`.

- [ ] **Step 1: failing test** — дефолты и `chunkBytes`, `assert` на кривые значения (`chunksPerSession < 1`, `maxRecordBytes > chunkBytes`).
- [ ] **Step 2: run** `fvm flutter test test/file_storage/file_log_storage_options_test.dart` → FAIL (нет класса).
- [ ] **Step 3: implement** const-класс с полями из спеки и `assert`-ами.
- [ ] **Step 4: run** → PASS.
- [ ] **Step 5: commit** `feat(file-storage): options for session file logs`

### Task 2: SessionFileName (naming + parse)

**Files:**
- Create: `lib/src/file_storage/session_file_name.dart`
- Test: `test/file_storage/session_file_name_test.dart`

**Interfaces:**
- Produces:
  - `String sessionIdFrom(DateTime utcStart, String rand4)` → `20260722T104501-a3f2`
  - `String chunkFileName(String sessionId, int part)` → `tlog_20260722T104501-a3f2_p03.jsonl`
  - `SessionFileInfo? parseFileName(String name)` → `{String sessionId, DateTime startedAt (UTC), int part}`; `null` на чужих файлах.

- [ ] **Step 1: failing test** — roundtrip build→parse, UTC parse, `null` на мусорных именах, сортировка по `startedAt`.
- [ ] **Step 2: run** → FAIL.
- [ ] **Step 3: implement** — формат/regexp, без DateFormat (руками, zero deps).
- [ ] **Step 4: run** → PASS.
- [ ] **Step 5: commit** `feat(file-storage): session file naming and parsing`

### Task 3: LogRecordEncoder (Log → JSONL, truncation)

**Files:**
- Create: `lib/src/file_storage/log_record_encoder.dart`
- Test: `test/file_storage/log_record_encoder_test.dart`

**Interfaces:**
- Consumes: `FileLogStorageOptions.maxRecordBytes`.
- Produces:
  - `String encodeSessionHeader({required String sessionId, required DateTime startedAt, required Map<String, Object?> meta})` — одна строка с `\n`.
  - `String encodeLog(Log log, {required int maxRecordBytes})` — одна строка с `\n`.

- [ ] **Step 1: failing tests**
  - header: `kind=session`, `schema=1`, ISO UTC `startedAt`, meta как есть;
  - лог: поля `ts/seq/lvl/lvlName/path/msg`, `trace`/`tags`/`data`/`err`/`stack` только когда есть;
  - несериализуемый `data` → поэлементный fallback `toString()` (объект с Socket внутри не роняет encode);
  - превышение `maxRecordBytes` → усечение stack → data → msg, `"trunc":true`, итог ≤ лимита.
- [ ] **Step 2: run** → FAIL.
- [ ] **Step 3: implement** — `jsonEncode(value, toEncodable: (o) => o.toString())`; усечение по байтам UTF-8 с маркером `…[truncated]`.
- [ ] **Step 4: run** → PASS.
- [ ] **Step 5: commit** `feat(file-storage): JSONL record encoder with size cap`

### Task 4: Retention (чистка каталога при старте)

**Files:**
- Create: `lib/src/file_storage/retention.dart`
- Test: `test/file_storage/retention_test.dart`

**Interfaces:**
- Consumes: `parseFileName`, options.
- Produces: `Future<void> applyRetention(Directory dir, FileLogStorageOptions options, {required String currentSessionId, required DateTime now})` — группирует файлы по sessionId, удаляет сессии: старше `maxAge` → сверх `maxSessions` (старейшие) → сверх `maxTotalBytes` (старейшие). Текущую сессию не трогает, чужие файлы не трогает, ошибки удаления глотает.

- [ ] **Step 1: failing tests** (temp dir, файлы с ручными именами):
  - старше maxAge удалена целиком (все чанки);
  - 12 сессий → остаются 10 новейших + текущая;
  - перебор maxTotalBytes → старейшие удаляются до лимита;
  - текущая сессия неприкосновенна даже если старая/большая;
  - посторонний файл `foo.txt` не тронут.
- [ ] **Step 2: run** → FAIL.
- [ ] **Step 3: implement**.
- [ ] **Step 4: run** → PASS.
- [ ] **Step 5: commit** `feat(file-storage): startup retention for session files`

### Task 5: FileLogStorage (ядро: запись, ротация, self-disable)

**Files:**
- Create: `lib/src/file_storage/file_log_storage.dart`
- Test: `test/file_storage/file_log_storage_test.dart`

**Interfaces:**
- Consumes: всё выше.
- Produces:
  ```dart
  final class FileLogStorage extends AsyncPublisherBase<Log> {
    FileLogStorage({
      required Directory directory,
      FileLogStorageOptions options = const FileLogStorageOptions(),
      Map<String, Object?> sessionMeta = const {},
    });
    String get sessionId;
    Future<List<File>> collectFiles(); // Task 6
    Future<void> close();
  }
  ```
  Поведение `handle(Log)`:
  - первая запись лениво инициализирует: mkdir, retention, открытие чанка `p00`, header;
  - `minLevel`/`recordFilter` отсекают до encode;
  - encode → `RandomAccessFile.writeString`; `flush()` (fsync) при `level >= LogLevels.error`;
  - размер чанка ≥ `chunkBytes` → закрыть, открыть `p<next>` c header; чанков > `chunksPerSession` → удалить старейший чанк сессии;
  - IO-ошибка → счётчик, 5 подряд → disabled навсегда + один вызов `onInternalError`; успешная запись сбрасывает счётчик.

- [ ] **Step 1: failing tests** (temp dir, реальный Logger с publisher = storage, `await storage.flush()` между проверками):
  - файл создан, первая строка — header, дальше — записи;
  - error-запись доступна на диске сразу после flush;
  - маленький `maxSessionBytes` (например 4 KiB / 4 чанка) + спам → чанков ≤ 4, старейший (`p00`) удалён, в живых чанках есть последние записи;
  - каждый чанк начинается с header;
  - каталог, удалённый после init (или readonly) → нет исключений, после 5 записей срабатывает `onInternalError` ровно один раз;
  - `recordFilter`/`minLevel` отфильтровывают.
- [ ] **Step 2: run** → FAIL.
- [ ] **Step 3: implement**.
- [ ] **Step 4: run** → PASS. Также `fvm flutter analyze` чисто.
- [ ] **Step 5: commit** `feat(file-storage): FileLogStorage publisher with chunk rotation`

### Task 6: collectFiles() + экспорт из пакета

**Files:**
- Modify: `lib/src/file_storage/file_log_storage.dart`
- Modify: `lib/flutter_team_logger.dart` (export `src/file_storage/...`)
- Test: `test/file_storage/collect_files_test.dart`

**Interfaces:**
- Produces: `Future<List<File>> collectFiles()` — `await flush()` (дренаж очереди + fsync), скан каталога через `parseFileName`, сортировка: сессии новые→старые, внутри сессии чанки по возрастанию part.

- [ ] **Step 1: failing tests:**
  - возвращает файлы текущей и прошлых сессий в заданном порядке;
  - запись, сделанная прямо перед `collectFiles()`, уже в файле;
  - чужие файлы каталога не попадают.
- [ ] **Step 2: run** → FAIL.
- [ ] **Step 3: implement + export.**
- [ ] **Step 4: run** → PASS.
- [ ] **Step 5: commit** `feat(file-storage): collectFiles() for support export`

### Task 7: Example app — Send logs

**Files:**
- Modify: `example/lib/logging.dart` (подключить `FileLogStorage` в MultiPublisher, каталог `Directory.systemTemp`-based для desktop-примера)
- Modify: `example/lib/home.dart` (кнопка «Send logs»: `collectFiles()` → диалог со списком имён и размеров)

**Interfaces:**
- Consumes: `FileLogStorage`, `collectFiles()`.

- [ ] **Step 1: wire** storage в `logging.dart`.
- [ ] **Step 2: add button** в `home.dart`.
- [ ] **Step 3: run** `cd example && fvm flutter build macos --debug` (или `fvm flutter analyze`) → компилируется.
- [ ] **Step 4: commit** `feat(example): send logs button over FileLogStorage`

### Task 8: Docs

**Files:**
- Modify: `README.md` (раздел Features/Usage: подключение, лимиты, collectFiles, PII-нота)
- Modify: `CHANGELOG.md` (0.4.0)
- Modify: `pubspec.yaml` (version 0.4.0)

- [ ] **Step 1: write docs** — компактно, через humanizer skill.
- [ ] **Step 2: commit** `docs: file-based session logs`

## Self-Review

- Spec coverage: формат (T3), имена/сессии (T2), лимиты+ротация (T1, T5), retention (T4), flush-политика (T5), ошибки записи (T5), collectFiles (T6), PII-фильтр (T1 options + T5), example (T7), докуметация (T8). Ок.
- Types: `FileLogStorageOptions.recordFilter` используется в T5; `parseFileName` в T4/T6 — имена совпадают.
- Placeholders: шаги без полного кода осознанно компактны (маленькие чистые модули, сигнатуры зафиксированы в Interfaces; исполнитель — эта же сессия).
