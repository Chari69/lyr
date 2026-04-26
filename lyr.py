def main():
	import sys
	from app.application import run_application

	initial_path = sys.argv[1] if len(sys.argv) > 1 else None
	run_application(initial_path)


if __name__ == "__main__":
	main()

