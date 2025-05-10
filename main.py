import sys
import feedparser
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QTextEdit, QStatusBar, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QTimer

# --- Constants ---
APP_TITLE = "News Aggregator"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
NEWS_SITES = {
    "BBC News": "http://feeds.bbci.co.uk/news/rss.xml",
    "CNN": "http://rss.cnn.com/rss/edition.rss",

    "Al Jazeera": "http://www.aljazeera.com/xml/rss/all.xml",
    "The Guardian": "https://www.theguardian.com/international/rss",
    "Kathmandu Post": "https://kathmandupost.com/rss",
   
}

# --- Main Application Window ---
class NewsAppGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(APP_TITLE)
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        try:
            self.setWindowIcon(QIcon("icon.png"))  # Set your app icon here
        except:
            print("Warning: icon.png not found. Using default icon.")

        # --- Central Widget and Main Layout ---
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # --- Title Label ---
        title_label = QLabel(APP_TITLE)
        title_label.setFont(QFont("Arial", 28, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #007BFF;")  # Blue color
        main_layout.addWidget(title_label)

        # --- Controls Layout (ComboBox and Button) ---
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)

        site_select_label = QLabel("Select News Source:")
        site_select_label.setFont(QFont("Arial", 12))
        controls_layout.addWidget(site_select_label)

        self.site_combo = QComboBox()
        self.site_combo.setFont(QFont("Arial", 11))
        self.site_combo.addItems(NEWS_SITES.keys())
        self.site_combo.setMinimumWidth(200)
        controls_layout.addWidget(self.site_combo)

        # Add a spacer to push the button to the right
        controls_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.fetch_button = QPushButton("Fetch News")
        self.fetch_button.setFont(QFont("Arial", 11, QFont.Bold))
        self.fetch_button.setMinimumHeight(35)
        self.fetch_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 8px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.fetch_button.clicked.connect(self.on_fetch_news_clicked)
        controls_layout.addWidget(self.fetch_button)

        main_layout.addLayout(controls_layout)

        # --- News Display Area ---
        self.news_display_area = QTextEdit()
        self.news_display_area.setReadOnly(True)
        self.news_display_area.setFont(QFont("Georgia", 11))
        self.news_display_area.setPlaceholderText("Select a news source and click 'Fetch News' to see headlines.")
        main_layout.addWidget(self.news_display_area, 1)

        # --- Status Bar ---
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready.", 3000)

        self.show()

    def on_fetch_news_clicked(self):
        selected_site_name = self.site_combo.currentText()
        selected_site_url = NEWS_SITES[selected_site_name]

        self.status_bar.showMessage(f"Fetching news from {selected_site_name}...", 0)
        self.news_display_area.clear()
        self.news_display_area.setPlaceholderText(f"Fetching news from {selected_site_name}...\nPlease wait.")
        self.fetch_button.setEnabled(False)

        QTimer.singleShot(1500, lambda: self.fetch_news(selected_site_url))

    def fetch_news(self, url):
        if url == "local":
            self.news_display_area.setText("This is a placeholder for a local news source.")
            self.status_bar.showMessage("Loaded local simulated news.", 3000)
            self.fetch_button.setEnabled(True)
            return

        feed = feedparser.parse(url)

        if feed.bozo:
            self.news_display_area.setText("⚠️ Failed to parse the feed. It may be unavailable or malformed.")
            self.status_bar.showMessage("❌ Error fetching the news.", 5000)
        elif not feed.entries:
            self.news_display_area.setText("ℹ️ No news items found in the selected feed.")
            self.status_bar.showMessage("No news found.", 5000)
        else:
            content = ""
            for entry in feed.entries[:10]:
                title = entry.get("title", "No Title")
                summary = entry.get("summary", "")
                link = entry.get("link", "")
                content += f"<b>{title}</b><br>{summary}<br><a href='{link}'>{link}</a><br><hr><br>"

            self.news_display_area.setHtml(content)
            self.status_bar.showMessage("✅ News fetched successfully!", 3000)

        self.fetch_button.setEnabled(True)


# --- Main Execution ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewsAppGUI()
    sys.exit(app.exec_())
