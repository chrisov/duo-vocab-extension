from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Label, Button, Static
from textual.containers import Grid, Container, Vertical

class DataValidator(App):
	# CSS = """
	# 	Container {
	# 		margin: 1 2;
	# 		padding: 1;
	# 		border: solid $primary;
	# 	}
	# 	Grid {
	# 		grid-columns: 1fr 1fr 1fr;
	# 		grid-rows: auto;
	# 		grid-row-gap: 1;
	# 		grid-column-gap: 2;
	# 		padding: 1;
	# 	}
	# 	Label { 
	# 		padding: 1;
	# 	}
	# 	.actions {
	# 		column-span: 3;
	# 		height: 3;
	# 		align: center middle;
	# 	}

	# 	Container {
	# 		min-width: 20;
	# 		min-height: 3;
	# 	}
	# """

	def __init__(self, raw_data, lang):
		super().__init__()
		self.language = lang
		self.raw_data = raw_data # The data from your Daemon



	def compose(self) -> ComposeResult:
		yield Header()
		with Grid():
			with Container():
				yield Label("Word:")
				yield Input(value=self.raw_data['Word'], id="word", disabled=True)
				yield Static(f"Language: {self.language}")
			
			with Container():
				yield Label("Article:")
				yield Input(value=self.raw_data['Article'], id="article")
				yield Static(f"Description: Article. Check the box to append")
			
			with Container():
				yield Label("English:")
				yield Input(value=self.raw_data['English'], id="english")
				yield Static(f"Description: Word's translation. Check the box to append")
			
			with Container():
				yield Label("Plural:")
				yield Input(value=self.raw_data['Plural'], id="plural")
				yield Static(f"Description: Plural form.")
			
			with Container():
				yield Label("Grammar:")
				yield Input(value=self.raw_data['Grammar'], id="grammar")
				yield Static(f"Description: Grammar type. Check the box to append")
	
			with Container():
				yield Label("Category:")
				yield Input(value=self.raw_data['Category'], id="category")
				yield Static(f"Description: Valid categories: [Noun, Verb, Adjective, Adverb, Pronoun, Phrase].")

			with Container():
				yield Label("Count:")
				yield Input(value=str(self.raw_data['Count']), id="count", disabled=True)
				yield Static(f"Description: Counts the number of occurunces in the tester.")

			with Container():
				yield Label("Success Rate:")
				yield Input(value=str(self.raw_data['SuccessRate']), id="successrate", disabled=True)
				yield Static(f"Description: The rate of successful input.")


			with Grid(id="actions", classes="actions"):
				yield Button("Commit to DB", variant="success", id="save")
				yield Button("Discard", variant="error", id="delete")
		yield Footer()



	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "save":
			# Extract current values from the UI
			final_data = {
				"Word": self.query_one("#word").value,
				"Article": self.query_one("#article").value,
				"English": self.query_one("#english").value,
				"Plural": self.query_one("#plural").value,
				"Grammar": self.query_one("#grammar").value,
				"Category": self.query_one("#category").value,
				"Count": self.query_one("#count").value,
				"SuccessRate": self.query_one("#successrate").value,
			}
			# Your SQLite Logic here: db.insert(final_data)
			self.exit(result=final_data)
		else:
			self.exit(result="Discarded")



if __name__ == "__main__":
	# Simulate data caught by your Daemon
	language = 'pt'
	sample_entry = {
		"Word": "mala",
		"Article": "a",
		"English": "suitcase",
		"Plural": "malas",
		"Grammar": "Noun",
		"Category": "Abstract",
		"Count": 0,
		"SuccessRate": 0.0
	}
	app = DataValidator(sample_entry, language)
	result = app.run()
	print(f"Action taken: {result}")