import curses
import sys

def choose_file(title, files):
	try:
		stdscr = curses.initscr()
		curses.noecho()
		curses.cbreak()
		stdscr.keypad(True)

		selected = 0
		while True:
			stdscr.clear()
			stdscr.addstr(0, 0, title, curses.A_BOLD)

			for i, file_name in enumerate(files):
				line = f"{i+1}. {file_name}"
				stdscr.addstr(i+2, 0, line)
				if i == selected:
					stdscr.addstr(i+2, 0, line, curses.A_REVERSE)

			stdscr.refresh()
			key = stdscr.getch()

			if key == curses.KEY_UP:
				selected = max(0, selected - 1)
			elif key == curses.KEY_DOWN:
				selected = min(len(files) - 1, selected + 1)
			elif key == 10:  # Enter key
				break

		curses.nocbreak()
		stdscr.keypad(False)
		curses.echo()
		curses.endwin()

		return files[selected]
	except KeyboardInterrupt:
		curses.nocbreak()
		stdscr.keypad(False)
		curses.echo()
		curses.endwin()
		print("Bye")
		sys.exit()

if __name__ == '__main__':
	files = ["file1.txt", "file2.txt", "file3.txt"]
	selected_file = choose_file("Title #1:", files)
	if selected_file is not None:
		print(f"You selected file {selected_file}")
	