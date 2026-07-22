# flutter_team_logger

Flutter widgets for displaying logs from [team_logger](https://pub.dev/packages/team_logger) library in the UI.

## Features

- `Logs` — a screen that renders a `LogStorage` with filtering, pause
  and auto-scroll.
- `FileLogFlushObserver` — companion for `FileLogStorage` from
  `package:team_logger/team_logger_io.dart`. Subscribes to app
  lifecycle and flushes buffered records to disk when the app goes to
  background or is about to die.

## Session logs on disk

The storage itself lives in `team_logger` (`doc/file_storage.md` there
covers limits, rotation and the failure policy). This package adds the
Flutter glue:

```dart
final fileLogStorage = FileLogStorage(directory: dir);
FileLogFlushObserver(fileLogStorage).attach();
```

The example app shows the full support flow: a "Send logs" button calls
`exportArchive()` and hands the zip snapshot to `share_plus`.

## Usage

See `example/`.
