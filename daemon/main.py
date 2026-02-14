from app.server_utils import load_data_from_json, write_data_to_json
from daemon.daemon_utils import get_active_session, str_to_list
from daemon.model import model_response
# from time import sleep
import datetime

## Find active language [OK]: Set when the vocab sent to the backend

## While true [TODO] Find a way to exit the loop

## Call LLM

## Put the modified data into the processed dict and set approved = false



if __name__ == "__main__":
	# while (True):
	
	## Set the characteristics
	language = get_active_session()
	data = load_data_from_json("VOCAB_COPY_PATH")
	vocab = data[language]['unprocessed']['vocabulary']

	print(vocab)
	print(language)

	## Call the LLM 
	response = model_response(vocab, language)
	print(response)

	## Turn the str response into a list response
	# processed = str_to_list(response)

	# ## Update the data
	# data[language]['unprocessed']['vocabulary'] = []
	# data[language]['processed'] = {'timestamp': datetime.datetime.now()}
	# data[language]['processed'] = {'vocabulary': processed}
	# # data[language]['processed'] = {'isUserApproved': False}
	
	# ## Write the data to the JSON file
	# write_data_to_json("VOCAB_COPY_PATH", data)

		# sleep(100)
		