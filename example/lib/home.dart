// ignore_for_file: avoid_print

import 'package:flutter/material.dart';
import 'package:flutter_team_logger/flutter_team_logger.dart';
import 'package:share_plus/share_plus.dart';

import 'logging.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _log = log.copyWith(name: 'logs');

  Future<void> _sendLogs() async {
    // Reference support flow: one immutable zip snapshot into the OS
    // share sheet (mail, messenger, support chat).
    final zip = await fileLogStorage.exportArchive();
    if (!mounted || zip == null) return;

    final box = context.findRenderObject() as RenderBox?;
    await Share.shareXFiles(
      [XFile(zip.path)],
      subject: 'App logs',
      // Required by the iPad/macOS share popover.
      sharePositionOrigin:
          box == null ? null : box.localToGlobal(Offset.zero) & box.size,
    );
  }

  Future<void> _showLogs() async {
    await Navigator.push(
      context,
      MaterialPageRoute<void>(
        builder: (_) => Logs(
          theme: uiTheme,
          logStorage: logStorage,
          onPaused: () => _log.w('[b]paused[/b]'),
          onResumed: () => _log.w('[b]resumed[/b]'),
          onCleared: () => _log.w('[b]cleared[/b]'),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(
          backgroundColor: Theme.of(context).colorScheme.inversePrimary,
          title: const Text('Logs demo'),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            spacing: 16,
            children: [
              ElevatedButton(
                onPressed: _showLogs,
                child: StreamBuilder<void>(
                  stream: logStorage.onChanged,
                  builder: (_, __) => Text('Logs (${logStorage.count})'),
                ),
              ),
              ElevatedButton(
                onPressed: _sendLogs,
                child: const Text('Send logs'),
              ),
            ],
          ),
        ),
      );
}
