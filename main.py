from src.sorter_bot.file_sorter import FileSorter

def start_app():
    target_folder = input("Enter the path to the folder to sort: ")
    sorter = FileSorter(target_folder)
    result = sorter.run()
    print(result)

if __name__ == "__main__":
    start_app()