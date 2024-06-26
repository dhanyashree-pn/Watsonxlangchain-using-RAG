from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens
from typing import Any, List, Mapping, Optional, Union, Dict
from pydantic import BaseModel, Extra
from ibm_watson_machine_learning.foundation_models import Model


class LangChainInterface(LLM, BaseModel):
    credentials: Optional[Dict] = None
    model: Optional[str] = None
    params: Optional[Dict] = None
    project_id: Optional[str] = None

    class Config:
        extra = Extra.forbid

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        _params = self.params or {}
        return {
            **{"model": self.model},
            **{"params": _params},
        }

    @property
    def _llm_type(self) -> str:
        return "IBM WATSONX"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        params = self.params or {}
        model = Model(model_id=self.model, params=params, credentials=self.credentials, project_id=self.project_id)
        text = model.generate_text(prompt)
        if stop is not None:
            text = enforce_stop_tokens(text, stop)
        return text
