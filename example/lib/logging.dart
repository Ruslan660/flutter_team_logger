import 'dart:io';

import 'package:ansi_escape_codes/style.dart' as ansi;
import 'package:team_logger/team_logger.dart';
import 'package:team_logger/team_logger_io.dart';

final theme = LogMainTheme.defaultActiveTheme;
final uiTheme = theme.copyWith(
  tagsStyle: ansi.gray8,
);

final logStorage = LogStorage(maxCount: 1000);

final fileLogStorage = FileLogStorage(
  directory: Directory('${Directory.systemTemp.path}/team_logger_example'),
  sessionMeta: const {'app': 'example', 'version': '0.3.0'},
);

final log = Logger('app')
  ..publisher = MultiPublisher([
    // ConsoleLogPrinter(
    //   theme: theme,
    //   rows: const [
    //     LogRow(
    //       maxLength: 140,
    //       children: [
    //         LogSequenceNum(),
    //         LogLevelName.short(),
    //         LogTime.onlyTime(),
    //         LogPath(),
    //         LogTraceId(),
    //         LogMessage(
    //           controlledPackages: {
    //             'team_logger',
    //             'flutter_team_logger',
    //           },
    //         ),
    //       ],
    //       tail: [
    //         LogTags(),
    //       ],
    //     ),
    //   ],
    // ),
    logStorage,
    fileLogStorage,
  ]);
