import 'package:flutter/widgets.dart';
import 'package:flutter_team_logger/flutter_team_logger.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:team_logger/team_logger.dart';

class _FlushSpy implements HasFlush {
  int calls = 0;

  @override
  Future<void> flush() async => calls++;
}

void main() {
  test('flushes on paused and detached, ignores the rest', () {
    final spy = _FlushSpy();
    final observer = FileLogFlushObserver(spy)
      ..didChangeAppLifecycleState(AppLifecycleState.resumed)
      ..didChangeAppLifecycleState(AppLifecycleState.inactive);
    expect(spy.calls, 0);

    observer
      ..didChangeAppLifecycleState(AppLifecycleState.paused)
      ..didChangeAppLifecycleState(AppLifecycleState.detached);
    expect(spy.calls, 2);
  });

  testWidgets('attach/detach registers with WidgetsBinding', (tester) async {
    final spy = _FlushSpy();
    final observer = FileLogFlushObserver(spy)..attach();

    tester.binding.handleAppLifecycleStateChanged(AppLifecycleState.paused);
    expect(spy.calls, 1);

    observer.detach();
    tester.binding.handleAppLifecycleStateChanged(AppLifecycleState.paused);
    expect(spy.calls, 1);
  });
}
