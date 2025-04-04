from fastapi import FastAPI
from search import SearchEngine
from database import Database
import time

app = FastAPI()

search_engine = SearchEngine()
database = Database()

@app.get("/")
def read_root():
    return {"msg": "this a api for search"}

@app.get("/serialnumber/{text}")
def search(text: str):
    start_time = time.time()
    res = {"msg": "serial number not found"}  # Default response to avoid undefined variable

    try:
        df = database.get_data()
        best_match, best_similarity = search_engine.search_model(text)
        
        if best_match:
            matched_data = df[df["SerialNumber"] == best_match].to_dict(orient="records")
            res = {
                "best_similarity": best_similarity,
                "detail": matched_data,
                "process": "model"
            }
        else:
            matched_sn = search_engine.search_contain(text, df)
            if matched_sn:
                matched_data = df[df["SerialNumber"].isin(matched_sn)].to_dict(orient="records")
                if matched_data:
                    res = {
                        "best_similarity": best_similarity,
                        "detail": matched_data,
                        "process": "contain"
                    }
        
        print(res)
        print("Time to search:", time.time() - start_time)
        return res

    except Exception as e:
        return {"msg": str(e)}