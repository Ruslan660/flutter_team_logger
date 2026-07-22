// Mobile entrypoint: the desktop one pulls in window_manager, which has
// no iOS/Android implementation. Logging setup and UI are shared.
import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_team_logger/flutter_team_logger.dart';
import 'package:team_logger/team_logger.dart';

import 'app.dart';
import 'logging.dart';

const _timerPeriod = Duration(milliseconds: 500);

Future<void> main() async {
  log.level = LogLevels.all;

  Object data(Timer timer) => {
        'tick': timer.tick,
        'now': DateTime.now(),
      };

  final timerLog = log.copyWith(name: 'timer');
  Timer.periodic(_timerPeriod, (timer) {
    final traceId = TraceId.auto('timer_d');
    timerLog.d('timer debug', data: () => data(timer), traceId: traceId);
    timerLog.i('timer info', data: () => data(timer), traceId: traceId);
    if (timer.tick % 5 == 0) {
      timerLog.e(
        'timer error',
        data: () => data(timer),
        error: Exception('test'),
        traceId: traceId,
      );
    }
  });

  WidgetsFlutterBinding.ensureInitialized();
  FileLogFlushObserver(fileLogStorage).attach();

  runApp(const App());
}
