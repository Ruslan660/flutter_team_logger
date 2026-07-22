import 'dart:async';

import 'package:flutter/widgets.dart';
import 'package:team_logger/team_logger.dart';

/// Flushes a log publisher (typically `FileLogStorage`) when the app
/// goes to background or is about to die — the last chance to get
/// buffered records on disk before a possible kill.
///
/// ```dart
/// final observer = FileLogFlushObserver(fileLogStorage)..attach();
/// ```
final class FileLogFlushObserver with WidgetsBindingObserver {
  final HasFlush storage;

  FileLogFlushObserver(this.storage);

  void attach() => WidgetsBinding.instance.addObserver(this);

  void detach() => WidgetsBinding.instance.removeObserver(this);

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.paused ||
        state == AppLifecycleState.detached) {
      unawaited(storage.flush());
    }
  }
}
