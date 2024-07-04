import ctranslate2
import transformers
from huggingface_hub import snapshot_download
import logging

# Set up logging
logging.basicConfig(filename='sql_generator.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class SQLGenerator:
    def __init__(self):
        try:
            model_id = "./llama3_8b_ct2"
            #model_path = snapshot_download(model_id)
            self.model = ctranslate2.Generator(model_id)
            self.tokenizer = transformers.AutoTokenizer.from_pretrained(model_id)
            logging.info("SQL Generator initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing SQL Generator: {str(e)}")
            raise

    def generate_sql(self, user_input):
        try:
            prompt = f"""
CREATE TABLE stadium (
    stadium_id number,
    location text,
    name text,
    capacity number,
    highest number,
    lowest number,
    average number
)

CREATE TABLE singer_in_concert (
    concert_id number,
    singer_id text
)

-- Using valid SQLite, answer the following questions for the tables provided above.

-- {user_input} ? (Generate 1 Sql query. No explanation needed)

answer:
            """

            messages = [
                {"role": "system", "content": "You are SQL Expert. Given an input question and schema, answer with correct sql query"},
                {"role": "user", "content": prompt},
            ]

            input_ids = self.tokenizer.apply_chat_template(
                messages, 
                tokenize=False, 
                add_generation_prompt=True
            )

            terminators = [
                self.tokenizer.eos_token_id,
                self.tokenizer.convert_tokens_to_ids("<|eot_id|>")
            ]

            input_tokens = self.tokenizer.convert_ids_to_tokens(self.tokenizer.encode(input_ids))

            results = self.model.generate_batch([input_tokens], include_prompt_in_result=False, max_length=256, sampling_temperature=0.6, sampling_topp=0.9, end_token=terminators)
            output = self.tokenizer.decode(results[0].sequences_ids[0])

            logging.info(f"SQL generated for input: {user_input}")
            return output.strip()
        except Exception as e:
            logging.error(f"Error generating SQL: {str(e)}")
            raise
