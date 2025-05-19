import json
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup

class MangaTracker:
    def __init__(self):
        self.data_file = "manga_data.json"
        self.manga_list = self.load_data()

    def load_data(self):
        """Load manga data from JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return []

    def save_data(self):
        """Save manga data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.manga_list, f, indent=4)

    def add_manga(self, title, url):
        """Add a new manga to track"""
        manga = {
            "title": title,
            "url": url,
            "last_checked": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_chapter": None
        }
        self.manga_list.append(manga)
        self.save_data()
        print(f"Added {title} to your tracking list!")

    def list_manga(self):
        """Display all tracked manga"""
        if not self.manga_list:
            print("No manga in your tracking list!")
            return
        
        print("\nYour Manga List:")
        print("-" * 50)

        for i, manga in enumerate(self.manga_list, 1):
            print(f"{i}. {manga['title']}")
            if manga['last_chapter']:
                print(f"   Last chapter: {manga['last_chapter']}")
            print(f"   Last checked: {manga['last_checked']}")
            print("-" * 50)

    def check_updates(self):
        """Check for updates on all tracked manga"""
        if not self.manga_list:
            print("No manga to check!")
            return

        print("\nChecking for updates...")
        for manga in self.manga_list:
            try:
                response = requests.get(manga['url'])
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find the first div with the specific class structure
                chapter_div = soup.find('div', class_='col-sm-5 col-7 text-left order-2 text-truncate')
                if chapter_div:
                    chapter_span = chapter_div.find('span', class_='chapter')
                    if chapter_span:
                        chapter_link = chapter_span.find('a', class_='filter')
                        if chapter_link:
                            latest_chapter = chapter_link.text.strip()
                            chapter_url = chapter_link.get('href', '')
                            print(f"Found chapter: {latest_chapter}")
                            print(f"URL: {chapter_url}")
                            if latest_chapter != manga['last_chapter']:
                                print(f"New chapter available for {manga['title']}: {latest_chapter}")
                                manga['last_chapter'] = latest_chapter
                            else:
                                print(f"No new chapters for {manga['title']}")
                        else:
                            print(f"Could not find chapter link for {manga['title']}")
                    else:
                        print(f"Could not find chapter span for {manga['title']}")
                else:
                    print(f"Could not find chapter div for {manga['title']}")
                
                manga['last_checked'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            except Exception as e:
                print(f"Error checking {manga['title']}: {str(e)}")
        
        self.save_data()

def main():
    tracker = MangaTracker()
    
    while True:
        print("\nManga Tracker Menu:")
        print("1. Add new manga")
        print("2. List tracked manga")
        print("3. Check for updates")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            title = input("Enter manga title: ")
            url = input("Enter manga URL: ")
            tracker.add_manga(title, url)
        
        elif choice == "2":
            tracker.list_manga()
        
        elif choice == "3":
            tracker.check_updates()
        
        elif choice == "4":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main() 