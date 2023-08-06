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
    position: int


@dataclasses.dataclass
class CommentValidator(Validator[Source]):
    dto_list: list[CommentDto]

    @validate()
    async def test1(self):
        post_ids = range(1, 10)
        for i, dto in enumerate(self.dto_list):
            if dto.post_id not in post_ids:
                self.context.add_error(
                    ErrorSchema(
                        code=ErrorCodeEnum.not_found.value,
                        message="Id doen't not exists",
                        detail=f"Post with id={dto.post_id} not found",
                        source=Source(
                            local="data/post_id",
                            position=i,
                        ),
                    )
                )

    @validate()
    async def test2(self):
        owner_ids = range(1, 10)
        for i, dto in enumerate(self.dto_list):
            if dto.owner_id not in owner_ids:
                self.context.add_error(
                    ErrorSchema(
                        code=ErrorCodeEnum.not_found.value,
                        message="Id doen't not exists",
                        detail=f"User with id={dto.post_id} not found",
                        source=Source(
                            local="data/owner_id",
                            position=i,
                        ),
                    )
                )


if __name__ == "__main__":
    try:
        coroutine = CommentValidator(
            [
                CommentDto(comment="comment", owner_id=1, post_id=1),
                CommentDto(comment="comment", owner_id=1, post_id=100),
                CommentDto(comment="comment", owner_id=100, post_id=1),
                CommentDto(comment="comment", owner_id=1234, post_id=1234),
            ]
        ).validate()
        asyncio.run(coroutine)
    except ValidationError as e:
        for message in e.messages:
            print(message)
