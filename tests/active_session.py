from app.server_utils import load_data_from_json, write_data_to_json, set_active_session


if __name__ == "__main__":
	session_data = load_data_from_json("SESSION_PATH")
	print("Current session data:")
	print(session_data)

	language = input("\nLanguage to mark as active: ").strip()
	set_active_session(session_data, language)
	write_data_to_json("SESSION_PATH", session_data)

	print("\nUpdated session data:")
	print(session_data)