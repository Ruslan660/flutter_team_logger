# AI-workshop deck, Tez Taxi app style (Darb palette: light surfaces,
# blue accent, yellow attention chips). Audience: all technical staff.
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SURFACE = RGBColor(0xF6, 0xF6, 0xF6)
SURFACE2 = RGBColor(0xF0, 0xF1, 0xF2)
TEXT = RGBColor(0x0F, 0x0F, 0x0F)
DIM = RGBColor(0x6E, 0x73, 0x79)
ACCENT = RGBColor(0x40, 0x6F, 0xE5)   # brand-accent
CYAN = RGBColor(0x39, 0xCA, 0xEA)     # brand-cyan
YELLOW = RGBColor(0xFF, 0xCE, 0x1F)   # status-attention
ERROR = RGBColor(0xF5, 0x41, 0x31)    # status-error
VIOLET = RGBColor(0x44, 0x1C, 0xB7)
SANS = "Helvetica Neue"
MONO = "Menlo"

W, H = Inches(13.333), Inches(7.5)
prs = Presentation()
prs.slide_width, prs.slide_height = W, H
BLANK = prs.slide_layouts[6]
TOTAL = 18


def no_line(shape):
    shape.line.fill.background()


def rounded(s, left, top, width, height, fill, radius=0.12):
    shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                             Inches(left), Inches(top),
                             Inches(width), Inches(height))
    shp.adjustments[0] = radius
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    no_line(shp)
    shp.shadow.inherit = False
    return shp


def slide_base(n, chip_text, chip_color=ACCENT):
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = WHITE
    # section chip, app-style pill
    pill = rounded(s, 0.7, 0.45, 0.42 + 0.135 * len(chip_text), 0.42,
                   chip_color, radius=0.5)
    tf = pill.text_frame
    tf.word_wrap = False
    tf.margin_left = Inches(0.1); tf.margin_right = Inches(0.1)
    tf.margin_top = 0; tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = chip_text
    r.font.name = SANS; r.font.size = Pt(13); r.font.bold = True
    r.font.color.rgb = TEXT if chip_color == YELLOW else WHITE
    # footer
    fb = s.shapes.add_textbox(Inches(0.7), Inches(7.05), Inches(12), Inches(0.35))
    p = fb.text_frame.paragraphs[0]
    r = p.add_run(); r.text = "tez.taxi · AI workshop"
    r.font.name = SANS; r.font.size = Pt(10); r.font.color.rgb = DIM
    r = p.add_run(); r.text = "    %d / %d" % (n, TOTAL)
    r.font.name = SANS; r.font.size = Pt(10); r.font.color.rgb = DIM
    return s


def title(s, text, size=34, top=1.15, color=TEXT, width=12.0):
    tb = s.shapes.add_textbox(Inches(0.7), Inches(top), Inches(width), Inches(1.0))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = text
    r.font.name = SANS; r.font.size = Pt(size); r.font.bold = True
    r.font.color.rgb = color
    return tb


def paragraphs(s, texts, top=2.25, size=17, width=11.9, left=0.7, color=TEXT):
    tb = s.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(4.5))
    tf = tb.text_frame; tf.word_wrap = True
    first = True
    for t in texts:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(12); p.line_spacing = 1.3
        r = p.add_run(); r.text = t
        r.font.name = SANS; r.font.size = Pt(size); r.font.color.rgb = color
    return tb


def bullets(s, items, top=2.25, left=0.7, width=11.9, size=16, gap=10,
            marker_color=ACCENT):
    tb = s.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(4.6))
    tf = tb.text_frame; tf.word_wrap = True
    first = True
    for head, rest in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(gap); p.line_spacing = 1.25
        r = p.add_run(); r.text = "•  "
        r.font.name = SANS; r.font.size = Pt(size); r.font.bold = True
        r.font.color.rgb = marker_color
        if head:
            r = p.add_run(); r.text = head + " "
            r.font.name = SANS; r.font.size = Pt(size); r.font.bold = True
            r.font.color.rgb = TEXT
        if rest:
            r = p.add_run(); r.text = rest
            r.font.name = SANS; r.font.size = Pt(size); r.font.color.rgb = DIM
    return tb


def card(s, left, top, width, height, head, body, head_color=ACCENT,
         head_size=16, body_size=13.5):
    rounded(s, left, top, width, height, SURFACE)
    tb = s.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.18),
                              Inches(width - 0.5), Inches(height - 0.36))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.space_after = Pt(6)
    r = p.add_run(); r.text = head
    r.font.name = SANS; r.font.size = Pt(head_size); r.font.bold = True
    r.font.color.rgb = head_color
    for line in body if isinstance(body, list) else [body]:
        p = tf.add_paragraph(); p.space_after = Pt(4); p.line_spacing = 1.2
        r = p.add_run(); r.text = line
        r.font.name = SANS; r.font.size = Pt(body_size); r.font.color.rgb = TEXT


def table(s, rows, top=2.15, col_w=(3.3, 8.6), size=13.5, header=("", ""),
          left=0.7):
    n = len(rows) + (1 if header[0] else 0)
    shape = s.shapes.add_table(n, 2, Inches(left), Inches(top),
                               Inches(col_w[0] + col_w[1]), Inches(0.5 * n))
    t = shape.table
    tbl = t._tbl
    for el in tbl.findall(qn('a:tblPr')):
        el.set('bandRow', '0'); el.set('firstRow', '0')
    t.columns[0].width = Inches(col_w[0]); t.columns[1].width = Inches(col_w[1])
    data = ([header] if header[0] else []) + rows
    for i, (a, b) in enumerate(data):
        is_header = header[0] and i == 0
        for j, text in enumerate((a, b)):
            cell = t.cell(i, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = SURFACE2 if is_header else (
                WHITE if i % 2 == (1 if header[0] else 0) else SURFACE)
            cell.vertical_anchor = MSO_ANCHOR.TOP
            cell.margin_left = Inches(0.14); cell.margin_right = Inches(0.14)
            cell.margin_top = Inches(0.08); cell.margin_bottom = Inches(0.08)
            p = cell.text_frame.paragraphs[0]
            r = p.add_run(); r.text = text
            r.font.name = SANS
            r.font.size = Pt(size)
            r.font.bold = (j == 0 and not is_header) or is_header
            r.font.color.rgb = DIM if is_header else (
                ACCENT if j == 0 else TEXT)
            cell.text_frame.word_wrap = True
    return shape


# ------------------------------------------------------------------ 1: title
s = slide_base(1, "workshop", ACCENT)
rounded(s, 0.7, 1.9, 7.2, 0.16, YELLOW, radius=0.5)
tb = s.shapes.add_textbox(Inches(0.7), Inches(2.3), Inches(12), Inches(2.2))
tf = tb.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]
r = p.add_run(); r.text = "AI-инструменты\nв ежедневной работе"
r.font.name = SANS; r.font.size = Pt(50); r.font.bold = True
r.font.color.rgb = TEXT
tb = s.shapes.add_textbox(Inches(0.7), Inches(4.75), Inches(11), Inches(1.1))
tf = tb.text_frame; tf.word_wrap = True
r = tf.paragraphs[0].add_run()
r.text = ("Как устроена работа с Claude Code: правила проекта, skills, "
          "агенты — и одна фича, доведённая за вечер от идеи до двух pull request.")
r.font.name = SANS; r.font.size = Pt(18); r.font.color.rgb = DIM
tb = s.shapes.add_textbox(Inches(0.7), Inches(6.2), Inches(10), Inches(0.4))
r = tb.text_frame.paragraphs[0].add_run()
r.text = "Ruslan · Tez Taxi mobile · 23.07.2026"
r.font.name = SANS; r.font.size = Pt(14); r.font.color.rgb = ACCENT
r.font.bold = True

# ------------------------------------------------------------------ 2: why
s = slide_base(2, "зачем", ACCENT)
title(s, "Это не только про разработку")
paragraphs(s, [
    "AI-агент — не автодополнение кода. Это исполнитель, которому даёшь задачу, "
    "а он сам работает с терминалом, файлами и сервисами: собирает приложение, "
    "воспроизводит баг, разбирает логи, готовит merge request.",
], top=2.15, size=17)
card(s, 0.7, 3.5, 3.85, 2.5, "Разработчику",
     ["merge request и pipeline", "миграции и рефакторинг",
      "разбор чужого кода"], ACCENT)
card(s, 4.75, 3.5, 3.85, 2.5, "QA-инженеру",
     ["воспроизведение багов на устройстве", "разбор логов сессии",
      "фейковые заказы на тестовом стенде"], CYAN)
card(s, 8.8, 3.5, 3.85, 2.5, "Команде",
     ["единые правила в репозитории", "общая память о решениях",
      "меньше устных договорённостей"], VIOLET)

# ------------------------------------------------------------------ 3: context
s = slide_base(3, "основы", ACCENT)
title(s, "Context window: рабочий стол агента")
paragraphs(s, [
    "У модели нет постоянной памяти. Есть context window — примерно 200 тысяч "
    "tokens (условно, сотни страниц текста). Туда помещается всё, что агент "
    "«видит»: инструкции проекта, история диалога, вывод каждой команды.",
    "Чего нет в окне — того для агента не существует. Когда окно переполняется, "
    "старая часть сжимается в краткий пересказ, и детали теряются.",
    "Вывод: объём окна — это бюджет. Его тратят на задачу, а не на лишний "
    "вывод команд и случайные файлы.",
], size=17)

# ------------------------------------------------------------------ 4: rules
s = slide_base(4, "основы", ACCENT)
title(s, "Правила проекта: CLAUDE.md и AGENTS.md")
paragraphs(s, [
    "Это файлы в репозитории, которые агент читает в начале каждой сессии — "
    "свод правил проекта. У нас он один для двух агентов: Claude Code и Codex.",
], top=2.1, size=16)
table(s, [
    ("toolchain", "какие версии Flutter и Java, как собирать, какие команды запускать"),
    ("запреты", "например: commit и push только по явной команде человека"),
    ("дорогие ошибки", "проверка ключей карт перед сборкой — после реального инцидента"),
    ("навигация", "ссылки на документы: «для задач про UI читай DESIGN.md»"),
], top=3.05, header=("что лежит", "пример"))
paragraphs(s, [
    "Принцип: в постоянно загружаемом файле — только правила и ссылки. Большие "
    "документы агент открывает сам, когда задача их касается.",
], top=5.75, size=15)

# ------------------------------------------------------------------ 5: memory
s = slide_base(5, "основы", ACCENT)
title(s, "Память между сессиями — обычные файлы")
table(s, [
    ("WORKLOG.md", "журнал: что сделано за сессию, что осталось, что важно знать следующему"),
    ("HANDOFF-*.md", "передача незаконченной задачи — как передача смены: выводы, а не переписка"),
    ("memory/", "проверенные факты, по файлу на каждый: «в CI авторизация настроена так-то»"),
    ("docs/adr/", "принятые архитектурные решения и их причины"),
], top=2.2, header=("файл", "роль"))
paragraphs(s, [
    "Всё это markdown в git. Читают три стороны: Claude, Codex и люди. "
    "Новая сессия начинает с выводов прошлой, а не с чистого листа.",
], top=5.15, size=16)

# ------------------------------------------------------------------ 6: skills
s = slide_base(6, "skills", ACCENT)
title(s, "Skill: инструкция, которая запускается сама")
paragraphs(s, [
    "Skill — это файл с описанием задачи и пошаговым порядком действий. Агент "
    "постоянно видит только короткое описание; полный текст читает, когда "
    "задача совпала. Эти skills лежат прямо в репозитории проекта:",
], top=2.05, size=15.5)
table(s, [
    ("run-app-ios", "запуск client или driver на iOS-симуляторе, включая настройку ключей карт"),
    ("teztaxi-debug-harness", "воспроизведение багов: фейковый заказ, логи, управление устройством"),
    ("teztaxi-gitlab", "merge request, статус pipeline, merge — через glab"),
    ("teztaxi-jira", "работа с задачами в Jira: посмотреть, перевести статус"),
    ("project-atlas", "навигация по архитектуре: какой документ читать под какую задачу"),
], top=3.15, header=("skill в репозитории", "что делает"))

# ------------------------------------------------------------------ 7: skill birth
s = slide_base(7, "skills", ACCENT)
title(s, "Как появляется skill")
bullets(s, [
    ("1.", "Прошёл рабочий путь руками. Второй раз. На третий — это кандидат в skill"),
    ("2.", "Попросил агента оформить прошедшую сессию в инструкцию: он помнит все команды и ошибки точнее человека"),
    ("3.", "Поправил руками два места: условие запуска и список «чего не делать»"),
    ("4.", "Положил в git. Дальше инструкция уточняется по мере новых случаев"),
], top=2.3, size=17, gap=14)
paragraphs(s, [
    "Хороший skill — как инструкция по сборке: точное условие запуска, конкретные "
    "команды, известные ошибки. Плохой — длинная статья без конкретики.",
], top=5.3, size=16)

# ------------------------------------------------------------------ 8: rtk
s = slide_base(8, "инструменты", YELLOW)
title(s, "rtk — экономия context window")
paragraphs(s, [
    "Проблема: вывод команд (git, поиск по коду, списки файлов) занимает "
    "огромную часть окна агента. Одна длинная сессия — и место кончилось.",
    "Решение: rtk перехватывает эти команды и отдаёт агенту сжатый вывод "
    "с тем же смыслом. Работает через hook — правило, которое срабатывает "
    "автоматически, агент даже не знает о подмене.",
], top=2.1, size=16)
card(s, 0.7, 4.35, 12.0, 1.5, "Эффект",
     ["Экономия 60–90% объёма на типовых командах. Это буквально в разы больше "
      "полезной работы в одной сессии без потери информации."], ACCENT)

# ------------------------------------------------------------------ 9: superpowers
s = slide_base(9, "инструменты", YELLOW)
title(s, "superpowers — дисциплина процесса")
paragraphs(s, [
    "Набор процессных skills, которые не дают агенту «сразу писать код». "
    "Главное правило — жёсткий шлагбаум: сначала обсуждение и спецификация, "
    "одобрение человека, потом реализация.",
], top=2.1, size=16)
bullets(s, [
    ("brainstorming:", "уточняющие вопросы и варианты решения до строчки кода"),
    ("test-driven development:", "сначала тест, который падает, потом код, который его чинит"),
    ("планы:", "реализация разбивается на маленькие проверяемые шаги с отдельными commit"),
], top=3.5, size=16, gap=12)
paragraphs(s, [
    "Смысл: у агента появляется рабочий процесс, как у аккуратного инженера.",
], top=5.6, size=16)

# ------------------------------------------------------------------ 10: codex
s = slide_base(10, "инструменты", YELLOW)
title(s, "codex — вторая модель для проверки")
paragraphs(s, [
    "Плагин-мост к Codex (модель OpenAI). Claude пишет — Codex независимо "
    "проверяет: спецификацию, код, готовый merge request. Запускается фоновой "
    "задачей, результат приходит отчётом.",
    "Зачем два разных AI: у разных моделей разные слепые зоны. То, что одна "
    "уверенно пропустит, другая заметит.",
], top=2.1, size=16)
card(s, 0.7, 4.5, 12.0, 1.7, "Вчерашний пример",
     ["Codex нашёл в коде Claude два критических дефекта: небезопасный "
      "одновременный доступ к файлу и выгрузку файлов, которые могли быть "
      "удалены во время отправки. Оба исправлены до попадания в main."], ERROR)

# ------------------------------------------------------------------ 11: mcp vs skill
s = slide_base(11, "инструменты", YELLOW)
title(s, "MCP или skill: подключение или знание")
card(s, 0.7, 2.2, 5.9, 3.3, "MCP-сервер = доступ к системе",
     ["живое подключение с набором операций",
      "пример: dcm — статический анализ кода",
      "пример: context7 — свежая документация библиотек",
      "нужен, когда агенту требуется API,",
      "до которого иначе не дотянуться"], ACCENT, body_size=14)
card(s, 6.9, 2.2, 5.75, 3.3, "Skill = знание процесса",
     ["текстовая инструкция в git",
      "ничего не запущено — нечему ломаться",
      "проходит code review как обычный код",
      "дешевле в поддержке",
      "покрывает большинство задач"], CYAN, body_size=14)
paragraphs(s, [
    "Практическое правило: нужен доступ к внешней системе — MCP; нужен порядок "
    "действий — skill. Если сомневаетесь, начните со skill.",
], top=5.75, size=16)

# ------------------------------------------------------------------ 12: agents
s = slide_base(12, "инструменты", YELLOW)
title(s, "Субагенты: отдельные исполнители под подзадачи")
paragraphs(s, [
    "Субагент — отдельный агент со своим чистым context window. Главная сессия "
    "держит задачу целиком и раздаёт подзадачи: «изучи, как устроен этот "
    "модуль», «подготовь план». Обратно приходит короткий отчёт, а не тысячи "
    "строк прочитанных файлов.",
    "Несколько независимых субагентов работают параллельно — три исследования "
    "по времени стоят как одно.",
    "Правило: субагенту делегируют сбор информации и черновую работу. Решения "
    "принимает главная сессия, у которой есть весь контекст задачи.",
], size=16)

# ------------------------------------------------------------------ 13: sdd
s = slide_base(13, "подход", VIOLET)
title(s, "SDD — Spec-Driven Development")
paragraphs(s, [
    "Подход: сначала специфицируем, что и с какими ограничениями делаем, "
    "и только потом пишем код.",
], top=2.05, size=16)
steps = [
    ("1. Спека", "цель, ограничения,\nграничные случаи", ACCENT),
    ("2. Ревью", "человек + вторая\nмодель, до кода", CYAN),
    ("3. План", "маленькие шаги,\nкаждый проверяем", VIOLET),
    ("4. Код", "по плану, тест\nперед реализацией", ACCENT),
    ("5. Проверка", "тесты, запуск,\nповторное ревью", CYAN),
]
x = 0.7
for head, body, color in steps:
    card(s, x, 3.0, 2.32, 1.9, head, body.split("\n"), color,
         head_size=15, body_size=12.5)
    x += 2.42
paragraphs(s, [
    "Экономика простая: спецификация на две страницы правится за минуты, "
    "код — за часы. Ошибка, пойманная до реализации, самая дешёвая.",
], top=5.35, size=16)

# ------------------------------------------------------------------ 14: case
s = slide_base(14, "кейс", CYAN)
title(s, "Кейс: логи сессий для поддержки")
paragraphs(s, [
    "Задача: приложение хранит логи каждой сессии на устройстве; они переживают "
    "сбой; пользователь отправляет их в поддержку одной кнопкой. Один вечер, "
    "полный цикл по SDD:",
], top=2.05, size=16)
table(s, [
    ("18:05", "спецификация: ограничения хранения, отказоустойчивость, граничные случаи"),
    ("18:20", "Codex проверяет спецификацию, параллельно пишется план"),
    ("18:30", "реализация по плану: каждый модуль начинается с падающего теста"),
    ("19:00", "обратная связь человека — спецификация и код скорректированы"),
    ("19:40", "Codex проверяет код: два критических дефекта, исправлены"),
    ("20:30", "два pull request: ядро и Flutter-обвязка, 30+ тестов"),
], top=3.1, col_w=(1.4, 10.5), header=("время", "шаг"))

# ------------------------------------------------------------------ 15: decisions
s = slide_base(15, "кейс", CYAN)
title(s, "Главные решения из спецификации")
table(s, [
    ("срок жизни логов", "7 дней и не больше 20 MiB на всё: старые сессии удаляются автоматически"),
    ("рост файла", "сессия пишется частями; при переполнении удаляется самая старая часть — конец сессии важнее начала, потому что сбой обычно в конце"),
    ("сбой при записи", "формат «одна запись — одна строка»: при аварии страдает максимум последняя строка"),
    ("диск переполнен", "после пяти неудач подряд запись отключается; приложение не падает никогда"),
    ("отправка", "снимок всех логов одним zip-архивом — его безопасно отправлять, пока приложение продолжает писать"),
], top=2.2, col_w=(2.9, 9.0), header=("вопрос", "решение"))

# ------------------------------------------------------------------ 16: review value
s = slide_base(16, "кейс", CYAN)
title(s, "Что дало ревью")
card(s, 0.7, 2.25, 5.9, 3.2, "Человек",
     ["«лимит на количество сессий не нужен —",
      "хватит срока и объёма» — минус сущность",
      "",
      "«добавьте отправку архивом» — плюс",
      "функция, которой не было в первой версии"], ACCENT, body_size=14)
card(s, 6.9, 2.25, 5.75, 3.2, "Codex (вторая модель)",
     ["небезопасный одновременный доступ",
      "к файлу из разных операций",
      "",
      "отправка «живых» файлов, которые",
      "могли быть удалены в этот момент"], ERROR, body_size=14)
paragraphs(s, [
    "Разные ревьюеры находят разное: человек проверяет смысл и продуктовую "
    "логику, вторая модель — техническую корректность. Оба раунда до main.",
], top=5.7, size=16)

# ------------------------------------------------------------------ 17: start
s = slide_base(17, "старт", ACCENT)
title(s, "С чего начать команде")
bullets(s, [
    ("1. CLAUDE.md в репозитории.", "Правила сборки и запреты. Час работы — и любой агент у любого члена команды играет по правилам проекта"),
    ("2. Один skill на самую частую рутину.", "Разработчику — merge request; QA — воспроизведение бага на устройстве"),
    ("3. WORKLOG.md.", "Пять строк в конце сессии — завтра продолжаешь с места, а не сначала"),
    ("4. Ревью второй моделью", "для крупных фич — когда первые три пункта приживутся"),
], top=2.3, size=16.5, gap=14)
paragraphs(s, [
    "Не заводите всё сразу: каждый инструмент здесь появился как ответ на "
    "конкретную проблему, а не по каталогу.",
], top=5.5, size=16)

# ------------------------------------------------------------------ 18: QA
s = slide_base(18, "вопросы", ACCENT)
rounded(s, 0.7, 2.0, 4.5, 0.16, YELLOW, radius=0.5)
tb = s.shapes.add_textbox(Inches(0.7), Inches(2.4), Inches(12), Inches(1.3))
r = tb.text_frame.paragraphs[0].add_run()
r.text = "Вопросы"
r.font.name = SANS; r.font.size = Pt(50); r.font.bold = True
r.font.color.rgb = TEXT
bullets(s, [
    ("Ядро фичи:", "github.com/Ruslan660/team_logger — pull request #1"),
    ("Flutter-часть и спецификация:", "github.com/Ruslan660/flutter_team_logger — pull request #1"),
    ("Материалы:", "docs/specs, docs/plans и эти слайды — в репозитории воркшопа"),
], top=4.1, size=16, gap=10)

out = "/Users/ucantrustmedude/Learn/ai-workshop-teztaxi/docs/slides/ai-workshop.pptx"
prs.save(out)
print("saved", out)
