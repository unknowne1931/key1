import random
from PIL import Image, ImageDraw
import io
import requests

# === CONFIG ===
UPLOAD_URL = "https://backend.stawro.com/stawro/upload.php"
POST_URL = "http://localhost/api/question"

DIFFICULTY = input("Enter difficulty (Too Easy, Easy, Medium, Tough, Too Tough): ")
NUM_QUESTIONS = int(input("How many questions to generate? "))

difficulty_config = {
    "Too Easy": {"size": 9, "seconds": 10},
    "Easy": {"size": 13, "seconds": 15},
    "Medium": {"size": 17, "seconds": 20},
    "Tough": {"size": 21, "seconds": 25},
    "Too Tough": {"size": 27, "seconds": 30}
}

config = difficulty_config.get(DIFFICULTY, difficulty_config["Medium"])
CELL_SIZE = 25
COLS = ROWS = config["size"]
GOAL_POS = (COLS // 2, ROWS // 2)


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = [True, True, True, True]  # Top, Right, Bottom, Left
        self.visited = False


class MazeGame:
    def __init__(self, force_no=False):
        self.grid = [Cell(x, y) for y in range(ROWS) for x in range(COLS)]
        self.generate_maze()
        self.force_no = force_no
        if self.force_no:
            self.block_path_somewhere()
        self.player = (0, 0)

    def index(self, x, y):
        if 0 <= x < COLS and 0 <= y < ROWS:
            return y * COLS + x
        return -1

    def generate_maze(self):
        stack = []
        start = self.grid[0]
        start.visited = True
        stack.append(start)

        while stack:
            current = stack[-1]
            neighbors = []
            directions = [(0, -1, 0, 2), (1, 0, 1, 3), (0, 1, 2, 0), (-1, 0, 3, 1)]

            for dx, dy, wall, opp in directions:
                nx, ny = current.x + dx, current.y + dy
                idx = self.index(nx, ny)
                if idx != -1 and not self.grid[idx].visited:
                    neighbors.append((self.grid[idx], wall, opp))

            if neighbors:
                neighbor, wall, opp_wall = random.choice(neighbors)
                current.walls[wall] = False
                neighbor.walls[opp_wall] = False
                neighbor.visited = True
                stack.append(neighbor)
            else:
                stack.pop()

    def block_path_somewhere(self):
        visited = set()
        queue = [(0, 0, [])]

        while queue:
            x, y, path = queue.pop(0)
            visited.add((x, y))
            cell = self.grid[self.index(x, y)]

            if (x, y) == GOAL_POS:
                if len(path) > 4:
                    bx, by = path[len(path) // 2]
                    direction_map = [(0, -1, 0, 2), (1, 0, 1, 3), (0, 1, 2, 0), (-1, 0, 3, 1)]
                    for dx, dy, wall, opp_wall in direction_map:
                        nx, ny = bx + dx, by + dy
                        if (nx, ny) in path:
                            idx1 = self.index(bx, by)
                            idx2 = self.index(nx, ny)
                            if idx1 != -1 and idx2 != -1:
                                self.grid[idx1].walls[wall] = True
                                self.grid[idx2].walls[opp_wall] = True
                                return
                return

            directions = [(0, -1, 0), (1, 0, 1), (0, 1, 2), (-1, 0, 3)]
            for dx, dy, wall in directions:
                nx, ny = x + dx, y + dy
                idx = self.index(nx, ny)
                if idx != -1 and not cell.walls[wall] and (nx, ny) not in visited:
                    queue.append((nx, ny, path + [(x, y)]))

    def draw_maze(self):
        maze_width = CELL_SIZE * COLS
        maze_height = CELL_SIZE * ROWS
        padding = 20  # padding on all sides

        # Create a larger image for padding
        padded_img = Image.new("RGB", (maze_width + 2 * padding, maze_height + 2 * padding), "white")
        draw = ImageDraw.Draw(padded_img)

        # Draw maze walls
        for cell in self.grid:
            x = cell.x * CELL_SIZE + padding
            y = cell.y * CELL_SIZE + padding
            if cell.walls[0]: draw.line([x, y, x + CELL_SIZE, y], fill="black", width=2)
            if cell.walls[1]: draw.line([x + CELL_SIZE, y, x + CELL_SIZE, y + CELL_SIZE], fill="black", width=2)
            if cell.walls[2]: draw.line([x + CELL_SIZE, y + CELL_SIZE, x, y + CELL_SIZE], fill="black", width=2)
            if cell.walls[3]: draw.line([x, y + CELL_SIZE, x, y], fill="black", width=2)

        # Draw player
        px, py = self.player
        draw.ellipse([
            px * CELL_SIZE + 6 + padding,
            py * CELL_SIZE + 6 + padding,
            px * CELL_SIZE + CELL_SIZE - 6 + padding,
            py * CELL_SIZE + CELL_SIZE - 6 + padding
        ], fill="blue")

        # Draw goal
        gx, gy = GOAL_POS
        draw.rectangle([
            gx * CELL_SIZE + 4 + padding,
            gy * CELL_SIZE + 4 + padding,
            gx * CELL_SIZE + CELL_SIZE - 4 + padding,
            gy * CELL_SIZE + CELL_SIZE - 4 + padding
        ], fill="red")

        # Resize to desired size (after padding applied)
        padded_img = padded_img.resize((400, 250))
        return padded_img


    def is_goal_reachable(self):
        visited = set()
        queue = [self.player]
        while queue:
            x, y = queue.pop(0)
            if (x, y) == GOAL_POS:
                return True
            visited.add((x, y))
            cell = self.grid[self.index(x, y)]
            directions = [(0, -1, 0), (1, 0, 1), (0, 1, 2), (-1, 0, 3)]
            for dx, dy, wall in directions:
                nx, ny = x + dx, y + dy
                idx = self.index(nx, ny)
                if idx != -1 and not cell.walls[wall] and (nx, ny) not in visited:
                    queue.append((nx, ny))
        return False

    def upload_image(self, img):
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        files = {"screenshot": ("maze.png", buf, "image/png")}
        res = requests.post(UPLOAD_URL, files=files)
        return res.json().get("path", None)

    def post_question(self, img_url, answer):
        payload = {
            "question": "Can the man reach the center of the maze?",
            "answer": answer,
            "a": "Yes",
            "b": "No",
            "c": "----",
            "d": "----",
            "language": "English",
            "category": "Maze Logic",
            "difficulty": DIFFICULTY,
            "type": "Mental Ability",
            "image": f"https://backend.stawro.com/stawro/{img_url}",
            "seconds": str(config["seconds"])
        }
        res = requests.post(POST_URL, json=payload)
        if res.status_code == 200:
            print("✅ Question posted successfully!")
        else:
            print("❌ Failed to post question:", res.text)

    def run(self):
        img = self.draw_maze()
        reachable = self.is_goal_reachable()
        answer = "No" if self.force_no else ("Yes" if reachable else "No")

        # Random yes/no print
        print("🔀 Random Pick (Unrelated):", random.choice(["Yes", "No"]))

        img_url = self.upload_image(img)
        if img_url:
            print(f"✅ Image uploaded! Answer: {answer}")
            self.post_question(img_url, answer)
        else:
            print("❌ Image upload failed.")


# === MAIN LOOP ===
for i in range(NUM_QUESTIONS):
    print(f"\n--- Generating Maze {i+1}/{NUM_QUESTIONS} ---")
    make_unsolvable = random.random() < 0.5  # 50% chance to force answer "No"
    game = MazeGame(force_no=make_unsolvable)
    game.run()
