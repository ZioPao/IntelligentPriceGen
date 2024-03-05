
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain_community.vectorstores import Chroma
from langchain.chains import LLMChain
from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
import json

from pydantic import BaseModel, Field
from typing import Deque, List, Optional, Tuple

class InputJsonData(BaseModel):

    fullType: str
    name: str
    category: str = "[]"
    weight: float
    additionalData: Optional[dict] = {}



class OutputJsonData(BaseModel):
    fullType: str
    price: int
    tag : str




examples = [


    # Essential Items as a base
    {
        "input": InputJsonData(fullType="Base.GranolaBar", name="Granola Bar", category="[Food]", weight=0.2).model_dump_json(),
        "output": OutputJsonData(fullType="Base.GranolaBar", price=20, tag="FOOD").model_dump_json()
    },
    {
        "input": InputJsonData(fullType="Base.BaseballBat", name="Baseball Bat", weight=2, category="[Blunt, Sports]", additionalData={"damage": 0.95}).model_dump_json(),
        "output": OutputJsonData(fullType="Base.BaseballBat", price=200, tag="WEAPON").model_dump_json()
    },



    # Random Junk
    {
        "input": InputJsonData(fullType="Base.ToiletPaper", name="Toilet Paper", weight=0.2, category="[Junk]").model_dump_json(), 
        "output": OutputJsonData(fullType="Base.ToiletPaper", price=5, tag="VARIOUS").model_dump_json()
    },
    


]




t = InputJsonData(fullType="Base.GranolaBar", name="Granola Bar", category="[Food]", weight=0.2)