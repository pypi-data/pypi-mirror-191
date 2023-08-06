import asyncio
import dataclasses
from pydantic import BaseModel
from business_validator import (
    Validator,
    ValidationError,
    ErrorSchema,
    ErrorCodeEnum,
    validate,
)


class CommentDto(BaseModel):
    comment: str
    post_id: int
    owner_id: int


class Source(BaseModel):
    local: str


@dataclasses.dataclass
class CommentValidator(Validator[Source]):
    dto: CommentDto

    @validate()
    async def test1(self):
        post_ids = list(range(1, 10))

        if self.dto.post_id not in post_ids:
            self.context.add_error(
                ErrorSchema(
                    code=ErrorCodeEnum.not_found.value,
                    message="Id doen't not exists",
                    detail=f"Post with id={self.dto.post_id} not found",
                    source=Source(
                        local="data/post_id",
                    ),
                )
            )

    @validate()
    async def test2(self):
        owner_ids = list(range(1, 10))

        if self.dto.owner_id not in owner_ids:
            self.context.add_error(
                ErrorSchema(
                    code=ErrorCodeEnum.not_found.value,
                    message="Id doen't not exists",
                    detail=f"User with id={self.dto.post_id} not found",
                    source=Source(
                        local="data/owner_id",
                    ),
                )
            )


if __name__ == "__main__":
    try:
        asyncio.run(
            CommentValidator(
                CommentDto(comment="comment", owner_id=1234, post_id=222)
            ).validate()
        )
    except ValidationError as e:
        print(e.messages)
