class Text_Edit:
    def __init__(self, file_path, lines):
        self.file_path = file_path
        self.lines = lines

    def save_txt(file_path, lines):
        try:
            with open(file_path, 'w') as file:
                file.write("\n".join(lines))
            return True
        except Exception as e:
            print(f"Error Saving File: {e}")
            return False

    def load_txt(file_path):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
            return [line.strip() for line in lines]
        except Exception as e:
            return [f"Error Loading File: {e}"]

    def del_dupes(input_list):
        return list(dict.fromkeys(input_list))
    
    def sort_items(input_list):
        return sorted(input_list)
