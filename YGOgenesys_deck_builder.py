import sys
import json
import os
import locale
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QLabel, QSplitter, QFileDialog, QSpinBox,
    QMenuBar, QMenu, QListWidget, QListWidgetItem, QMessageBox,
    QPushButton, QGroupBox, QComboBox
)
from PySide6.QtGui import QPixmap, QAction, QActionGroup
from PySide6.QtCore import Qt

class DeckBuilderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setup_default_language()
        self.setup_translations()
        
        # --- App State ---
        self.all_cards = {}
        self.id_to_cid = {}
        self.card_list_cids = []
        self.current_file_path = None
        
        # --- Interaction State ---
        self.active_cid = None
        self.active_card_source_list = None

        # --- Deck State ---
        self.main_deck = {}
        self.extra_deck = {}
        self.side_deck = {}

        self.load_card_data()
        self.setup_ui()
        self.update_all_views()
        self.update_ui_text()

    def setup_default_language(self):
        try:
            lang_code, _ = locale.getdefaultlocale()
            primary_lang = lang_code.split('_')[0]
        except Exception:
            primary_lang = 'en'

        if primary_lang == 'zh':
            self.current_lang = "zh"
            self.current_display_name_key = "cn_name"
        elif primary_lang == 'ja':
            self.current_lang = "ja"
            self.current_display_name_key = "jp_name"
        else:
            self.current_lang = "en"
            self.current_display_name_key = "en_name"

    def setup_translations(self):
        self.name_options = {
            "cn_name": {"zh": "YGOPro 中文", "ja": "YGOPro 中国語", "en": "YGOPro Chinese"},
            "sc_name": {"zh": "官方简体中文", "ja": "公式簡体字", "en": "Official SC"},
            "nwbbs_n": {"zh": "NWBBS 中文", "ja": "NWBBS 中国語", "en": "NWBBS Chinese"},
            "cnocg_n": {"zh": "CNOCG 中文", "ja": "CNOCG 中国語", "en": "CNOCG Chinese"},
            "jp_name": {"zh": "日语原名", "ja": "日本語名", "en": "Japanese"},
            "en_name": {"zh": "英文名", "ja": "英語名", "en": "English"}
        }
        self.translations = {
            "window_title": {"zh": "游戏王分数制组卡器", "ja": "遊戯王ポイント制デッキビルダー", "en": "Yu-Gi-Oh! Point System Deck Builder"},
            "file_menu": {"zh": "&文件", "ja": "&ファイル", "en": "&File"},
            "new_deck": {"zh": "&新建卡组", "ja": "&新規デッキ", "en": "&New Deck"},
            "open_deck": {"zh": "&打开卡组...", "ja": "&デッキを開く...", "en": "&Open Deck..."},
            "save_deck": {"zh": "&保存卡组", "ja": "&デッキを保存", "en": "&Save Deck"},
            "save_as": {"zh": "另存为...", "ja": "名前を付けて保存...", "en": "Save As..."},
            "exit": {"zh": "&退出", "ja": "&終了", "en": "&Exit"},
            "options_menu": {"zh": "&选项", "ja": "&オプション", "en": "&Options"},
            "language_menu": {"zh": "&语言", "ja": "&言語", "en": "&Language"},
            "search_group": {"zh": "卡片检索", "ja": "カード検索", "en": "Card Search"},
            "search_placeholder": {"zh": "输入卡名进行搜索...", "ja": "カード名で検索...", "en": "Search by card name..."},
            "display_name_label": {"zh": "显示名称:", "ja": "表示名:", "en": "Display Name:"},
            "details_group": {"zh": "卡片详情 (操作目标)", "ja": "カード詳細 (操作対象)", "en": "Card Details (Active Target)"},
            "no_card_selected": {"zh": "请选择一张卡片", "ja": "カードを選択してください", "en": "Please select a card"},
            "image_not_found": {"zh": "没有图片", "ja": "画像がありません", "en": "No Image"},
            "points_cost": {"zh": "分数成本", "ja": "ポイントコスト", "en": "Point Cost"},
            "add_to_main": {"zh": "添加到主卡组", "ja": "メインデッキに追加", "en": "Add to Main Deck"},
            "add_to_extra": {"zh": "添加到额外", "ja": "EXデッキに追加", "en": "Add to Extra"},
            "add_to_side": {"zh": "添加到副卡组", "ja": "サイドデッキに追加", "en": "Add to Side"},
            "deck_info_group": {"zh": "卡组信息", "ja": "デッキ情報", "en": "Deck Info"},
            "points": {"zh": "分数", "ja": "ポイント", "en": "Points"},
            "cap": {"zh": "上限", "ja": "上限", "en": "Cap"},
            "main_deck_label": {"zh": "主卡组", "ja": "メインデッキ", "en": "Main Deck"},
            "extra_deck_label": {"zh": "额外卡组", "ja": "EXデッキ", "en": "Extra Deck"},
            "side_deck_label": {"zh": "副卡组", "ja": "サイドデッキ", "en": "Side Deck"},
            "deck_stats_label": {"zh": "主卡组: {0} | 额外: {1} | 副卡组: {2}", "ja": "メイン: {0} | EX: {1} | サイド: {2}", "en": "Main: {0} | Extra: {1} | Side: {2}"},
            "remove_selected": {"zh": "移除选中卡片", "ja": "選択したカードを削除", "en": "Remove Selected Card"},
            "select_card_to_add": {"zh": "请先选择一张卡片作为操作目标。", "ja": "まず操作対象のカードを選択してください。", "en": "Please select a target card first."},
            "limit_reached": {"zh": "数量达到上限", "ja": "上限に達しました", "en": "Limit Reached"},
            "limit_reached_msg": {"zh": "每张同名卡最多投入3张。", "ja": "各カードは3枚までしか入れられません。", "en": "You can only have up to 3 copies of any card."},
            "legality_error_title": {"zh": "构筑错误", "ja": "構築エラー", "en": "Legality Error"},
            "extra_in_main_error_msg": {"zh": "融合、同调、超量怪兽不能加入主卡组。", "ja": "融合・シンクロ・エクシーズモンスターはメインデッキに追加できません。", "en": "Fusion, Synchro, and Xyz monsters cannot be added to the Main Deck."},
            "main_in_extra_error_msg": {"zh": "只有融合、同调、超量怪兽能加入额外卡组。", "ja": "融合・シンクロ・エクシーズモンスターのみがEXデッキに追加できます。", "en": "Only Fusion, Synchro, and Xyz monsters can be added to the Extra Deck."},
            "deck_illegal_title": {"zh": "卡组不合法", "ja": "デッキが不正です", "en": "Invalid Deck"},
            "deck_illegal_header": {"zh": "您的卡组存在以下问题，无法保存：\n", "ja": "デッキに以下の問題があるため、保存できません：\n", "en": "Your deck has the following issues and cannot be saved:\n"},
            "main_deck_size_error": {"zh": "主卡组数量 ({0}) 必须在40-60张之间。", "ja": "メインデッキの枚数 ({0}) は40枚から60枚の間でなければなりません。", "en": "Main Deck must have between 40 and 60 cards (currently {0})."},
            "extra_deck_size_error": {"zh": "额外卡组数量 ({0}) 不能超过15张。", "ja": "EXデッキの枚数 ({0}) は15枚を超えることはできません。", "en": "Extra Deck cannot have more than 15 cards (currently {0})."},
            "side_deck_size_error": {"zh": "副卡组数量 ({0}) 不能超过15张。", "ja": "サイドデッキの枚数 ({0}) は15枚を超えることはできません。", "en": "Side Deck cannot have more than 15 cards (currently {0})."},
            "copy_limit_error": {"zh": "卡片 '{0}' 的合计投入数量超过3张。", "ja": "カード '{0}' の合計枚数が3枚を超えています。", "en": "More than 3 copies of '{0}' were found."},
            "extra_in_main_list_header": {"zh": "\n以下额外卡组怪兽不能在主卡组中:", "ja": "\n以下のEXデッキモンスターはメインデッキに入れられません:", "en": "\nThe following Extra Deck monsters cannot be in the Main Deck:"},
            "main_in_extra_list_header": {"zh": "\n以下非额外卡组怪兽不能在额外卡组中:", "ja": "\n以下の非EXデッキモンスターはEXデッキに入れられません:", "en": "\nThe following non-Extra Deck monsters cannot be in the Extra Deck:"}
        }

    def load_card_data(self):
        try:
            with open("cards_data.json", "r", encoding="utf-8") as f: data = json.load(f)
            for cid, card_data in data.items():
                card_type_text = card_data.get("text", {}).get("types", "")
                if "链接" not in card_type_text and "灵摆" not in card_type_text:
                    self.all_cards[cid] = card_data
                    card_id = card_data.get("id")
                    if card_id: self.id_to_cid[str(card_id)] = cid
            self.card_list_cids = sorted(self.all_cards.keys(), key=lambda c: self.get_card_display_name(self.all_cards[c]) or "")
        except FileNotFoundError: QMessageBox.critical(self, "Error", "cards_data.json not found.")
        except Exception as e: QMessageBox.critical(self, "Error", f"Failed to load card data: {e}")

    def setup_ui(self):
        self.setGeometry(100, 100, 1360, 800)
        menu_bar = self.menuBar()
        self.file_menu = menu_bar.addMenu(""); self.new_deck_action = self.file_menu.addAction(""); self.new_deck_action.triggered.connect(self.new_deck)
        self.open_deck_action = self.file_menu.addAction(""); self.open_deck_action.triggered.connect(self.open_deck)
        self.save_deck_action = self.file_menu.addAction(""); self.save_deck_action.triggered.connect(self.save_deck)
        self.save_as_action = self.file_menu.addAction(""); self.save_as_action.triggered.connect(self.save_deck_as)
        self.file_menu.addSeparator(); self.exit_action = self.file_menu.addAction(""); self.exit_action.triggered.connect(self.close)
        self.options_menu = menu_bar.addMenu(""); self.language_menu = self.options_menu.addMenu("")
        lang_group = QActionGroup(self)
        self.zh_action = lang_group.addAction(QAction("简体中文", self, checkable=True)); self.zh_action.triggered.connect(lambda: self.on_language_changed("zh"))
        self.ja_action = lang_group.addAction(QAction("日本語", self, checkable=True)); self.ja_action.triggered.connect(lambda: self.on_language_changed("ja"))
        self.en_action = lang_group.addAction(QAction("English", self, checkable=True)); self.en_action.triggered.connect(lambda: self.on_language_changed("en"))
        self.language_menu.addActions(lang_group.actions())
        central_widget = QWidget(); self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget); splitter = QSplitter(Qt.Horizontal); main_layout.addWidget(splitter)
        left_pane = QWidget(); left_layout = QVBoxLayout(left_pane); splitter.addWidget(left_pane)
        right_pane = QWidget(); right_layout = QVBoxLayout(right_pane); splitter.addWidget(right_pane)
        self.browser_group = QGroupBox(); browser_layout = QVBoxLayout(self.browser_group)
        self.search_input = QLineEdit(); browser_layout.addWidget(self.search_input); self.search_input.textChanged.connect(self.filter_card_list)
        name_display_layout = QHBoxLayout(); self.display_name_label = QLabel(); self.name_display_combo = QComboBox()
        self.name_display_combo.currentIndexChanged.connect(self.on_name_display_changed)
        name_display_layout.addWidget(self.display_name_label); name_display_layout.addWidget(self.name_display_combo); browser_layout.addLayout(name_display_layout)
        self.card_list_view = QListWidget(); self.card_list_view.itemSelectionChanged.connect(self.on_browser_card_selected); self.card_list_view.itemDoubleClicked.connect(self.on_browser_card_double_clicked)
        browser_layout.addWidget(self.card_list_view); left_layout.addWidget(self.browser_group)
        self.details_group = QGroupBox(); details_layout = QVBoxLayout(self.details_group)
        self.card_image_label = QLabel(); self.card_image_label.setAlignment(Qt.AlignCenter); self.card_image_label.setFixedSize(240, 350); self.card_image_label.setScaledContents(True)
        self.card_info_label = QLabel(); self.card_info_label.setWordWrap(True); self.card_info_label.setAlignment(Qt.AlignTop)
        info_display_layout = QHBoxLayout(); info_display_layout.addWidget(self.card_image_label); info_display_layout.addWidget(self.card_info_label); details_layout.addLayout(info_display_layout)
        add_buttons_layout = QHBoxLayout(); self.add_to_main_btn = QPushButton(); self.add_to_extra_btn = QPushButton(); self.add_to_side_btn = QPushButton()
        self.add_to_main_btn.clicked.connect(lambda: self.add_card_from_details("Main Deck"))
        self.add_to_extra_btn.clicked.connect(lambda: self.add_card_from_details("Extra Deck"))
        self.add_to_side_btn.clicked.connect(lambda: self.add_card_from_details("Side Deck"))
        add_buttons_layout.addWidget(self.add_to_main_btn); add_buttons_layout.addWidget(self.add_to_extra_btn); add_buttons_layout.addWidget(self.add_to_side_btn); details_layout.addLayout(add_buttons_layout)
        left_layout.addWidget(self.details_group); left_layout.setStretch(0, 5); left_layout.setStretch(1, 4)
        self.stats_group = QGroupBox(); stats_layout = QHBoxLayout(self.stats_group)
        self.points_label_title = QLabel(); stats_layout.addWidget(self.points_label_title); self.points_label = QLabel("0 / 100"); stats_layout.addWidget(self.points_label)
        self.cap_label_title = QLabel(); stats_layout.addWidget(self.cap_label_title); self.point_cap_spinbox = QSpinBox(); self.point_cap_spinbox.setRange(0, 999); self.point_cap_spinbox.setValue(100)
        self.point_cap_spinbox.valueChanged.connect(self.update_points_display); stats_layout.addWidget(self.point_cap_spinbox); stats_layout.addStretch()
        self.stats_label = QLabel(); stats_layout.addWidget(self.stats_label); right_layout.addWidget(self.stats_group)
        self.main_deck_group, self.main_deck_list = self.create_deck_list_widget("Main Deck")
        self.extra_deck_group, self.extra_deck_list = self.create_deck_list_widget("Extra Deck")
        self.side_deck_group, self.side_deck_list = self.create_deck_list_widget("Side Deck")
        right_layout.addWidget(self.main_deck_group); right_layout.addWidget(self.extra_deck_group); right_layout.addWidget(self.side_deck_group)
        splitter.setSizes([500, 760])

    def create_deck_list_widget(self, name):
        group_box = QGroupBox(); list_widget = QListWidget(); list_widget.setObjectName(name)
        list_widget.itemSelectionChanged.connect(self.on_deck_card_selected)
        list_widget.itemDoubleClicked.connect(self.on_deck_card_double_clicked)
        layout = QVBoxLayout(group_box); layout.addWidget(list_widget)
        return group_box, list_widget

    def on_language_changed(self, lang_code): self.current_lang = lang_code; self.update_ui_text()
    
    def on_name_display_changed(self, index):
        key = self.name_display_combo.itemData(index)
        if key:
            self.current_display_name_key = key; self.filter_card_list()
            self.update_deck_list_widget(self.main_deck_list, self.main_deck)
            self.update_deck_list_widget(self.extra_deck_list, self.extra_deck)
            self.update_deck_list_widget(self.side_deck_list, self.side_deck)

    def update_ui_text(self):
        lang = self.current_lang
        self.setWindowTitle(self.translations["window_title"][lang]); self.file_menu.setTitle(self.translations["file_menu"][lang])
        self.new_deck_action.setText(self.translations["new_deck"][lang]); self.open_deck_action.setText(self.translations["open_deck"][lang])
        self.save_deck_action.setText(self.translations["save_deck"][lang]); self.save_as_action.setText(self.translations["save_as"][lang])
        self.exit_action.setText(self.translations["exit"][lang]); self.options_menu.setTitle(self.translations["options_menu"][lang])
        self.language_menu.setTitle(self.translations["language_menu"][lang]); self.zh_action.setChecked(lang == "zh")
        self.ja_action.setChecked(lang == "ja"); self.en_action.setChecked(lang == "en")
        self.browser_group.setTitle(self.translations["search_group"][lang]); self.search_input.setPlaceholderText(self.translations["search_placeholder"][lang])
        self.display_name_label.setText(self.translations["display_name_label"][lang]); self.details_group.setTitle(self.translations["details_group"][lang])
        self.card_image_label.setText(self.translations["no_card_selected"][lang]); self.add_to_main_btn.setText(self.translations["add_to_main"][lang])
        self.add_to_extra_btn.setText(self.translations["add_to_extra"][lang]); self.add_to_side_btn.setText(self.translations["add_to_side"][lang])
        self.stats_group.setTitle(self.translations["deck_info_group"][lang]); self.points_label_title.setText(f"<b>{self.translations['points'][lang]}:</b>")
        self.cap_label_title.setText(f"<b>{self.translations['cap'][lang]}:</b>"); self.main_deck_group.setTitle(self.translations["main_deck_label"][lang])
        self.extra_deck_group.setTitle(self.translations["extra_deck_label"][lang]); self.side_deck_group.setTitle(self.translations["side_deck_label"][lang])
        self.name_display_combo.blockSignals(True); self.name_display_combo.clear()
        for key, names in self.name_options.items(): self.name_display_combo.addItem(names[lang], key)
        index = self.name_display_combo.findData(self.current_display_name_key)
        if index != -1: self.name_display_combo.setCurrentIndex(index)
        self.name_display_combo.blockSignals(False); self.update_stats_display()

    def get_card_display_name(self, card_data):
        name = card_data.get(self.current_display_name_key) or card_data.get("cn_name")
        return name if name else None

    def filter_card_list(self):
        search_text = self.search_input.text().lower(); temp_card_list = []
        for cid, data in self.all_cards.items():
            name = self.get_card_display_name(data)
            if name and (not search_text or search_text in name.lower()):
                temp_card_list.append(cid)
        self.card_list_cids = sorted(temp_card_list, key=lambda c: self.get_card_display_name(self.all_cards[c]))
        self.update_card_list_view()

    def update_card_list_view(self):
        self.card_list_view.clear()
        for cid in self.card_list_cids:
            card_data = self.all_cards.get(cid)
            if card_data:
                display_name = self.get_card_display_name(card_data)
                if display_name:
                    item = QListWidgetItem(display_name); item.setData(Qt.UserRole, cid); self.card_list_view.addItem(item)
    
    def display_card_by_cid(self, cid, source_list):
        self.active_cid = cid
        self.active_card_source_list = source_list
        card_data = self.all_cards.get(cid)
        if not card_data: return
        image_path = os.path.join("pics", f"{card_data.get('id')}.jpg"); pixmap = QPixmap(image_path)
        if pixmap.isNull(): self.card_image_label.setText(self.translations["image_not_found"][self.current_lang])
        else: self.card_image_label.setPixmap(pixmap)
        point_cost = card_data.get("point", 0); display_name = self.get_card_display_name(card_data) or ""
        info_text = (f"<b>{display_name}</b><br><i>{card_data.get('en_name', '')}</i><br><br>"
                     f"<b>{self.translations['points_cost'][self.current_lang]}: {point_cost}</b><hr>"
                     f"{card_data.get('text', {}).get('types', '').replace(chr(10), '<br>')}<hr>"
                     f"{card_data.get('text', {}).get('desc', '')}")
        self.card_info_label.setText(info_text)

    def on_browser_card_selected(self):
        if not self.card_list_view.selectedItems(): return
        self.main_deck_list.clearSelection(); self.extra_deck_list.clearSelection(); self.side_deck_list.clearSelection()
        cid = self.card_list_view.selectedItems()[0].data(Qt.UserRole)
        self.display_card_by_cid(cid, self.card_list_view)

    def on_deck_card_selected(self):
        sender_list = self.sender()
        if not sender_list.selectedItems(): return
        self.card_list_view.clearSelection()
        for deck_list in [self.main_deck_list, self.extra_deck_list, self.side_deck_list]:
            if deck_list is not sender_list: deck_list.clearSelection()
        card_id = sender_list.selectedItems()[0].data(Qt.UserRole)
        cid = self.id_to_cid.get(str(card_id))
        if cid: self.display_card_by_cid(cid, sender_list)
    
    def update_deck_list_widget(self, list_widget, deck_dict):
        list_widget.clear()
        sorted_ids = sorted(deck_dict.keys(), key=lambda i: self.get_card_display_name(self.all_cards[self.id_to_cid[str(i)]]) or "")
        for card_id in sorted_ids:
            count = deck_dict[card_id]; cid = self.id_to_cid.get(str(card_id))
            if cid:
                card_data = self.all_cards[cid]; display_name = self.get_card_display_name(card_data)
                if display_name:
                    point_cost = card_data.get("point", 0)
                    display_text = f"[{count}x] {display_name}"
                    if point_cost > 0: display_text += f"  ({point_cost} P)"
                    item = QListWidgetItem(display_text); item.setData(Qt.UserRole, card_id); list_widget.addItem(item)
    
    def update_all_views(self):
        self.update_deck_list_widget(self.main_deck_list, self.main_deck)
        self.update_deck_list_widget(self.extra_deck_list, self.extra_deck)
        self.update_deck_list_widget(self.side_deck_list, self.side_deck)
        self.update_stats_display(); self.update_points_display()

    def restore_selection(self):
        if not self.active_cid or not self.active_card_source_list: return
        
        target_list = self.active_card_source_list
        target_list.blockSignals(True)
        
        data_to_find = self.active_cid
        if target_list is not self.card_list_view:
            card_id = self.all_cards[self.active_cid].get("id")
            data_to_find = card_id

        for i in range(target_list.count()):
            item = target_list.item(i)
            if item.data(Qt.UserRole) == data_to_find:
                item.setSelected(True)
                target_list.scrollToItem(item)
                break
        target_list.blockSignals(False)

    def update_stats_display(self):
        main_count = sum(self.main_deck.values()); extra_count = sum(self.extra_deck.values()); side_count = sum(self.side_deck.values())
        self.stats_label.setText(self.translations["deck_stats_label"][self.current_lang].format(main_count, extra_count, side_count))

    def update_points_display(self):
        total_points = sum(self.all_cards[self.id_to_cid[str(cid)]].get("point", 0) * count for deck in (self.main_deck, self.extra_deck, self.side_deck) for cid, count in deck.items())
        point_cap = self.point_cap_spinbox.value(); self.points_label.setText(f"{total_points} / {point_cap}")
        self.points_label.setStyleSheet("color: red; font-weight: bold;" if total_points > point_cap else "")

    def on_browser_card_double_clicked(self, item):
        cid = item.data(Qt.UserRole); card_data = self.all_cards.get(cid)
        if not card_data: return
        card_id = card_data.get("id"); card_type_text = card_data.get("text", {}).get("types", "")
        if any(t in card_type_text for t in ["融合", "同调", "超量"]): self.add_card("Extra Deck", card_id)
        else: self.add_card("Main Deck", card_id)

    def on_deck_card_double_clicked(self, item):
        list_widget = self.sender(); card_id = item.data(Qt.UserRole)
        if card_id: self.remove_card(list_widget.objectName(), card_id, 1)

    def add_card_from_details(self, deck_name):
        if not self.active_cid:
            QMessageBox.information(self, "Info", self.translations["select_card_to_add"][self.current_lang]); return
        card_id = self.all_cards[self.active_cid].get("id")
        if card_id: self.add_card(deck_name, card_id)

    def add_card(self, deck_name, card_id):
        cid = self.id_to_cid.get(str(card_id))
        if not cid: return
        card_data = self.all_cards[cid]; card_type_text = card_data.get("text", {}).get("types", "")
        is_extra_deck_monster = any(t in card_type_text for t in ["融合", "同调", "超量"])
        if deck_name == "Main Deck" and is_extra_deck_monster:
            QMessageBox.warning(self, self.translations["legality_error_title"][self.current_lang], self.translations["extra_in_main_error_msg"][self.current_lang]); return
        if deck_name == "Extra Deck" and not is_extra_deck_monster:
            QMessageBox.warning(self, self.translations["legality_error_title"][self.current_lang], self.translations["main_in_extra_error_msg"][self.current_lang]); return
        deck_map = {"Main Deck": self.main_deck, "Extra Deck": self.extra_deck, "Side Deck": self.side_deck}
        deck = deck_map.get(deck_name); total_count = sum(d.get(card_id, 0) for d in deck_map.values())
        if total_count >= 3:
            QMessageBox.warning(self, self.translations["limit_reached"][self.current_lang], self.translations["limit_reached_msg"][self.current_lang]); return
        deck[card_id] = deck.get(card_id, 0) + 1
        self.update_all_views()
        self.restore_selection()
    
    def remove_card(self, deck_name, card_id, amount):
        deck_map = {"Main Deck": self.main_deck, "Extra Deck": self.extra_deck, "Side Deck": self.side_deck}
        deck = deck_map.get(deck_name)
        if deck is None or card_id not in deck: return
        if amount == 'all' or deck[card_id] <= amount: del deck[card_id]
        else: deck[card_id] -= amount
        self.update_all_views()
        self.restore_selection()

    def new_deck(self):
        self.active_cid = None; self.active_card_source_list = None
        self.main_deck.clear(); self.extra_deck.clear(); self.side_deck.clear()
        self.current_file_path = None; self.update_all_views()
        self.setWindowTitle(f"{self.translations['window_title'][self.current_lang]} - {self.translations['new_deck'][self.current_lang]}")

    def open_deck(self):
        filepath, _ = QFileDialog.getOpenFileName(self, self.translations["open_deck"][self.current_lang], "", "YGOPro Deck (*.ydk);;All Files (*)")
        if not filepath: return
        self.new_deck(); self.current_file_path = filepath; current_section = None
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#created by'): continue
                    if line == '#main': current_section = self.main_deck
                    elif line == '#extra': current_section = self.extra_deck
                    elif line == '!side': current_section = self.side_deck
                    elif line.isdigit() and current_section is not None:
                        card_id = int(line)
                        if str(card_id) in self.id_to_cid: current_section[card_id] = current_section.get(card_id, 0) + 1
        except Exception as e: QMessageBox.critical(self, "Error", f"Could not read deck file:\n{e}")
        self.update_all_views(); self.setWindowTitle(f"Deck Builder - {os.path.basename(filepath)}")

    def check_deck_legality(self):
        lang = self.current_lang; error_messages = []
        main_count = sum(self.main_deck.values()); extra_count = sum(self.extra_deck.values()); side_count = sum(self.side_deck.values())
        if not (40 <= main_count <= 60): error_messages.append(self.translations["main_deck_size_error"][lang].format(main_count))
        if extra_count > 15: error_messages.append(self.translations["extra_deck_size_error"][lang].format(extra_count))
        if side_count > 15: error_messages.append(self.translations["side_deck_size_error"][lang].format(side_count))
        all_cards_counter = {}; illegal_main = []; illegal_extra = []
        for card_id, count in self.main_deck.items():
            all_cards_counter[card_id] = all_cards_counter.get(card_id, 0) + count
            card_data = self.all_cards[self.id_to_cid[str(card_id)]]; card_type = card_data.get("text", {}).get("types", "")
            if any(t in card_type for t in ["融合", "同调", "超量"]): illegal_main.append(self.get_card_display_name(card_data))
        for card_id, count in self.extra_deck.items():
            all_cards_counter[card_id] = all_cards_counter.get(card_id, 0) + count
            card_data = self.all_cards[self.id_to_cid[str(card_id)]]; card_type = card_data.get("text", {}).get("types", "")
            if not any(t in card_type for t in ["融合", "同调", "超量"]): illegal_extra.append(self.get_card_display_name(card_data))
        for card_id, count in self.side_deck.items(): all_cards_counter[card_id] = all_cards_counter.get(card_id, 0) + count
        for card_id, count in all_cards_counter.items():
            if count > 3: error_messages.append(self.translations["copy_limit_error"][lang].format(self.get_card_display_name(self.all_cards[self.id_to_cid[str(card_id)]])))
        if illegal_main: error_messages.append(self.translations["extra_in_main_list_header"][lang] + "\n- " + "\n- ".join(set(illegal_main)))
        if illegal_extra: error_messages.append(self.translations["main_in_extra_list_header"][lang] + "\n- " + "\n- ".join(set(illegal_extra)))
        if error_messages:
            full_error_msg = self.translations["deck_illegal_header"][lang] + "\n* " + "\n* ".join(error_messages)
            QMessageBox.critical(self, self.translations["deck_illegal_title"][lang], full_error_msg); return False
        return True

    def save_deck(self):
        if not self.check_deck_legality(): return
        if not self.current_file_path: self.save_deck_as()
        else: self._write_deck_file(self.current_file_path)

    def save_deck_as(self):
        if not self.check_deck_legality(): return
        filepath, _ = QFileDialog.getSaveFileName(self, self.translations["save_as"][self.current_lang], "", "YGOPro Deck (*.ydk);;All Files (*)")
        if filepath:
            self.current_file_path = filepath; self._write_deck_file(filepath)
            self.setWindowTitle(f"YGOgenesys Deck Builder - {os.path.basename(filepath)}")

    def _write_deck_file(self, filepath):
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("#created by YGOgenesys Deck Builder\n")
                f.write("#main\n"); [f.write(f"{cid}\n" * c) for cid, c in self.main_deck.items()]
                f.write("#extra\n"); [f.write(f"{cid}\n" * c) for cid, c in self.extra_deck.items()]
                f.write("!side\n"); [f.write(f"{cid}\n" * c) for cid, c in self.side_deck.items()]
        except Exception as e: QMessageBox.critical(self, "Error", f"Could not write to deck file:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeckBuilderWindow()
    window.show()
    sys.exit(app.exec())