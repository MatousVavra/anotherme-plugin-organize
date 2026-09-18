import asyncio
import logging

from fastapi import APIRouter, HTTPException

from pydantic import BaseModel, Field


class OrganizeRequest(BaseModel):
    instructions: str = Field(min_length=1, max_length=8000)


class OrganizeResponse(BaseModel):
    suggestions: str


class Plugin:
    def on_load(self, ctx):
        self._vault = ctx.vault_manager
        self._llm = ctx.llm_client
        self._ctx = ctx

        router = APIRouter()

        @router.post("", response_model=OrganizeResponse)
        async def organize(body: OrganizeRequest):
            vn = self._ctx.vault_name
            try:
                vault_context = self._vault.get_vault_context(vn)
                suggestions = await asyncio.to_thread(
                    lambda: self._llm.organize(vault_context, body.instructions, caller="organize")
                )
            except Exception as e:
                logging.getLogger(__name__).exception("Organize failed")
                raise HTTPException(500, "Failed to organize vault")
            return OrganizeResponse(suggestions=suggestions)

        ctx.register_router(router)
