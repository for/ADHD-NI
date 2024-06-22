import sys, urllib3, requests
from bs4 import BeautifulSoup
from PyQt6.QtWidgets import *
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Scrp_ADHD:
    def __init__(self): self.url = "https://www.nhs.uk/conditions/attention-deficit-hyperactivity-disorder-adhd/"
    def parse(self):
        try:
            response = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0'}, verify=False, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            return [f"{self._parse_section(section)} - {self.url}" for section in soup.find_all('section') if section.find('h2')]
        except Exception as e: print(f"Error scraping {self.url}: {str(e)}"); return []

    def _parse_section(self, section):
        content = [section.find('h2').text.strip()]
        for elem in section.find_all(['p', 'ul']):
            if elem.name == 'p': content.append(elem.text.strip())
            else: content.extend(f"• {li.text.strip()}" for li in elem.find_all('li') if li.text.strip())
        return '\n'.join(filter(None, content))

class Scrp_MentHealth:
    def __init__(self): self.url = "https://www.nhs.uk/conditions/medically-unexplained-symptoms/"
    def parse(self):
        try:
            response = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0'}, verify=False, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            return [f"{self._parse_section(section)} - {self.url}" for section in soup.find_all('section') if section.find('h2')]
        except Exception as e: print(f"Error scraping {self.url}: {str(e)}"); return []

    def _parse_section(self, section):
        content = [section.find('h2').text.strip()]
        for elem in section.find_all(['p', 'ul']):
            if elem.name == 'p': content.append(elem.text.strip())
            else: content.extend(f"• {li.text.strip()}" for li in elem.find_all('li') if li.text.strip())
        return '\n'.join(filter(None, content))

class ADHDResourceFinder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("ADHD Resources in Northern Ireland")
        self.setGeometry(100, 100, 600, 400)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(QLabel("ADHD Resources in Northern Ireland"))
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        self.search_button = QPushButton("Search for Resources")
        self.search_button.clicked.connect(self.search_resources)
        layout.addWidget(self.search_button)

    def search_resources(self):
        self.tab_widget.clear()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab_widget.addTab(self.tab1, "ADHD")
        self.tab_widget.addTab(self.tab2, "Mental Health")
        layout1 = QVBoxLayout(self.tab1)
        layout2 = QVBoxLayout(self.tab2)
        self.resource_list1 = QListWidget()
        self.resource_list2 = QListWidget()
        layout1.addWidget(self.resource_list1)
        layout2.addWidget(self.resource_list2)
        self.resource_list1.addItems(Scrp_ADHD().parse())
        self.resource_list2.addItems(Scrp_MentHealth().parse())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ADHDResourceFinder()
    window.show()
    sys.exit(app.exec())